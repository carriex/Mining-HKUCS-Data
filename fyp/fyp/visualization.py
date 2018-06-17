from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from mining1.models import Applicants
from django.forms.models import model_to_dict
from mining1.forms import Feature_selection_chart, Feature_selection_chart_2
import json
from collections import OrderedDict
from django.db.models import Q
import scipy.stats as stats
from mining1.logistic_regression import recommend_api
from data_preprocessing.Preprocess import clearlabel,readfeature
from .views import get_proportion,get_years_query


def applicant_chart(request):
	form = Feature_selection_chart
	filter_admission = False
	x_axis = "gpa_ug"
	y_axis = "papers"
	z_axis = "interest1"
	filter_year = '+'.join([ d['year'] for d in list(Applicants.objects.order_by('year').values('year').distinct())])
	filter_interest = "all"
	year = filter_year.replace('+', ' ')
	interest = filter_interest
	prop = get_proportion(Applicants.objects.all(),"interest1")
	if request.method == 'POST':
		form = Feature_selection_chart(request.POST)
		if form.is_valid():
			x_axis = form.cleaned_data.get('x_axis')
			y_axis = form.cleaned_data.get('y_axis')
			z_axis = form.cleaned_data.get('z_axis')
			filter_admission = form.cleaned_data.get('filter_admission')
			filter_year  = '+'.join(form.cleaned_data.get('filter_year'))
			year = filter_year.replace('+', ' ')
			filter_interest = form.cleaned_data.get('filter_interest')
			interest = filter_interest
			query = get_years_query(form.cleaned_data.get('filter_year'))
			applicants = Applicants.objects.filter(query)
			if filter_admission:
				applicants = applicants.filter(ad_result='ad')
				filter_admission = 1
			elif "ad" in z_axis and "result" not in z_axis:
				applicants=applicants.filter(ad_result='ad')
			prop = get_proportion(applicants,z_axis)
			print(prop)
	return render (request, 'chart.html',{'form':form, 'x_axis':x_axis, 'y_axis':y_axis,'z_axis':z_axis, 'filter_year':filter_year,'filter_interest':filter_interest,'filter_admission':filter_admission, 'year':year, 'interest':interest,'prop':prop})

def applicant_chart_2(request):
	form = Feature_selection_chart_2
	filter_admission = False
	x_axis = "year"
	y_axis = "apply_for"
	filter_year = '+'.join([ d['year'] for d in list(Applicants.objects.order_by('year').values('year').distinct())])
	filter_interest = "all"
	year = filter_year.replace('+', ' ')
	interest = filter_interest
	prop = get_proportion(Applicants.objects.all(),"interest1")
	if request.method == 'POST':
		form = Feature_selection_chart_2(request.POST)
		if form.is_valid():
			x_axis = form.cleaned_data.get('x_axis')
			y_axis = form.cleaned_data.get('y_axis')
			filter_admission = form.cleaned_data.get('filter_admission')
			filter_year  = '+'.join(form.cleaned_data.get('filter_year'))
			year = filter_year.replace('+', ' ')
			filter_interest = form.cleaned_data.get('filter_interest')
			interest = filter_interest
			query = get_years_query(form.cleaned_data.get('filter_year'))
			applicants = Applicants.objects.filter(query)
			if filter_admission:
				applicants = applicants.filter(ad_result='ad')
				filter_admission = 1
			elif "ad" in y_axis and "result" not in y_axis:
				applicants=applicants.filter(ad_result='ad')
			#prop = get_proportion(applicants,z_axis)
			#print(prop)
	return render (request, 'chart2.html',{'form':form, 'x_axis':x_axis, 'y_axis':y_axis, 'filter_year':filter_year,'filter_interest':filter_interest,'filter_admission':filter_admission, 'year':year, 'interest':interest})


