#!/usr/bin/env python3
# Name: logsAnalysis
# Author: Jack Holtby
# Purpose: Connect to the news postgresql database and return:
# 1. The three most popular articles of all time in the database.
# 2. A list of the authors in order of popularity based on article views.
# 3. A list of the days on which more than 1% of requests lead to errors.
#
# These will be output in text. No arguments. No input.

# Imports
import psycopg2

DBNAME = "news"

topThreeTemp = '''
"%s" - with %s views'''

mostPopularTemp = '''
"%s" - %s views'''

badDaysTemp = '''
%s/%s/%s - %s%% errors'''

# Query to get the top three most popular articles of all time
# (based on article views)
topThreeArticlesQuery = '''
SELECT articles.title, count(log.path) AS number
FROM articles LEFT JOIN log
ON articles.slug = substring(log.path FROM 10)
GROUP BY articles.title
ORDER BY number DESC LIMIT 3;
'''

# Query to get the most popular author of all time (based on article views)
mostPopularQuery = '''
SELECT authors.name, tmp.number
FROM (
SELECT articles.author AS id, count(log.path) AS number
FROM articles LEFT JOIN log
ON articles.slug = substring(log.path FROM 10)
GROUP BY articles.author
ORDER BY number desc
) AS tmp
JOIN authors ON tmp.id = authors.id;
'''

# Query to get list of days and percentage of requests that lead to Errors
# only when those errors made up more than 1% of the requests made that day.
badDaysQuery = '''
SELECT
day, month, year,
TRUNC(CAST(totalerror AS DECIMAL)/total*100 , 2) AS percentError
FROM
(
SELECT
CAST(tmpOK.year AS INTEGER), cast(tmpOK.month AS integer),
CAST(tmpOK.day AS INTEGER), total, totalerror
FROM (
SELECT date_part('year', time::DATE) AS year,
date_part('month', time::DATE) AS month, date_part('day', time::DATE) AS day,
count(path) AS total
FROM log
GROUP BY year, month, day
ORDER BY year, month, day
) AS tmpOK
JOIN
(SELECT date_part('year', time::DATE) AS year,
date_part('month', time::DATE) AS month, date_part('day', time::DATE) AS day,
count(path) AS totalerror
FROM log WHERE status = '404 NOT FOUND'
GROUP BY year, month, day
ORDER BY year, month, day
) AS tmpERROR
ON tmpOK.year = tmpERROR.year
AND tmpOK.month = tmpERROR.month
AND tmpOK.day = tmpERROR.day
) AS meta
WHERE TRUNC(CAST(totalerror AS DECIMAL)/total*100 , 2) > 1;
'''

# Connect to the Database....if it's there....ooohhheeeooohhheeeee
try:
    db = psycopg2.connect(database=DBNAME)
except psycopg2.Error as error:
    print("Uh nuuu bruuu, the detabis ain't connictible to.")
    print(error.pgerror)
    print(error.diag.message_detail)
    sys.exit(1)


c = db.cursor()

# Run the top three articles query.
c.execute(topThreeArticlesQuery)
topThree = c.fetchall()
topThreeOutput = "".join(topThreeTemp % (title, number)
                         for title, number in topThree)

# Run the most popular author query.
c.execute(mostPopularQuery)
mostPopular = c.fetchall()
mostPopularOutput = "".join(mostPopularTemp %
                            (name, number) for name, number in mostPopular)

# Run the bad days query.
c.execute(badDaysQuery)
badDays = c.fetchall()
badDaysOutput = "".join(badDaysTemp %
                        (day, month, year, percenterror)
                        for day, month, year, percenterror in badDays)

# Print out results nicely.

print("1. What are the most popular articles of all time?",
      topThreeOutput, "\n")
print("2. Who are the most popular article authors of all time?",
      mostPopularOutput, "\n")
print("3. On which days did more than 1% of requests lead to errors?",
      badDaysOutput)

# Close the connection to the database
db.close()
