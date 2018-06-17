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

#Term frequency times Inverse Document Frequency 
import pydotplus

from sklearn.feature_extraction.text import CountVectorizer,TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from IPython.display import Image
from mining1.forms import Applicant_selection
from data_preprocessing.Preprocess import preprocess 



@csrf_exempt
def text_mining_1(request):
	length = len(Applicants.objects.all())
	applicants = preprocess(Applicants.objects.all())[:int(length*(1/2)-1)]
	Y=[]
	X=[]
	Z=[]
	for a in applicants:
		if a.tc !='':
			Y.append(a.apply_for)
			Z.append(a.shortlisted)
			X.append(a.tc)
	class_names=['mphil','phd','either']
	class2_names=['not shortlisted', 'shortlisted']
	count_vect = CountVectorizer()
	X_train_counts = count_vect.fit_transform(X)
	tfidf_transformer = TfidfTransformer()
	X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
	clf=MultinomialNB().fit(X_train_tfidf, Y)
	if request.method == 'GET':
		form = Applicant_selection	
		applicants2 = preprocess(Applicants.objects.all()[(length/2):length])
		Y=[]
		X=[]
		Z=[]
		for a in applicants2:
			if a.tc !='':
				Y.append(a.apply_for)
				Z.append(a.shortlisted)
				X.append(a.tc)
		X_new_counts = count_vect.transform(X)
		X_new_tfidf = tfidf_transformer.transform(X_new_counts)
		result = clf.predict(X_new_tfidf)
		result = result.astype(np.int)
		accuracy = str(list(np.reshape(np.asarray(np.mean(result == Y)), (1, np.size(np.mean(result == Y))))[0]))[1:-1] #numpy to string
		description="Result for program type prediction:"+accuracy
		return render(request,'text_mining.html', {'description':description, 'form': form})
	elif request.method == 'POST':
		form = Applicant_selection(request.POST)
		description = "There is some error."
		if form.is_valid():
			pk = form.cleaned_data.get('applicant')
			applicant = Applicants.objects.filter(reference_no=pk+'\r')[0]
			X=[]
			Z=[]
			Y=[]
			X.append(applicant.tc)
			Y.append(a.apply_for)
			Z.append(applicant.shortlisted)
			X_new_counts = count_vect.transform(X)
			X_new_tfidf = tfidf_transformer.transform(X_new_counts)
			result = clf.predict(X_new_tfidf)
			result = result.astype(np.int)
			description = "The predicted result for this applicant is: " + class_names[result[0]]
		return render(request,'text_mining.html', {'description':description, 'form': form, 'a':applicant, 'reference_no': applicant.reference_no.replace('\r','')})