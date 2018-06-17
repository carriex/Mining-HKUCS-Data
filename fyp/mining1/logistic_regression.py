from django.http import HttpResponse, JsonResponse
from django import db
from django.core import serializers
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
import json
import os
import hmac
import numpy
from mining1.forms import Feature_selection_logistic, Feature_selection_logistic_2
from mining1.models import Applicants
# from mining1.forms import Feature_selection

import sklearn
from sklearn import metrics
from sklearn.linear_model import LogisticRegression


@csrf_exempt
def get_features():	
	features = ['apply_phd', 'apply_mph', 'qs_ug', \
				'major_cs', 'attend_pg', 'papers', \
				'norm_gpa_ug']
	return features

@csrf_exempt
def get_statistics(applicants):
	total_num = len(applicants)
	ad_num = 0
	for index, a in enumerate(applicants):
		if a.ad_result == 'ad':
			ad_num += 1

	return total_num, ad_num


@csrf_exempt
def preprocess(applicants):	
	target_data = []
	features = get_features()
	data = []
	present_data = []
	multi = False
	ids = []
	for index, a in enumerate(applicants):

		ids.append(a.idnum)

		if multi == True:
			target_data.append(a.ad_result)
		else:
			# change 333
			if a.ad_result == 'rej' or a.ad_result == 'NA':
				target_data.append('reject')
			else:
				target_data.append('admit')
		
		d = []
		pd = []
		if a.apply_for == 'phd':
			d.append(1)
			d.append(0)
			pd.append('phd')
			pd.append('-')
		elif a.apply_for == 'mphil':
			d.append(0)
			d.append(1)
			pd.append('-')
			pd.append('mphil')
		else:
			d.append(1)
			d.append(1)
			pd.append('phd')
			pd.append('mphil')
		d.append(a.qs_ug)
		pd.append(a.qs_ug)
		if a.major_ug == 'CS':
			d.append(1)
			pd.append('CS')
		else:
			d.append(0)
			pd.append('others')
		if a.university_pg != 'NI':
			d.append(1)
			pd.append(a.university_pg)
		else:
			d.append(0)
			pd.append('-')
		d.append(a.papers)
		pd.append(a.papers)
		d.append(a.norm_gpa_ug)
		pd.append(a.norm_gpa_ug)
		
		data.append(d)
		present_data.append(pd)
	return data, target_data, ids, present_data

@csrf_exempt
def recommend_api(year, idnum = None):

	# year should be in the format of Y16 or Y15
# @csrf_exempt
# def recommend_api(request, year = None, idnum = None):	
# 	year = 2015
# 	idnum = "Y15A01"

	if year == "Y15":
		train_year = "Y16"
	else:
		train_year = "Y" + str((int(year[-2:]) - 1) % 2000)

	# if int(year) == 2015:
	# 	train_year = "Y16"	
	# else:
	# 	train_year = "Y" + str((int(year) - 1) % 2000)
	
	train_applicants = Applicants.objects.filter(year=train_year)
	
	test_year = year
	test_applicants = Applicants.objects.filter(year=test_year)
	
	train_data, train_target, train_ids, train_p_data = preprocess(train_applicants)
	test_data, test_target, test_ids, test_p_data = preprocess(test_applicants)
	
	model = LogisticRegression()
	model.fit(train_data, train_target)
	test_proba = model.predict_proba(test_data)
	test_proba = [p[0] for p in test_proba]

	train_total_num, train_ad_num = get_statistics(train_applicants)
	test_total_num, test_ad_num = get_statistics(test_applicants)
	recommend_num = int(test_total_num * train_ad_num / train_total_num)
	recommend_index = list(reversed(numpy.argsort(test_proba)[-recommend_num:]))
	recommend_list = [test_ids[i] for i in recommend_index]
	
	# print("test_proba:", test_proba)
	# print("1:", test_proba[77], test_ids[77])
	# print("2:", test_proba[82], test_ids[82])
	# print("3:", test_proba[1], test_ids[1])
	# print("recommend_index:", recommend_index)
	# print("test_ids:", test_ids)
	# print("test_total_num:", test_total_num)

	rank = 0
	percentage = 0
	if idnum is not None:
		index = test_ids.index(idnum)
		proba = test_proba[index]
		rank = 1
		for p in test_proba:
			if proba < p:
				rank += 1
		percentage = round(rank / test_total_num, 3)

	description = []
	description.append("Testing year is " + test_year + ".")
	description.append("Testing year has " + str(test_total_num) + " applicants.")
	description.append("Training model is using " + train_year + " applicants data, " + \
				  str(train_total_num) + " total applicants and " + str(train_ad_num) + " admitted.")
	description.append("The model suggests " + str(recommend_num) + " applicants to be admitted.")
	description.append("The model suggests " + str(idnum) + " ranks " + str(rank) + " (" + str(percentage) + ") among the applicants.")
	
	# return render(request, 'logistic.html', {'recommend_list': recommend_list, 'rank': rank,'percentage': percentage, 'description': description})

	return {'recommend_list': recommend_list, 'rank': rank,'percentage': percentage, 'description': description}




