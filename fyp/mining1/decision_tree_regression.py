#regr_1 = tree.DecisionTreeRegressor(max_depth=3,min_samples_leaf=1, random_state=3) #random_state is seed
from django.http import HttpResponse, JsonResponse
from django import db
from django.core import serializers
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from mining1.models import Applicants
import json
import os
import hmac
import numpy as np

from sklearn import preprocessing  #encode numerical attributes - le_sex = preprocessing.LabelEncoder()
from sklearn import tree, grid_search
import sklearn
from mining1.export import export_json
from mining1.forms import Feature_selection
from data_preprocessing.Preprocess import preprocess, clearlabel 
from data_preprocessing.decision_tree import convert_feature, treeToJson




##Possible ways to increase accuracy
# Cross validation
# Maximum depth 
# Separation of training data and testing data  



@csrf_exempt
def decision_tree_r(request,year):
	years = [ d['year'] for d in list(Applicants.objects.order_by('year').values('year').distinct())]
	applicants = preprocess(Applicants.objects.all() if year =="all" else Applicants.objects.filter(year=year))
	applicants2 = preprocess(Applicants.objects.filter(ad_result='ad') if year =="all" else Applicants.objects.filter(ad_result='ad',year=year) )
	Y=[]
	X=[]
	Z=[]
	W=[]
	json_str = ""
	description = []
	year = ','.join(["20"+y[1:] for y in years]) if year =="all" else "20"+year[1:]
	if request.method == 'GET':		#data preprocessing
		for a in applicants:
			Y.append(a.ad_result)
			X.append([a.toefl, a.gpa_ug, a.papers,a.major_ug,a.qs_ug])
		class_names=['Not admitted','PhD','Mphil']
		class2_names=['No HKPF', 'HKPF']
		feature = ['TOEFL_score','Undergraduate_GPA', 'Papers', 'Undergraduate_Major','Undergraduate_QS_Ranking']
		parameters = {'max_depth': np.array([3,4,5])}
		regr =tree.DecisionTreeRegressor(max_depth=3)
		regr.fit(X,Y)
		for a in applicants2:
			W.append([int(a.toefl), a.gpa_ug, int(a.papers),int(a.major_ug),int(a.qs_ug)])
			Z.append(a.ad_hkpf)
		regr2 = tree.DecisionTreeRegressor(max_depth=3)
		regr2 = regr2.fit(W,Z)
		json_str = json.dumps(treeToJson(regr,feature,class_names))
		description.append("This is a sample Decision Tree classifier generated on the Applicaiton data of 2016.")
		description.append("The features include:" + str(feature))
		description.append("The decision tree classifies on whether the applicant is shortlisted or not.")
		form = Feature_selection
		importance = regr.feature_importances_.tolist()
		max_feature = feature[importance.index(max(importance))]
		return render(request, 'decision_tree.html', {'form':form, 'json_str':json_str, 'description': description, 'Title':"Decision Tree Regression", 'years':years, 'max_feature':max_feature,'year':year})
	elif request.method == 'POST':
		form = Feature_selection(request.POST)
		if form.is_valid():
			feature = form.cleaned_data.get('feature_names')
			print (feature)
			classes = form.cleaned_data.get('classified_on')
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
			parameters = {'max_depth': np.array([3,4,5])}	
			regr = grid_search.GridSearchCV(tree.DecisionTreeRegressor(),parameters, n_jobs=4)
			regr.fit(X,Y)
			regr = regr.best_estimator_
			tree.export_graphviz(regr, out_file = 'tree.dot')
			regr2 = tree.DecisionTreeRegressor()
			regr2.fit(W,Z)
			tree.export_graphviz(regr2, out_file = 'tree2.dot')
			description.append("This is a Decision Tree Classifier generated on the Applicaiton data of 2016.")
			description.append("The features include:" + str(feature))
			if classes[0] == '1':
				class_names=['Not Admitted','PhD','MPhil']
				json_str = json.dumps(treeToJson(regr,convert_feature(feature), class_names))
				importance = regr.feature_importances_.tolist()
				description.append("The decision tree classifies on the admission result.")
				result = regr.predict(X)
				#accuracy = str(list(np.reshape(np.asarray(np.mean(result == Y)), (1, np.size(np.mean(result == Z))))[0]))[1:-1] #numpy to string
			else:
				class_names = ['NO HKPF', 'HKPF']
				json_str = json.dumps(treeToJson(regr2,convert_feature(feature), class_names))
				importance = regr2.feature_importances_.tolist()
				description.append("The decision tree classifies on HKPF result.")
				result = regr2.predict(X)
				#accuracy = str(list(np.reshape(np.asarray(np.mean(result == Z)), (1, np.size(np.mean(result == Z))))[0]))[1:-1] #numpy to string
			max_feature = feature[importance.index(max(importance))]
			gini = str(max(importance))
			#description.append("The accuracy of the model applied on the applicants of 2016 is  " + accuracy)
			description.append("The most important attribute is " + max_feature + " with Gini importance equal to " + gini + ".")
		return render(request, 'decision_tree.html', {'form':form, 'json_str':json_str,'description': description, 'Title':"Decision Tree Regression",'years':years, 'max_feature':max_feature,'year':year})