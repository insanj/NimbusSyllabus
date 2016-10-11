#!/usr/bin/python

import cgitb
import cgi
import sqlite3

cgitb.enable()

# create HTML and CSS stub, to be populated with results from database
print 'Content-Type: text/html'
print
print '''<html>
	<head>
		<title>Nimbus Syllabus</title>
		<link rel="stylesheet" type="text/css" href="../style.css">
		<link rel="shortcut icon" type="image/png" href="../favicon.png">
		<link rel="icon" type="image/png" href="../favicon.png">
	</head>
    <body>
        <a href="http://nimsyllabus.com"><img src="../colored_icon.png" />
		<h3>Welcome to</h3>
		<h1>Nimbus Syllabus</h1></a>

		<hr/>
'''

# retrieve form data from GET request
user_form = cgi.FieldStorage()

username = user_form['username_field'].value
password = user_form['password_field'].value

# connect to database, if exists
conn = sqlite3.connect('nimbus.db') # automatically creates file if doesn't exist
c = conn.cursor()

c.execute('CREATE TABLE IF NOT EXISTS accounts(id INTEGER primary key, username varchar(250), password varchar(250))')
c.execute('SELECT * FROM accounts WHERE username=?', (username,))
existing_accounts = c.fetchall()

if len(existing_accounts) > 0:
	print 'Account already exists with username ' + username + '.'
else:
	c.execute('INSERT INTO accounts (username, password) VALUES (?, ?)', (username, password))
	print 'Created new account with username ' + username + '.'

# complete database connection and HTML/CSS stub
conn.commit()
conn.close()

print '''
  </body>
</html>
'''
