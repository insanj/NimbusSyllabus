#!/usr/bin/python

import cgitb
import cgi
import sqlite3
import hashlib
import datetime
import urllib

cgitb.enable()

# create HTML and CSS stub, to be populated with results from database
#print 'Content-Type: text/html'
#print
#print '''<html>
#	<head>
#		<title>Nimbus Syllabus</title>
#		<link rel="stylesheet" type="text/css" href="../style.css">
#		<link rel="shortcut icon" type="image/png" href="../favicon.png">
#		<link rel="icon" type="image/png" href="../favicon.png">
#	</head>
 #   <body>
  #      <a href="http://nimsyllabus.com"><img src="../colored_icon.png" />
	#	<h3>Welcome to</h3>
	#	<h1>Nimbus Syllabus</h1></a>
#
#		<hr/>
#'''

# retrieve form data from GET request
user_form = cgi.FieldStorage()

username = user_form['username_field'].value
password = user_form['password_field'].value

# connect to database, if exists
conn = sqlite3.connect('nimbus.db') # automatically creates file if doesn't exist
c = conn.cursor()

c.execute('CREATE TABLE IF NOT EXISTS accounts(id INTEGER primary key, username varchar(250), password varchar(250), timestamp datetime)')
c.execute('SELECT * FROM accounts WHERE username=?', (username,))
existing_accounts = c.fetchall()

result_string = '<br/><hr/>'

if len(existing_accounts) > 0:
	result_string += 'Account already exists with username <b>' + username + '</b>.'
else:
	current_time = datetime.datetime.now()
	salt = str(current_time)
	hasher = hashlib.md5()
	hasher.update(password)
	hasher.update(salt)
	encrypted_password = hasher.hexdigest()
	c.execute('INSERT INTO accounts (username, password, timestamp) VALUES (?, ?, ?)', (username, encrypted_password, current_time))
	result_string += 'Created new account with username <b>' + username + '</b>.'

# read original HTML page and insert stylized result_string
# original_page_request = urllib2.Request()
original_page = urllib.urlopen('http://nimsyllabus.com/index.html')
original_page_text = original_page.read()
augmented_text = original_page_text.replace('</body>', result_string + '</body>')
print 'Content-Type: text/html\n\n' + augmented_text

# complete database connection and HTML/CSS stub
conn.commit()
conn.close()

#print '''
#  </body>
#</html>
#'''

