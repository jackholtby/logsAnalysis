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
trunc(cast(totalerror as decimal)/total*100 , 2) as percentError
from
(
SELECT
cast(tmpOK.year as integer), cast(tmpOK.month as integer),
cast(tmpOK.day as integer), total, totalerror
FROM (
select date_part('year', time::date) as year,
date_part('month', time::date) as month, date_part('day', time::date) as day,
count(path) as total
from log
group by year, month, day
order by year, month, day
) as tmpOK
JOIN
(select date_part('year', time::date) as year,
date_part('month', time::date) as month, date_part('day', time::date) as day,
count(path) as totalerror
from log where status = '404 NOT FOUND'
group by year, month, day
order by year, month, day
) as tmpERROR
ON tmpOK.year = tmpERROR.year
AND tmpOK.month = tmpERROR.month
AND tmpOK.day = tmpERROR.day
) as meta
where trunc(cast(totalerror as decimal)/total*100 , 2) > 1;
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
