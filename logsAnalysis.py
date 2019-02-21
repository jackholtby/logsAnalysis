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
ORDER BY num DESC LIMIT 3;
'''

mostProlificQuery = '''
INSERT QUERY HERE
'''

badDaysQuery = '''
INSERT QUERY HERE
'''

db = psycopg2.connect(database=DBNAME)
c = db.cursor()
c.execute(topThreeAuthorQuery)
c.execute(mostProlificQuery)
c.execute(badDaysQuery)
db.close()
