#!/usr/bin/python

import cgitb
import cgi
import sqlite3
import hashlib
import time
import datetime
import urllib
import Cookie
import os
# import httplib
from random import randint
#import cookielib


def groupsHTMLForUsername(username):
	conn = sqlite3.connect('nimbus.db') # automatically creates file if doesn't exist
	c = conn.cursor()
	c.execute('SELECT * FROM groups WHERE username=? ORDER BY id DESC', (username,))

	group_i = 0
	result_string = ''
	for group in c:
		group_i = group_i + 1
		result_group_id = str(group[0])
		result_group_name = group[2]
		result_group_color = str(group[3])
		result_group_timestamp = str(group[4])
		result_group_timeconverted = time.mktime(time.strptime(result_group_timestamp, '%Y-%m-%d %H:%M:%S.%f')) # time.mktime(time.strptime(result_group_timestamp, '%Y-%m-%d %H:%M:%S').timetuple())
		result_group_timestring = datetime.datetime.fromtimestamp(result_group_timeconverted).strftime('%m/%d/%Y')

		# result_group_timestring = result_group_timeconverted.strftime("%d/%m/%y")
		result_string += '<div class="group" id="' + result_group_id + '" style="color:' + result_group_color + '"><div class="group_number">' + str(group_i) + '</div>' + result_group_name + '<p class="group_subtitle"> Created ' + result_group_timestring + '</p></div>'

	if group_i == 0:
		result_string += '<div class="message">No groups yet :)</div>'
	else:
		group_plural_suffix = 's'
		if group_i == 1:
			group_plural_suffix = ''
		result_string = '<div class="group_header">' + str(group_i) + ' Group' + group_plural_suffix + '</div>' + result_string
		
	conn.commit()
	conn.close()

	return result_string

cgitb.enable()

stored_cookie_string = os.environ.get('HTTP_COOKIE') #look for a cookie
# retrieve form data from GET request
user_form = cgi.FieldStorage()

submit_value = user_form['submit'].value 

if submit_value == 'Delete':
	cookie = Cookie.SimpleCookie(stored_cookie_string)
	if not 'account_cookie' in cookie:	
		original_page = urllib.urlopen('http://nimsyllabus.com/index.html')
		original_page_text = original_page.read()
		augmented_text = original_page_text.replace('</body>', '<div class="message">Cannot find username for current account, please log in again.</div>' + '</body>')
		print 'Content-Type: text/html\n\n' + 'No username found'
	else:
		username = cookie['account_cookie'].value
		groupId = user_form['id'].value
		
		conn = sqlite3.connect('nimbus.db') # automatically creates file if doesn't exist
		c = conn.cursor()
		
		#c.execute("SELECT * FROM groups WHERE username='?'' AND id=?', (username, groupId))
		#if c.rowcount <= 0:
		#	conn.commit()
		#	conn.close()
		#	print 'Content-Type: text/html\n\n' + str(c.rowcount) + ' groups found for username=' + username + ' and id=' + groupId
		#else:
		c.execute('DELETE FROM groups WHERE username=? AND id=?', (username, groupId))
		conn.commit()
		conn.close()

		#result_string = '<div class="message">Deleted group successfully.</div>'
		#result_string += groupsHTMLForUsername(username)

		print 'Content-Type: text/html\n\nSuccess'
elif submit_value == 'Logout':
	expiring_cookie = Cookie.SimpleCookie()
	expiring_cookie['account_cookie'] = 'yes it should'
	expiring_cookie['account_cookie']['expires'] = 'Thu, 01 Jan 1970 00:00:00 GMT'
	expiring_cookie['account_cookie']['path'] = '/'
	print expiring_cookie
	#cookielib.CookieJar().clear('nimsyllabus.com')

	original_page = urllib.urlopen('http://nimsyllabus.com/index.html')
	original_page_text = original_page.read()
	augmented_text = original_page_text.replace('</body>', '<div class="message">Logged out. See you soon!</div>' + '</body>')
	print 'Content-Type: text/html\n\n' + augmented_text
elif submit_value == 'Cookie Login':
	conn = sqlite3.connect('nimbus.db') # automatically creates file if doesn't exist
	c = conn.cursor()
	
	username = user_form['username'].value
	current_time = datetime.datetime.now()

	c.execute('CREATE TABLE IF NOT EXISTS groups(id INTEGER primary key, username varchar(250), group_name varchar(250), group_color varchar(250), timestamp datetime)')
	conn.commit()
	conn.close()

	result_string = groupsHTMLForUsername(username)

	original_page = urllib.urlopen('http://nimsyllabus.com/content.html')
	original_page_text = original_page.read()
	augmented_text = original_page_text.replace('</body>', result_string + '</body>')
	print 'Content-Type: text/html\n\n' + augmented_text
