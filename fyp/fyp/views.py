from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from mining1.models import Applicants2016, Applicants
from django.forms.models import model_to_dict
from mining1.forms import Applicant_filter
import json
from collections import OrderedDict
from django.db.models import Q
import scipy.stats as stats
from mining1.logistic_regression import recommend_api
from data_preprocessing.Preprocess import clearlabel

def weight_tree(request):
	Ordered_statistics = [{'items_base': ['no-QSRanking'], 'items_add': ['papers bad'], 'confidence': 0.6307692307692307, 'lift': 0.783023872679045}, \
						  {'items_base': ['papers bad'], 'items_add': ['no-QSRanking'], 'confidence': 0.2827586206896552, 'lift': 0.7830238726790452} \
						  ]
	itemset = ['no-QSRanking', 'papers bad']
	Support = 0.2
	
	Ordered_statistics2 = [{'items_base': ['2no-QSRanking'], 'items_add': ['2papers bad'], 'confidence': 0.6307692307692307, 'lift': 0.783023872679045}, \
						   {'items_base': ['2papers bad'], 'items_add': ['2no-QSRanking'], 'confidence': 0.2827586206896552, 'lift': 0.7830238726790452} \
						  ]
	itemset2 = ['2no-QSRanking', '2papers bad']
	Support2 = 0.8

	results = [{'itemset': itemset, 'Support': Support, 'items_base': ['no-QSRanking'], 'items_add': ['papers bad'], 'confidence': 0.6307692307692307, 'lift': 0.783023872679045}, \
			   {'itemset': itemset, 'Support': Support, 'items_base': ['papers bad'], 'items_add': ['no-QSRanking'], 'confidence': 0.2827586206896552, 'lift': 0.7830238726790452}, \
			   {'itemset': itemset2, 'Support': Support2, 'items_base': ['2no-QSRanking'], 'items_add': ['2papers bad'], 'confidence': 0.6307692307692307, 'lift': 0.783023872679045}, \
			   {'itemset': itemset2, 'Support': Support2, 'items_base': ['2papers bad'], 'items_add': ['2no-QSRanking'], 'confidence': 0.2827586206896552, 'lift': 0.7830238726790452}]
	json_str = json.dumps(results)
	return render (request, 'WeightedtreeTest.html', {'results': json_str})


def get_test(tests):
	tests = tests.split(":")
	tests = zip (tests, tests[1:])
	r = {}
	for (a,b) in tests:
		a = a.split(" ")
		b = b.split (" ")
		name =''
		if len(a)>1 and a[1]!='':
			name = a[1]
		elif len(a)==1 and a[0]!='':
			name = a[0]
		if name !='':
			if len(b) == 3:
				r[name] =b[1]
			elif len(b) == 2:
				r[name] = b[0] if b[0]!='' else "N/A"
	r = OrderedDict(sorted(r.items(),key=lambda x:x[1]))
	return r

def get_comment(comments):
	comments = [y for y in comments.split("(") if y!='']
	c = {}
	for comment in comments:
		comment = comment.split(")")
		if len(comment) >1:
			c[comment[0]] = comment[1]
	return c

def get_percentile(applicant):
	applicants = Applicants.objects.filter(year=applicant['year'])
	UGPAs = []
	PGPAs = []
	URankings = []
	PRankings = []
	Papers = []
	for a in applicants:
		if a.gpa_ug !="NI":
			UGPAs.append(a.gpa_ug/a.gpa_ug_scale)
		if a.gpa_pg !="NI":
			PGPAs.append(a.gpa_pg/a.gpa_pg_scale)
		if a.qs_on_ug:
			URankings.append(a.qs_ug)
		if a.qs_on_pg:
			PRankings.append(a.qs_pg)
		if a.papers !="NI":
			Papers.append(a.papers)
	p = {}
	p["gpa_ug"] = int(stats.percentileofscore(UGPAs,applicant["gpa_ug"]/applicant["gpa_ug_scale"]))
	p["qs_ug"] = 100 - int(stats.percentileofscore(URankings,applicant["qs_ug"]))
	p["papers"] = int(stats.percentileofscore(Papers, applicant["papers"]))
	p["qs_pg"] = 100 - int(stats.percentileofscore(PRankings,applicant["qs_pg"]))
	p["gpa_pg"] = int(stats.percentileofscore(PGPAs,applicant["gpa_pg"]/applicant["gpa_pg_scale"]))
	for s in ["gpa_ug","qs_ug","papers","gpa_pg","qs_pg"]:
		if p[s] > 75:
			p[s+"_state"] = "success"
		elif p[s] > 50:
			p[s+"_state"] = "warning"
		else:
			p[s+"_state"] = "danger"
	return p

