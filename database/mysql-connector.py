import mysql.connector

dbc = mysql.connector.connect(user="root", password="fyp", host="localhost", database="fypdb")

cursor = dbc.cursor()

query = "select reference_no, gpa_ug, major_ug, apply_for from applicants2016"

cursor.execute(query)

for (reference_no, gpa_ug, major_ug, apply_for) in cursor:
	print reference_no
	print "has gpa_ug is {}, major_ug is {}, apply_for is {}".format(gpa_ug, major_ug, apply_for)

cursor.close()

dbc.close()