@csrf_exempt
def logistic(request):
	if request.method == 'GET':
		form = Feature_selection_logistic_2(initial={'train_year': 'Y15', 'test_year': 'Y16'})

		features = get_features()
		train_applicants = Applicants.objects.filter(year="Y15")

		train_data, train_target, train_ids, train_p_data = preprocess(train_applicants)
		
		model = LogisticRegression()
		model.fit(train_data, train_target)	
		

		cof = model.coef_.tolist()
		inf = model.intercept_
		for i, cc in enumerate(cof):
			cc[:] = [round(c, 3) for c in cc]
			cc.append(round(inf[i], 3))
			if len(model.classes_) > 2:
				cc.insert(0, model.classes_[i])
			else:
				cc.insert(0, model.classes_[1])

		
		params = model.get_params()
		classes = ''

		# print("333 model:", model)
		# print("333 cof:", cof)
		# print("333 inf:", inf)
		
		# print("333 classes:", model.classes_)
		# print("333 classes[1]:", model.classes_[1])

		# test data
		test_applicants = Applicants.objects.filter(year="Y16")
		test_data, test_target, test_ids, test_p_data = preprocess(test_applicants)
		# make predictions
		test_predict = model.predict(test_data)

		test_score = model.score(test_data, test_target)
		# Returns the coefficient of determination (R^2). 
		# A measure of how well observed outcomes are replicated by the model, 
		# as the proportion of total variation of outcomes explained by the model. 
		
		test_decision = model.decision_function(test_data)
		test_proba = model.predict_proba(test_data)
		
		# print("333 test_data:", test_data[:5])
		# print("333 test_target:", test_target[:5])

		# print("333 test_predict:", test_predict[:5])
		# print("333 test_proba:", test_proba[:5])
		
		# print("333 test_decision:", test_decision[:5])


		ad_proba = [p[0] for p in test_proba]
		indices = list(range(len(ad_proba)))
		indices.sort(key=lambda x: ad_proba[x])
		rank = [0] * len(indices)
		num = len(ad_proba)
		for i, x in enumerate(indices):
		    rank[x] = num - i

		rec = recommend_api("Y16")

		for i, a in enumerate(test_p_data):
			a.insert(0, round(ad_proba[i], 3))
			a.insert(0, rank[i])
			if (rank[i] <= len(rec['recommend_list'])):
				a.insert(0, 'admit')
			else:
				a.insert(0, 'reject')
			a.insert(0, test_ids[i])

		# summarize the fit of the model
		# print(metrics.classification_report(test_target, test_predict))
		# print(metrics.confusion_matrix(test_target, test_predict))

		

		return render(request, 'logistic.html', \
			   {'form': form, 'features': features, 'cof': cof, 'inf': inf, \
			   'recommend_list': rec['recommend_list'], 'rank': rec['rank'],\
			   'percentage': rec['percentage'], 'description': rec['description'], \
			   'dataset': test_p_data})
	elif request.method == 'POST':
		form = Feature_selection_logistic_2(request.POST)
		if form.is_valid():
			train_year = form.cleaned_data.get('train_year')
			test_year = form.cleaned_data.get('test_year')
			target = form.cleaned_data.get('target')

			# print("train_year:", train_year)
			# print("test_year:", test_year)
		else:
			return render(request, 'logistic.html', {'form': form})

		# test_year = year[0]
		# if test_year == "Y15":
		# 	train_year = "Y16"
		# else:
		# 	train_year = "Y" + str((int(test_year[-2:]) - 1) % 2000)

		features = get_features()
		train_applicants = Applicants.objects.filter(year=train_year)

		train_data, train_target, train_ids, train_p_data = preprocess(train_applicants)
		# print(train_data[:5])
		# print(train_target[:5])
		model = LogisticRegression()
		model.fit(train_data, train_target)	
		# print(model)

		cof = model.coef_.tolist()
		inf = model.intercept_
		for i, cc in enumerate(cof):
			cc[:] = [round(c, 3) for c in cc]
			cc.append(round(inf[i], 3))
			if len(model.classes_) > 2:
				cc.insert(0, model.classes_[i])
			else:
				cc.insert(0, model.classes_[1])

		
		params = model.get_params()
		# print("classes_:", model.classes_)
		# print("cof:", cof)
		# print("inf:", inf)
		# print("params:", params)

		# test data
		# if len(year) > 1:
		# 	test_applicants = Applicants.objects.filter(Q(year="Y15") | Q(year="Y16"))
		# else:
		# 	test_applicants = Applicants.objects.filter(year=test_year)
		test_applicants = Applicants.objects.filter(year=test_year)
		test_data, test_target, test_ids, test_p_data = preprocess(test_applicants)
		# make predictions
		test_predict = model.predict(test_data)

		test_score = model.score(test_data, test_target)
		test_proba = model.predict_proba(test_data)
		
		ad_proba = [p[0] for p in test_proba]
		indices = list(range(len(ad_proba)))
		indices.sort(key=lambda x: ad_proba[x])
		rank = [0] * len(indices)
		num = len(ad_proba)
		for i, x in enumerate(indices):
		    rank[x] = num - i

		rec = recommend_api(test_year)

		for i, a in enumerate(test_p_data):
			a.insert(0, round(ad_proba[i], 3))
			a.insert(0, rank[i])
			if (rank[i] <= len(rec['recommend_list'])):
				a.insert(0, 'admit')
			else:
				a.insert(0, 'reject')
			a.insert(0, test_ids[i])

		
		return render(request, 'logistic.html', \
			   {'form': form, 'features': features, 'cof': cof, 'inf': inf, \
			   'recommend_list': rec['recommend_list'], 'rank': rec['rank'],\
			   'percentage': rec['percentage'], 'description': rec['description'], \
			   'dataset': test_p_data})




