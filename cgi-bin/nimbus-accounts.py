#!/usr/bin/env python

import cgitb
import cgi
# import sqlite3

cgitb.enable()

user_form = cgi.FieldStorage()

print 'Content-Type: text/html'
print

print '''<html>
  <head>
    <title>Nimbus Syllabus Response</title>
  </head>
  <body>
'''

username = user_form['username_field'].value
password = user_form['password_field'].value

# conn = sqlite3.connect('pizza_orders.db')
# c = conn.cursor()
# c.execute('insert into pizza_orders values (?,?,?,?,?,?)', (name, size, crust, str(toppings), phone, ccn))

# conn.commit()
# conn.close()

print '<h1>You created a Account!!!!</h1>'
print '<h2>Your ' + username + ' with password ' + password + '</h2>'
print '''
  </body>
</html>
'''