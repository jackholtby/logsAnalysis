Name: logsAnalysis.py
Author: Jack Holtby
Purpose: Connect to the news postgresql database and return:
1. The three most popular articles of all time in the database.
2. A list of the authors in order of popularity based on article views.
3. A list of the days on which more than 1% of requests lead to errors.

These will be output in text. No arguments. No input.

Program Design:

This is a Python 3 program. It runs on a PostgreSQL database which contains
three tables: articles, authors, and log.

The three queries are placed inside variables to separate database requests
from code. We've avoided using views to eradicate any need for making changes
to the database. The code just runs.

How to run the code:
To run the code, assuming the database is up and running already, simply run:
python3 logsAnalysis.py


Note: I looked up methods and ways to do database queries and output code
on stackoverflow and such websites. However, the content was always different,
although helpful, and hence I did not plagarise any part of my project, as far
as I understand it.
The following is a list of sites posts/sites I used to learn how to do
specific things in my project. There might have been more but this is the gist of it.

https://stackoverflow.com/questions/6908143/should-i-put-shebang-in-python-scripts-and-what-form-should-it-take
https://stackoverflow.com/questions/34504497/division-not-giving-my-answer-in-postgresql
https://stackoverflow.com/questions/39682194/how-to-calculate-percentage-for-number-of-values-in-a-column-in-sql#39682266 (used this to figure out how to get a percentage...)
https://stackoverflow.com/questions/36024712/how-to-group-by-week-in-postgresql (This for sorting by a given time unit)
https://stackoverflow.com/questions/15691127/postgresql-query-to-count-group-by-day-and-display-days-with-no-data (I looked at this a lot
  but can't don't think I implemented anything that similar.)
https://stackoverflow.com/questions/2076685/how-to-join-the-results-of-two-subqueries-in-postgresql (when working with subqueries)
https://stackoverflow.com/questions/32467019/extract-a-substring-from-a-text-string-in-postgres (when getting substrings)
