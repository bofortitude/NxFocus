#!/usr/bin/python


from mysql import connector



host = '10.0.12.21'
username = 'root'
password = 'fortinet'
serverPort = 3306
database = None
useCharset = 'utf8'
db_index=True



mySqlConfig={'host':host, # default is 127.0.0.1
'user':username,
'password':password,
'port':serverPort ,#default is 3306
'database':database,
'charset': useCharset #default is utf8
}
try:
	myConnection = connector.connect(**mySqlConfig)
except connector.Error as e:
	print('connect fails!{}'.format(e))

myCursor = myConnection.cursor()

sql = 'select host,user,authentication_string from mysql.user'
myCursor.execute(sql)

resultSet = myCursor.fetchall()
if resultSet:
	for row in resultSet:
		# print "%d, %s, %s, %d, %s, %s" % (row[0],row[1],row[2],row[3],row[4],row[5])
		print row

myCursor.close()
myConnection.close()




