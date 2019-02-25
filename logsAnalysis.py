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
year, month, day,
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

# Connect to the Database
db = psycopg2.connect(database=DBNAME)
c = db.cursor()

# Run the top three articles query and output results.
c.execute(topThreeArticlesQuery)
topThree = c.fetchall()

print("Top Three Articles Of All Time")
for row in topThree:
    print('-', row[0], "-", row[1], "views")

print("\n")

# Run the most popular author query and output results.
c.execute(mostPopularQuery)
mostPopular = c.fetchall()

print("Most Popular Authors")
for row in mostPopular:
    print("-", row[0], "-", row[1], "views")

print("\n")

# Run the bad days query and print out results.
c.execute(badDaysQuery)
badDays = c.fetchall()

print("Days With More Than 1% Of Requests Giving Errors")
for row in badDays:
    print("-", row[0], "-", row[1], "-", row[2], " --- ", row[3], "% errors")

# Close the connection to the database
db.close()
