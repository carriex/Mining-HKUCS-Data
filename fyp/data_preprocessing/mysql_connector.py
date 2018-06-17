# import mysql.connector
# import json
# from django.http import HttpResponse, JsonResponse


# def connect_mysql(db):

# 	dbc = mysql.connector.connect(user="root", password="fyp", host="localhost", database=db)
# 	# cursor = dbc.cursor()
# 	# query = "select reference_no, gpa_ug, major_ug, apply_for from applicants2016"
# 	# cursor.execute(query)
# 	# for (reference_no, gpa_ug, major_ug, apply_for) in cursor:
# 	# 	print reference_no
# 	# 	print "has gpa_ug is {}, major_ug is {}, apply_for is {}".format(gpa_ug, major_ug, apply_for)
# 	return dbc


# def make_query(dbc, query, constraints):
# 	cursor = dbc.cursor()
# 	query = "select reference_no, gpa_ug, major_ug, apply_for from applicants2016"
# 	cursor.execute(query)
# 	dataset = []
# 	for applicant in cursor:
# 		sample = []
# 		for i in range(0,len(applicant)):
# 			sample.append(applicant[i])
# 		dataset.append(sample)
# 	cursor.close()
# 	return json.dumps(dataset)

# def close_dbc(dbc):
# 	dbc.close()