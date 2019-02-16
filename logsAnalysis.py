# Name: logsAnalysis
# Author: Jack Holtby
# Purpose: Connect to the news postgresql database and return:
# 1. The three most popular articles of all time in the database.
# 2. A list of the authors listed in order of how prolific they are (prolificacy?).
# 3. A list of the days on which more than 1% of requests lead to errors.
#
# These will be output in text. No arguments. No input.

# Imports
import psycopg2

DBNAME = "news"

topThreeAuthorQuery = '''
INSERT QUERY HERE
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
