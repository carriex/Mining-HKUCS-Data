from django.http import HttpResponse, JsonResponse
from django import db
from django.core import serializers
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from mining1.models import Applicants2016
import json
import os
import hmac

from sklearn.datasets import load_iris
from sklearn import tree, preprocessing  #encode numerical attributes - le_sex = preprocessing.LabelEncoder()
import pydotplus
from IPython.display import Image

# Create your views here.


#STUDENT: listing all the students data
@csrf_exempt
def applicant_list(request):
	if request.method == 'GET':
		applicants = Applicants2016.objects.all()
		applicants_data = serializers.serialize("json", applicants)
		return HttpResponse(applicants_data)
	elif request.method == 'POST':
		return _error_response(request, "POST not allowed")

#STUDENT: used to retrieve individual student data.
@csrf_exempt
def applicant_detail(request, pk):
	try:
		pk = pk + "\r"
		applicant = Applicants2016.objects.get(pk=pk)
	except Applicants2016.DoesNotExist:
		return _error_response(request, "applicant DoesNotExist")
	if request.method == 'GET':
		#Method 0: return a dictionary
		# return _success_response(request, {'pk': applicant.pk, 'gpa_ug': user.gpa_ug})
		#Method 1: a serialized json
		# applicant_data = serializers.serialize("json", [applicant,]) 
		# return HttpResponse(applicant_data)
		#Method 2: return a dict
		applicant_data = model_to_dict(applicant)
		# return JsonResponse(applicant_data, safe=False)
		return _success_response(request, applicant_data)
	elif request.method == 'POST':   
		return _error_response(request, "POST not allowed")

@csrf_exempt
def graph(request):
	if request.method == 'GET':
		length = len(Applicants2016.objects.all())
		applicants = Applicants2016.objects.all()[:(length/2-1)]
		clf = tree.DecisionTreeClassifier(max_depth=3,min_samples_leaf=1)
		clf2 = tree.DecisionTreeClassifier(max_depth=3,min_samples_leaf=1)
		Y=[]
		X=[]
		Z=[]
		for a in applicants:
			if a.apply_for == "mphil":
				Y.append("0")
			elif a.apply_for == "phd":
				Y.append("1")
			else:
				Y.append("2")
			Z.append(a.shortlisted)
			X.append([a.toefl, a.gpa_ug/a.gpa_ug_scale, a.papers])
			if a.major_ug == 'CS':
				X[-1].append("1")
			else:
				X[-1].append("0")
		feature_names = ['toefl','gpa_ug_scale','papers','major_ug']
		class_names=['mphil','phd','either']
		class2_names=['not shortlisted', 'shortlisted']
		clf = clf.fit(X, Y)
		clf2 = clf2.fit(X,Z)
		f = tree.export_graphviz(clf, out_file=None, feature_names=feature_names, class_names=class_names, filled =True, rounded = True, special_characters = True)
		f2 = tree.export_graphviz(clf2, out_file=None, feature_names=feature_names, class_names=class2_names, filled =True, rounded = True, special_characters = True)
		graph = pydotplus.graph_from_dot_data(f)
		graph2 = pydotplus.graph_from_dot_data(f2)
		current_dir= os.path.dirname(os.path.abspath(__file__))
		static = os.path.join(current_dir,'static', 'mining1')
		graph.write_png(os.path.join(static, "tree.png"))
		graph2.write_png(os.path.join(static, "tree2.png"))		
		#image_data1=open('tree.png',"rb").read()
		#image_data2=open('tree2.png',"rb").read()
		html = "<p style='text-align:center;'>Decision Tree for program</p><img src='/static/mining1/tree.png'><p style='text-align:center;'>Decision Tree for shortlisted interview</p><img src='/static/mining1/tree2.png'>"

		applicants2 = Applicants2016.objects.all()[(length/2):length]
		Y=[]
		X=[]
		Z=[]
		for a in applicants2:
			if a.apply_for == "mphil":
				Y.append("0")
			elif a.apply_for == "phd":
				Y.append("1")
			else:
				Y.append("2")
			Z.append(a.shortlisted)
			X.append([a.toefl, a.gpa_ug/a.gpa_ug_scale, a.papers])
			if a.major_ug == 'CS':
				X[-1].append("1")
			else:
				X[-1].append("0")
		result = clf2.predict(X)
		i=0
		accuracy = 0
		for r in result:
			if r == Z[i]:
				accuracy=accuracy+1
			i=i+1
		print (accuracy/i)

		#return HttpResponse(image_data1,content_type="image/png")
		return HttpResponse(html)
	elif request.method == 'POST':
		return _error_response(request, "POST not allowed")


def _error_response(request, error_msg):
	return JsonResponse({'work': False, 'msg': error_msg}, safe=False)

def _success_response(request, resp=None):
	if resp:
		return JsonResponse({'work': True, 'resp': resp}, safe=False)
	else:
		return JsonResponse({'work': True})