'''
cof: [[  1.71721715e-01  -1.11445865e+00  -7.17835340e-04  -2.15400931e-01
   -6.40236104e-01  -1.54634888e-01  -4.95398403e-01]
 [ -1.71234450e-01  -6.32508223e-01  -1.59203259e-03  -4.67718547e-01
    2.26538327e-01  -6.62408099e-01  -1.37041438e+00]
 [ -2.75147816e-01   1.14450427e+00   3.36980913e-04   2.13867456e-01
    5.01226407e-01   2.53541985e-01   5.09822738e-01]]
inf: [-0.97949878 -1.56978337  1.01755081]
test_target: ['rej', 'ad', 'rej', 'rej', 'rej']
test_predict: ['rej' 'rej' 'rej' 'rej' 'rej']

             precision    recall  f1-score   support

         ad       0.00      0.00      0.00        26
    decline       0.00      0.00      0.00         2
        rej       0.83      1.00      0.91       169
  terminate       0.00      0.00      0.00         1
   waitlist       0.00      0.00      0.00         5

avg / total       0.69      0.83      0.76       203

[[  0   0  26   0   0]
 [  0   0   2   0   0]
 [  0   0 169   0   0]
 [  0   0   1   0   0]
 [  0   0   5   0   0]]
'''


@csrf_exempt
def prediction_preprocess(applicants):	
	target_data = []
	features = get_features()
	data = []
	present_data = []
	multi = False
	ids = []

	groups = []
	for index, a in enumerate(applicants):

		if "DB/SE" in a.interest1 or "DB" in a.interest1 or "SE" in a.interest1:
			groups.append("Data and Software Engineering")
		elif "VG" in a.interest1:
			groups.append("HCI, Graphics and Computer Vision")
		elif "ST/NW" in a.interest1 or "ST" in a.interest1 or "NW" in a.interest1:
			groups.append("Systems and Networking")
		elif "BIO/ALG" in a.interest1 or "BI" in a.interest1 or "AL" in a.interest1:
			groups.append("Algorithms and Bioinformatics")
		else:
			groups.append("Information Security and Forensics")

		ids.append(a.idnum)

		if multi == True:
			target_data.append(a.ad_result)
		else:
			# change 333
			if a.ad_result == 'rej' or a.ad_result == 'NA':
				target_data.append('reject')
			else:
				target_data.append('admit')
		
		d = []
		pd = []
		if a.apply_for == 'phd':
			d.append(1)
			d.append(0)
			pd.append('phd')
			pd.append('-')
		elif a.apply_for == 'mphil':
			d.append(0)
			d.append(1)
			pd.append('-')
			pd.append('mphil')
		else:
			d.append(1)
			d.append(1)
			pd.append('phd')
			pd.append('mphil')
		d.append(a.qs_ug)
		pd.append(a.qs_ug)
		if a.major_ug == 'CS':
			d.append(1)
			pd.append('CS')
		else:
			d.append(0)
			pd.append('others')
		if a.university_pg != 'NI':
			d.append(1)
			pd.append(a.university_pg)
		else:
			d.append(0)
			pd.append('-')
		d.append(a.papers)
		pd.append(a.papers)
		d.append(a.norm_gpa_ug)
		pd.append(a.norm_gpa_ug)
		
		data.append(d)
		present_data.append(pd)
	return data, target_data, ids, present_data, groups


