# Logs Analysis - Udacity Project (1)
### Author: Jack Holtby

## Purpose: Connect to the news postgresql database and return:
* 1. The three most popular articles of all time in the database.
* 2. A list of the authors in order of popularity based on article views.
* 3. A list of the days on which more than 1% of requests lead to errors.

These will be output in text. No arguments. No input.

## Program Design:

This is a Python 3 program. It runs on a PostgreSQL database which contains
three tables: articles, authors, and log.

The three queries are placed inside variables to separate database requests
from code. We've avoided using views to eradicate any need for making changes
to the database.

## How to run the code:

To run the code, you'll need to setup the database.

* 1. Install Python (version 3).
If you're running linux, run:

apt install python3 python3-pip

If you're using Ubuntu then append "sudo" to the front of that command.
If you're using Windows or Mac you can find python through the following links:
https://www.python.org/downloads/mac-osx/
https://www.python.org/downloads/windows/

Installation instructions can be found here: https://wiki.python.org/moin/BeginnersGuide/Download.

* 2. Install VirtualBox
You can install virtualbox on debian based linux distros with:

apt install virtualbox

If you're running Debian unstable then you'll be getting VirtualBox version 6.1
or some such thing. This will not work with vagrant for some reason. You'll be
able to boot (from virtualbox, don't even try booting using "vagrant up"),
but the shared folders won't work. So I recommend installing on stable or
equivalent.

Get the old version that works from here: https://www.virtualbox.org/wiki/Download_Old_Builds_5_1

* 3. Install vagrant
You install vagrant to run the virtualbox system. You can find it here:
https://www.vagrantup.com/downloads.html

Or you can install it using apt if you're using a real operating system.

apt install vagrant

Add "sudo" if you're using Ubuntu or other derivatives.

You'll then need to download the configuration for the system that will run
on virtualbox and vagrant. This can be downloaded here:
https://s3.amazonaws.com/video.udacity-data.com/topher/2018/April/5acfbfa3_fsnd-virtual-machine/fsnd-virtual-machine.zip

Unzip this file into a directory of your choice. Enter the directory called
'vagrant' inside the directory you just unzipped. While inside the vagrant
directory, run the following command:

vagrant up

This will take quite some time to set up, depending on your internet connection.

* 4. Log into the vagrant os

You can log into the system with:

vagrant ssh

While logged in, you can find the data in the /vagrant folder.

If it is not there, see the next step.

* 5. Set up the data.
The data for this project can be found here:
https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip

Download it and unzip it into the directory that is shared with vagrant.
This is the directory called vagrant inside the unzipped folder from the vagrant
installation.

There should be a file called newsdata.sql in the vagrant directory now.
Run the following command:

psql -d news -f newsdata.sql

If you get errors like psql: FATAL: database "news" does not exist, then you
need to create it.

Run the following command:

psql

Then you will be inside a PostgreSQL interactive prompt. Create the database with:

create database news;

Then run the first command in this section again. Shoobeedoobeedooo

* 6. And now that's all setup, you can copy the logsAnalysis file into your
shared vagrant folder and then log into vagrant and run it with the following:

python3 logsAnalysis.py


Note: I looked up methods and ways to do database queries and output code
on stackoverflow and such websites. However, the content was always different,
although helpful, and hence I did not plagarise any part of my project, as far
as I understand it. For example, I used a stackoverflow question about sorting
by date in postgresql to sort day in the database. The example I found would
have been what I'd find in a tutorial, and I simply changed it to work with
days instead of weeks.

The following is a list of sites posts/sites I used to learn how to do
specific things in my project. This is the gist of it.

https://stackoverflow.com/questions/6908143/should-i-put-shebang-in-python-scripts-and-what-form-should-it-take
https://stackoverflow.com/questions/34504497/division-not-giving-my-answer-in-postgresql
https://stackoverflow.com/questions/39682194/how-to-calculate-percentage-for-number-of-values-in-a-column-in-sql#39682266 (used this to figure out how to get a percentage...)
https://stackoverflow.com/questions/36024712/how-to-group-by-week-in-postgresql (This for sorting by a given time unit)
https://stackoverflow.com/questions/2076685/how-to-join-the-results-of-two-subqueries-in-postgresql (when working with subqueries)
https://stackoverflow.com/questions/32467019/extract-a-substring-from-a-text-string-in-postgres (when getting substrings)