def get_feature(applicants,features):
	applicant_list = []
	for a in applicants:
		a1 = {'idnum':a.idnum}
		for f in features:
			a1[f]=model_to_dict(a)[f]
		applicant_list.append(a1)
	return applicant_list

def get_proportion(applicants,feature):
	prop = {}
	feature_name = [ a[feature] for a in applicants.order_by(feature).values(feature).distinct()]
	features=[getattr(a,feature) for a in applicants]
	for f in feature_name:
		prop[f]=features.count(f)
	return prop 

def get_years_query(list):
	queries = [Q(year=l) for l in list]
	query = queries.pop()
	for item in queries:
		query |= item
	return query

def index(request,year=None):
	if year == "all" or year is None:
		applicants = Applicants.objects.all()
		year = "all"
	else:
		applicants = Applicants.objects.filter(year=year)
	interest = {}
	phd = {}
	mphil = {}
	phds = {}
	results = [d['ad_result'] for d in list(Applicants.objects.order_by('ad_result').values('ad_result').distinct())]
	interest1 = [a.interest1.replace('/', 'or') for a in applicants]
	years = [ d['year'] for d in list(Applicants.objects.order_by('year').values('year').distinct())]
	for a in applicants:
		a.interest1=a.interest1.replace('/', 'or')
	for i in interest1:
		if i not in interest.keys():
			interest[i]=interest1.count(i)
	for y in years:
		prog = [a.apply_for for a in Applicants.objects.all() if a.year ==y]
		phd[y] = prog.count('phd')
		mphil[y] = prog.count('mphil')
	for r in results:
		prog = [a.apply_for for a in Applicants.objects.all() if a.ad_result == r]
		phds[r] = int((prog.count('phd')/sum(phd.values()))*100)
	status = [a.status for a in applicants]
	hkpf=len(applicants.filter(ad_hkpf=1))
	result = [a.ad_result for a in applicants]
	admitted = result.count('ad')
	ps = len(applicants.filter(apply_for='phd'))

	return render (request, 'index.html', {'interest': interest, 'mphil':mphil, 'phd':phd,'phds':phds, 'ps':ps, 'count':len(applicants), 'hkpf': hkpf, 'admitted':admitted, 'years':years, 'year':year})



def applicant_list(request):
	features = ["year", "apply_for", "qs_ug", "gpa_ug","interest1"]
	form = Applicant_filter
	applicants = Applicants.objects.all()
	filter_year = "All"
	filter_interest = "All"
	filter_admission = "No"
	filter_hkpf = "No"
	filter_application_program_type = "All"
	filter_admitted_program_type = "All"
	if request.method == 'POST':
		form = Applicant_filter(request.POST)
		if form.is_valid():
			filter_year = form.cleaned_data.get('filter_year')
			filter_interest = form.cleaned_data.get('filter_interest')
			filter_admission = form.cleaned_data.get('filter_admission')
			filter_hkpf = form.cleaned_data.get('filter_hkpf')
			filter_application_program_type = form.cleaned_data.get('filter_application_program_type')
			filter_admitted_program_type = form.cleaned_data.get('filter_admitted_program_type')
			query = get_years_query(filter_year)
			applicants = Applicants.objects.filter(query)
			if filter_admission == True: 
				applicants = applicants.filter(ad_result="ad")
				print ("filter admission")
			if filter_hkpf == True:
				applicants = applicants.filter(ad_hkpf=1)
			if filter_interest != 'all':
				print (filter_interest)
				applicants = applicants.filter(interest1=filter_interest)
			if filter_application_program_type != 'all':
				applicants = applicants.filter(apply_for=filter_application_program_type)
			if filter_admitted_program_type != 'all':
				applicants = applicants.filter(ad_result='ad').filter(ad_degree=filter_admitted_program_type)
			filter_year = '+'.join(filter_year)
			print (applicants)
	applicants = get_feature(applicants,features)
	return render (request, 'table.html', {'applicants':applicants, 'features':features, 'form':form, 
		'filter_year':filter_year, 
		'filter_interest':filter_interest,
		'filter_admission':filter_admission, 
		'filter_hkpf':filter_hkpf, 
		'filter_application_program_type':filter_application_program_type, 
		"filter_admitted_program_type":filter_admitted_program_type})

