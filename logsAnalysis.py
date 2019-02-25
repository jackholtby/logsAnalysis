# Name: logsAnalysis
# Author: Jack Holtby
# Purpose: Connect to the news postgresql database and return:
# 1. The three most popular articles of all time in the database.
# 2. A list of the authors listed in order of popularity based on article views.
# 3. A list of the days on which more than 1% of requests lead to errors.
#
# These will be output in text. No arguments. No input.

# Imports
import psycopg2

DBNAME = "news"

topThreeAuthorQuery = '''
SELECT articles.title, count(log.path) AS number
FROM articles LEFT JOIN log
ON articles.slug = substring(log.path FROM 10)
GROUP BY articles.title
ORDER BY number DESC LIMIT 3;
'''

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

badDaysQuery = '''
SELECT total, totalError
FROM (
select date_part('year', time::date) as year,
date_part('month', time::date) as monthly, date_part('day', time::date) as daily,
count(path) as total
from log
group by year, monthly, daily
order by year, monthly, daily
) as tmpOK
JOIN
(select date_part('year', time::date) as year,
date_part('month', time::date) as monthly, date_part('day', time::date) as daily,
count(path) as totalError
from log where status = '404 NOT FOUND'
group by year, monthly, daily
order by year, monthly, daily
) as tmpERROR
ON tmpOK.year = tmpERROR.year
AND tmpOK.monthly = tmpERROR.monthly
AND tmpOK.daily = tmpERROR.daily
;
'''

select date_part('year', time::date) as year,
date_part('month', time::date) as monthly, date_part('day', time::date) as daily,
count(path)
from log where status = '200 OK'
group by tmp.year, tmp.monthly, daily
order by year, monthly, daily;
'''

db = psycopg2.connect(database=DBNAME)
c = db.cursor()
c.execute(topThreeAuthorQuery)
c.execute(mostProlificQuery)
c.execute(badDaysQuery)
db.close()
