from django.http import HttpResponse, JsonResponse
from django import db
from django.core import serializers
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from django.db.models import Q
from mining1.models import Applicants
import json
import os
import hmac
import numpy as np

from sklearn import preprocessing  #encode numerical attributes - le_sex = preprocessing.LabelEncoder()
from sklearn import tree, grid_search
from sklearn.ensemble import RandomForestClassifier
import sklearn
from mining1.export import export_json
from mining1.forms import Feature_selection
from fyp.views import get_feature
from data_preprocessing.Preprocess import preprocess, clearlabel
from data_preprocessing.decision_tree import convert_feature, treeToJson



##Possible ways to increase accuracy
# Cross validation
# Maximum depth 
# Separation of training data and testing data  



@csrf_exempt
def decision_tree_c(request,year):
	years = [ d['year'] for d in list(Applicants.objects.order_by('year').values('year').distinct())]
	Y=[]
	X=[]
	Z=[]
	W=[]
	P=[]
	json_str = ""
	description = []
	p_applicants = []
	if request.method == 'GET':	
		if year == "all":	
			applicants = preprocess(Applicants.objects.all())
			applicants2 = preprocess(Applicants.objects.filter(ad_result='ad'))
			selected_year = ','.join(["20"+y[1:] for y in years])
		else:
			applicants = preprocess(Applicants.objects.filter(~Q(year=year)))
			applicants2 = preprocess(Applicants.objects.filter(~Q(year=year)).filter(ad_result='ad'))
			selected_year = ','.join(["20"+y[1:] for y in years if y!=year])
		for a in applicants:
			Y.append(a.ad_result)
			X.append([a.toefl, a.gpa_ug, a.papers,a.major_ug,a.qs_ug])
		class_names=['Not admitted','PhD','Mphil']
		class2_names=['No HKPF', 'HKPF']
		feature = ['TOEFL_score','Undergraduate_GPA', 'Papers', 'Undergraduate_Major','Undergraduate_QS_Ranking']
		feature_names=['toefl','gpa_ug','papers','major_ug','qs_ug']
		parameters = {'max_depth': [3,4,5]}
		clf = grid_search.GridSearchCV(tree.DecisionTreeClassifier(),parameters, n_jobs=4)
		clf.fit(X,Y)
		clf = clf.best_estimator_
		if year !="all":
			p_applicants = preprocess(Applicants.objects.filter(year=year))
			for a in p_applicants:
				P.append([a.toefl, a.gpa_ug/a.gpa_ug_scale, a.papers,a.major_ug,a.qs_ug])
			result = list(clf.predict(P))
			p_applicants = get_feature(p_applicants,feature_names)
			for p in p_applicants:
				p['result'] = result[p_applicants.index(p)]
		for a in applicants2:
			W.append([a.toefl, a.gpa_ug/a.gpa_ug_scale, a.papers,a.major_ug,a.qs_ug])
			Z.append(a.ad_hkpf)
		clf2 = grid_search.GridSearchCV(tree.DecisionTreeClassifier(),parameters, n_jobs=4)
		clf2 = clf2.fit(W,Z)
		json_str = json.dumps(treeToJson(clf,feature,class_names))
		form = Feature_selection
		importance = clf.feature_importances_.tolist()
		feature_importance = {}
		for f in feature:
			feature_importance[f] = importance[feature.index(f)]
		sorted_feature = sorted(feature_importance, key=feature_importance.get,reverse=True) 
		max_feature = feature[importance.index(max(importance))]
		return render(request, 'decision_tree.html', {'form':form, 'json_str':json_str, 'description': description, 'Title':"Decision Tree Classification", 'years':years,'year':selected_year, 'sorted_feature':sorted_feature, 'class':'Admission', 'features':feature, 'applicants':p_applicants})
	elif request.method == 'POST':
		form = Feature_selection(request.POST)
		if form.is_valid():
			feature = form.cleaned_data.get('select_features')
			print (feature)
			classes = form.cleaned_data.get('classified_on')
			ys = form.cleaned_data.get('select_years')
			selected_year = ','.join(["20"+y[1:] for y in ys])
			applicants = []
			applicants2 = []
			for y in ys:
				applicants += preprocess(Applicants.objects.filter(year=y))
				applicants2 += preprocess(Applicants.objects.filter(ad_result='ad',year=y))
			X = []
			Y = []
			Z = []
			W = []
			for a in applicants:
				Y.append(a.ad_result)
				X.append([getattr(a,f) for f in feature])
			for a in applicants2:
				Z.append(a.ad_hkpf)
				W.append([getattr(a,f) for f in feature])
			parameters = {'max_depth': [3,4,5]}	
			clf = grid_search.GridSearchCV(tree.DecisionTreeClassifier(),parameters, n_jobs=4)
			clf.fit(X,Y)
			clf = clf.best_estimator_
			tree.export_graphviz(clf, out_file = 'tree.dot')
			clf2 = grid_search.GridSearchCV(tree.DecisionTreeClassifier(),parameters, n_jobs=4)
			clf2.fit(W,Z)
			clf2 = clf2.best_estimator_
			tree.export_graphviz(clf2, out_file = 'tree2.dot')
			description.append("This is a Decision Tree Classifier generated on the Applicaiton data of 2016.")
			description.append("The features include:" + str(feature))
			if classes[0] == '1':
				class_names=['Not Admitted','PhD','MPhil']
				json_str = json.dumps(treeToJson(clf,convert_feature(feature), class_names))
				importance = clf.feature_importances_.tolist()
				description.append("The decision tree classifies on the admission result.")
				result = clf.predict(X)
				#accuracy = str(list(np.reshape(np.asarray(np.mean(result == Y)), (1, np.size(np.mean(result == Z))))[0]))[1:-1] #numpy to string
			else:
				class_names = ['NO HKPF', 'HKPF']
				json_str = json.dumps(treeToJson(clf2,convert_feature(feature), class_names))
				importance = clf2.feature_importances_.tolist()
				description.append("The decision tree classifies on HKPF result.")
				result = clf2.predict(X)
				#accuracy = str(list(np.reshape(np.asarray(np.mean(result == Z)), (1, np.size(np.mean(result == Z))))[0]))[1:-1] #numpy to string
			feature_importance = {}
			for f in feature:
				feature_importance[f] = importance[feature.index(f)]
			print (feature_importance)
			sorted_feature = sorted(feature_importance, key=feature_importance.get,reverse=True) 
			print (sorted_feature)
			max_feature = feature[importance.index(max(importance))]
			gini = str(max(importance))
			#description.append("The accuracy of the model applied on the applicants of 2016 is  " + accuracy)
			description.append("The most important attribute is " + max_feature + " with Gini importance equal to " + gini + ".")
		return render(request, 'decision_tree.html', {'form':form, 'json_str':json_str,'description': description, 'Title':"Decision Tree Classification",'years':years, 'sorted_feature':sorted_feature,'year':selected_year})