elif submit_value == '+ New Group':
	if not stored_cookie_string:
		original_page = urllib.urlopen('http://nimsyllabus.com/index.html')
		original_page_text = original_page.read()
		augmented_text = original_page_text.replace('</body>', '<div class="message">Cannot find logged in account, please log in again.</div>' + '</body>')
		print 'Content-Type: text/html\n\n' + augmented_text
	else:		
		cookie = Cookie.SimpleCookie(stored_cookie_string)
		if not 'account_cookie' in cookie:	
			original_page = urllib.urlopen('http://nimsyllabus.com/index.html')
			original_page_text = original_page.read()
			augmented_text = original_page_text.replace('</body>', '<div class="message">Cannot find username for current account, please log in again.</div>' + '</body>')
			print 'Content-Type: text/html\n\n' + augmented_text
		else:
			username = cookie['account_cookie'].value
		
			conn = sqlite3.connect('nimbus.db') # automatically creates file if doesn't exist
			c = conn.cursor()

			group_name = 'Untitled'
			if 'group_name' in user_form:
				group_name = str(user_form['group_name'].value)

			group_color = 'black'
			if 'group_color' in user_form:
				group_color = str(user_form['group_color'].value)

			current_time = datetime.datetime.now()

			c.execute('CREATE TABLE IF NOT EXISTS groups(id INTEGER primary key, username varchar(250), group_name varchar(250), group_color varchar(250), timestamp datetime)')
			c.execute('INSERT INTO groups (username, group_name, group_color, timestamp) VALUES (?, ?, ?, ?)', (username, group_name, group_color, current_time))
			conn.commit()
			conn.close()

			result_string = groupsHTMLForUsername(username)
			original_page = urllib.urlopen('http://nimsyllabus.com/content.html')
			original_page_text = original_page.read()
			augmented_text = original_page_text.replace('</body>', result_string + '</body>')
			print 'Content-Type: text/html\n\n' + augmented_text
elif not 'username_field' in user_form or not 'password_field' in user_form:
	original_page = urllib.urlopen('http://nimsyllabus.com/index.html')
	original_page_text = original_page.read()
	augmented_text = original_page_text.replace('</body>', '<div class="message">Invalid username or password given. Try again please!</div>' + '</body>')
	print 'Content-Type: text/html\n\n' + augmented_text
else:
	username = user_form['username_field'].value
	password = user_form['password_field'].value
	load_content_page = False

	result_string = ''

	# connect to database, if exists
	conn = sqlite3.connect('nimbus.db') # automatically creates file if doesn't exist
	c = conn.cursor()

	if submit_value == 'Sign Up':
		confirm_password = user_form['confirm_password_field'].value
		if confirm_password != password:
			result_string += '<div class="message">Passwords do not match, please try again!</div>'
		else:
			c.execute('CREATE TABLE IF NOT EXISTS accounts(id INTEGER primary key, username varchar(250), password varchar(250), timestamp datetime)')
			c.execute('SELECT * FROM accounts WHERE username=?', (username,))
			existing_accounts = c.fetchall()

			if len(existing_accounts) > 0:
				result_string += '<div class="message">Account already exists with username <b>' + username + '</b>.</div>'
			else:
				current_time = datetime.datetime.now()
				salt = str(current_time)
				hasher = hashlib.md5()
				hasher.update(password)
				hasher.update(salt)
				encrypted_password = hasher.hexdigest()
				c.execute('INSERT INTO accounts (username, password, timestamp) VALUES (?, ?, ?)', (username, encrypted_password, current_time))
				result_string += '<div class="message">Created new account with username <b>' + username + '</b>.</div>'
				load_content_page = True

				cookie = Cookie.SimpleCookie()
 				cookie['account_cookie'] = username
    				cookie['account_cookie']['path'] = '/'
				print cookie # important thing

	else:
		c.execute('SELECT * FROM accounts WHERE username=?', (username,))
		existing_account = c.fetchone()

		if not existing_account:
			result_string += '<div class="message">Account not found.</div>'
		else:
			existing_timestamp = existing_account[3]
			salt = str(existing_timestamp)
			hasher = hashlib.md5()
			hasher.update(password)
			hasher.update(salt)
			given_encrypted_password = hasher.hexdigest()
			existing_encrypted_password = existing_account[2]

			if given_encrypted_password == existing_encrypted_password:
				load_content_page = True
 				result_string += '<div class="message">Logged in! Welcome back :)</div>'

 				cookie = Cookie.SimpleCookie()
 				#cookie['path'] = cookie_path
 				# cookie['domain'] = 'nimsyllabus.com'
 				#cookie['account'] = 'account'
 				cookie['account_cookie'] = username
   				# cookie['account_cookie']['current_time'] = datetime.datetime.now()
				#token = randint(0,99999999)
    				#cookie['account_cookie']['token'] = token
    				cookie['account_cookie']['path'] = '/'
    				# cookie['account_cookie']['expires'] = ''
    				# cookie['httponly'] = '0'
    				#cookie['account_cookie']['domain'] = 'nimsyllabus.com'
    				#cookie['expires'] = '7' # datetime.date(2020, 4, 20)
    			#cookie['path'] = "/"

				print cookie # important thing

				result_string += groupsHTMLForUsername(username)
	 		else:
	 			result_string += '<div class="message">Incorrect password for account, try again please!</div>'

	# read original HTML page and insert stylized result_string
	# original_page_request = urllib2.Request()
	page_url = 'http://nimsyllabus.com/index.html'

	if load_content_page:
		page_url = 'http://nimsyllabus.com/content.html'
		
	original_page = urllib.urlopen(page_url)
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
	