def applicant_list1(request,id,year,param=None):
	features = ["year", "apply_for", "qs_ug", "gpa_ug","interest1","papers"]
	form = Applicant_filter
	filter_year = "All"
	filter_interest = "All"
	filter_admission = "No"
	filter_hkpf = "No"
	filter_application_program_type = "All"
	filter_admitted_program_type = "All"
	if id == "group":
		group = param.replace('or','/')
		if year == "all":
			applicants = get_feature(Applicants.objects.filter(interest1=group).order_by('status', 'apply_for'),features)
		else:
			filter_year = year
			years = year.split("+")
			query = get_years_query(years)
			applicants = Applicants.objects.filter(query)
			applicants = get_feature(applicants.filter(interest1=group).order_by('status', 'apply_for'),features)
		for a in applicants:
			a['interest1'] = a['interest1'].replace('/', 'or')
	elif id == "prog":
		applicants = get_feature(Applicants.objects.all().filter(apply_for="phd").order_by('status'),features)
		filter_application_program_type = "PhD"
		for a in applicants:
			a['interest1'] = a['interest1'].replace('/', 'or')
	elif id == 'hkpf':
		filter_hkpf = "Yes"
		applicants = get_feature(Applicants.objects.all().filter(ad_hkpf=1),features)
		for a in applicants:
			a['interest1'] = a['interest1'].replace('/', 'or')
	elif id == "ad":
		filter_admission = "Yes"
		applicants = get_feature(Applicants.objects.all().filter(ad_result="ad"),features)
		for a in applicants:
			a['interest1'] = a['interest1'].replace('/', 'or')
	return render (request, 'table.html', {'applicants':applicants, 'features':features, 'form':form, 
		'filter_year':filter_year, 
		'filter_interest':filter_interest,
		'filter_admission':filter_admission, 
		'filter_hkpf':filter_hkpf, 
		'filter_application_program_type':filter_application_program_type, 
		"filter_admitted_program_type":filter_admitted_program_type})



def applicant_detail(request, pk):
	applicant = model_to_dict(Applicants.objects.filter(idnum=pk)[0])
	if applicant['apply_for'] == 'either':
		applicant['apply_for'] = 'PhD/MPhil'
	if applicant['interest3'] == 'NI':
		applicant['interest3'] = 'N/A'
	percentile = get_percentile(applicant)
	applicant['year'] = applicant['year'].replace("Y", "20")
	results = get_test(applicant['english_tests'])
	comments = get_comment(applicant['toc'])
	#clearlabel(applicant)
	return render (request, 'detail.html', {'a':applicant, 'reference_no': pk, 'results':results, 'comments':comments, 'p':percentile})

def applicant_map(request):
	applicant = Applicants.objects.all()
	location = []
	ref = []
	for a in applicant:
		location.append(model_to_dict(a)['university_ug'])
		ref.append(model_to_dict(a)['reference_no'])
	return render (request, 'chart2.html', {'location': location, 'ref': ref})

def tsv(request, years, interest, axis,filt_ad=None):
	applicants = []
	if interest == 'all':
		if years == 'all':
			applicants.append(Applicants.objects.all())
		years = years.split("+")
		for y in years: 
			applicants.append(Applicants.objects.filter(year=y))
	else:
		if years == 'all':
			applicants.append(Applicants.objects.all().filter(interest1=interest))
		years = years.split("+")
		for y in years: 
			applicants.append(Applicants.objects.filter(year=y,interest1=interest))
	data = ['\t'.join([f.name for f in Applicants._meta.get_fields()]+["count"]),]
	for applicant in applicants:
		if "ad" in axis and "result" not in axis:
			applicant = applicant.filter(ad_result="ad")
		elif filt_ad =='1':
			applicant = applicant.filter(ad_result="ad")
		for a in applicant:
			a.gpa_ug = round(float(a.gpa_ug/a.gpa_ug_scale)*4.0,2) #pre-process GPA
			if a.interest1 == 'ALG':
				a.interest1 = 'AL'
			if 'M' in a.ad_degree:
				a.ad_degree ="MPhil"
			data.append('\t'.join([str(v).replace('\n', '').replace('\r', '') for v in [getattr(a, f.name) for f in Applicants._meta.get_fields()]]+["1"]))
	data = '\n'.join(data)
	return HttpResponse(data, 'text/plain; charset=utf8')






