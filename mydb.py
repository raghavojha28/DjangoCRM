# Installed Mysql 
# pip install mysql
# pip install mysql-connector-python
# pip install mysql-connector
# change the settings.py file for database connection
# now, in this file, we are making a connection using python

import mysql.connector as mysql

dataBase = mysql.connect(
    host = 'localhost',
    user = 'root',
    passwd = 'Raghavojha.333',
)

# prepare a cursor object
cursorObject = dataBase.cursor()

# create a database

cursorObject.execute('CREATE DATABASE Djangocrm')

print('Database Created')

cursorObject.close()
dataBase.close()