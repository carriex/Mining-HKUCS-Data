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
import csv 

from sklearn import preprocessing  #encode numerical attributes - le_sex = preprocessing.LabelEncoder()
from sklearn import tree, grid_search
import sklearn
from mining1.export import export_json
from mining1.forms import Feature_selection
from data_preprocessing.Preprocess import preprocess 




##Possible ways to increase accuracy
# Cross validation
# Maximum depth 
# Separation of training data and testing data  

def treeToJson(decision_tree, feature_names=None, class_names=None):
  from warnings import warn
 
  js = ""
 
  def node_to_str(tree, node_id, criterion):
    if not isinstance(criterion, sklearn.tree.tree.six.string_types):
      criterion = "impurity"
 
    value = tree.value[node_id]
    if tree.n_outputs == 1:
      value = value[0, :]
    jsonValue = ', '.join([str(x) for x in value])


    jsonValue = str(list(zip(class_names, jsonValue.split(','))))
    print (jsonValue)

    if tree.children_left[node_id] == sklearn.tree._tree.TREE_LEAF:
      return '"id": "%s", "criterion": "%s", "impurity": "%s", "samples": "%s", "value": "%s"' \
             % (node_id, 
                criterion,
                tree.impurity[node_id],
                tree.n_node_samples[node_id],
                jsonValue)
    else:
      if feature_names is not None:
        feature = feature_names[tree.feature[node_id]]
      else:
        feature = tree.feature[node_id]
 
      if "=" == feature:
        ruleType = "="
        ruleValue = "false"
      else:
        ruleType = "<="
        ruleValue = "%.4f" % tree.threshold[node_id]
 
      return '"id": "%s", "name": "%s %s %s", "%s": "%s", "samples": "%s"' \
             % (node_id, 
                feature,
                ruleType,
                ruleValue,
                criterion,
                tree.impurity[node_id],
                tree.n_node_samples[node_id])
 
  def recurse(tree, node_id, criterion, parent=None, depth=0):
    tabs = "  " * depth
    js = ""
 
    left_child = tree.children_left[node_id]
    right_child = tree.children_right[node_id]
 
    js = js + "\n" + \
         tabs + "{\n" + \
         tabs + "  " + node_to_str(tree, node_id, criterion)
 
    if left_child != sklearn.tree._tree.TREE_LEAF:
      js = js + ",\n" + \
           tabs + '  "children":[ ' + \
           recurse(tree, \
                   left_child, \
                   criterion=criterion, \
                   parent=node_id, \
                   depth=depth + 1) + "\n" + \
           tabs + ',' + \
           recurse(tree, \
                   right_child, \
                   criterion=criterion, \
                   parent=node_id,
                   depth=depth + 1) + \
           tabs + ']'
    js = js + tabs + "\n" + \
         tabs + "}"
 
    return js
 
  if isinstance(decision_tree, sklearn.tree.tree.Tree):
    js = js + recurse(decision_tree, 0, criterion="impurity")
  else:
    js = js + recurse(decision_tree.tree_, 0, criterion=decision_tree.criterion)
 
  return js


#There is no selection of attribute 
@csrf_exempt
def decision_tree_c1(request,year):
	length = len(Applicants.objects.all())
	applicants = preprocess(Applicants.objects.all())[:int(length*(1/2)-1)]
	Y=[]
	X=[]
	Z=[]
	clf2 = tree.DecisionTreeClassifier(max_depth=3,min_samples_leaf=1)
	for a in applicants:
		Y.append(a.ad_result)
		X.append([a.toefl, a.gpa_ug/a.gpa_ug_scale, a.papers,a.major_ug])
		Z.append(a.ad_hkpf)
	class_names=['not admitted','phd','mphil']
	class2_names=['No HKPF', 'HKPF']
	feature_names = ['toefl','gpa_ug_scale','papers']
	parameters = {'max_depth': [3,4,5,6,7]}
	clf = grid_search.GridSearchCV(tree.DecisionTreeClassifier(),parameters, n_jobs=4)
	clf.fit(X,Y)
	clf = clf.best_estimator_
	clf2 = clf2.fit(X,Z)
	json_str = json.dumps(treeToJson(clf,feature_names, class_names))
	description = []
	description.append("This is a sample Decision Tree classifier generated on the Applicaiton data of 2016.")
	description.append("The features include:" + str(feature_names))
	description.append("The decision tree classifies on whether the applicant is admitted or not.")
	form = Feature_selection
	return render(request, 'decision_tree.html', {'json_str':json_str, 'description': description, 'Title':"Decision Tree Classification"})