@csrf_exempt
def prediction(request):
	# should process applicant data interest field, and filter each Group applicants
	# build group-based classifer using specific applicant data
	features = get_features()

	train_applicants = Applicants.objects.filter(Q(year="Y15") | Q(year="Y16"))
	
	train_data, train_target, train_ids, train_p_data, train_groups = prediction_preprocess(train_applicants)
		
	model = LogisticRegression()
	model.fit(train_data, train_target)	

	# test data
	test_applicants = Applicants.objects.filter(year="Y17")
	test_data, test_target, test_ids, test_p_data, test_groups = prediction_preprocess(test_applicants)
	# make predictions
	test_predict = model.predict(test_data)
	test_proba = model.predict_proba(test_data)

	ad_proba = [p[0] for p in test_proba]
	indices = list(range(len(ad_proba)))
	indices.sort(key=lambda x: ad_proba[x])
	rank = [0] * len(indices)
	num = len(ad_proba)
	for i, x in enumerate(indices):
	    rank[x] = num - i

	for i, a in enumerate(test_p_data):
		a.insert(0, round(ad_proba[i], 3))
		a.insert(0, rank[i])
		a.insert(0, test_groups[i])
		a.insert(0, test_ids[i])
	
	p_DSE_data = []
	p_GCV_data = []
	p_ISF_data = []
	p_SN_data = []
	p_AB_data = []
	for i, a in enumerate(test_p_data):
		if a[1] == "Data and Software Engineering":
			p_DSE_data.append(a)
		elif a[1] == "HCI, Graphics and Computer Vision":
			p_GCV_data.append(a)
		elif a[1] == "Information Security and Forensics":
			p_ISF_data.append(a)
		elif a[1] == "Systems and Networking":
			p_SN_data.append(a)
		elif a[1] == "Algorithms and Bioinformatics":
			p_AB_data.append(a)

	p_AB_data.sort(key=lambda x: x[2])
	p_AB_data = p_AB_data[:5]

	p_DSE_data.sort(key=lambda x: x[2])
	p_DSE_data = p_DSE_data[:5]

	p_GCV_data.sort(key=lambda x: x[2])
	p_GCV_data = p_GCV_data[:5]

	p_ISF_data.sort(key=lambda x: x[2])
	p_ISF_data = p_ISF_data[:5]

	p_SN_data.sort(key=lambda x: x[2])
	p_SN_data = p_SN_data[:5]

	# Data and Software Engineering
	DSE_pro = "Professor D.W.L. Cheung, \
	Dr. R.C.K. Cheng, \
	Professor B.C.M. Kao, \
	Professor N. Mamoulis"

	# HCI, Graphics and Computer Vision
	GCV_pro = "Professor W. Wang, \
	Dr. K.P. Chan, \
	Dr. L.Y. Wei, \
	Dr. K.K.Y. Wong, \
	Professor Y.Z. Yu"

	# Information Security and Forensics
	ISF_pro = "Dr. K.P. Chow, \
	Dr. L.C.K. Hui"

	# Systems and Networking
	SN_pro = "Professor F.C.M. Lau, \
	Professor C.L. Wang, \
	Dr. H. Cui, \
	Dr. C.Wu"

	# Algorithms and Bioinformatics
	AB_pro = "Professor T.W. Lam, \
	Dr. H.T.H. Chan, \
	Dr. G. Chiribella, \
	Dr. Z. Huang, \
	Dr. B. Oliveira, \
	Dr. H.F. Ting, \
	Dr. S.M. Yiu"
	return render(request, 'prediction.html', \
			   {'features': features, 'dataset': test_p_data, \
			   'p_AB_data': p_AB_data, 'AB_pro': AB_pro, \
			   'p_DSE_data': p_DSE_data, 'DSE_pro': DSE_pro, \
			   'p_GCV_data': p_GCV_data, 'GCV_pro': GCV_pro, \
			   'p_ISF_data': p_ISF_data, 'ISF_pro': ISF_pro, \
			   'p_SN_data': p_SN_data, 'SN_pro': SN_pro \
			   })
	return render(request, 'prediction.html', {})


