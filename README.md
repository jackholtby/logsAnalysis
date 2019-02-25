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
