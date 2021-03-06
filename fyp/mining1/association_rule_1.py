from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from mining1.models import Applicants2016, Applicants
import json
import os
from numpy import *
from mining1.apriori_api import apriori, dump_as_json
from mining1.forms import Feature_selection_apriori
from django.utils.safestring import mark_safe
from django.db.models import Q



# def preprocess_333(applicants):	#This function should be written elsewhere; how to pre-process some attributes
# 	applicants = Applicants.objects.all()

# 	for index, a in enumerate(applicants):
# 		if a.major_ug =='CS':
# 			applicants[index].major_ug = 1
# 		else:
# 			applicants[index].major_ug = 0

# 		# if a.rank_ug == 'DK' or a.rank_ug == 'N/A':
# 		# 	applicants[index].rank_ug = -1
# 		# elif '/' in a.rank_ug and a.rank_ug.split('/')[0].isdigit():
# 		# 	applicants[index].rank_ug = float(a.rank_ug.split('/')[0])/float(a.rank_ug.split('/')[1])
# 		# elif '%' in a.rank_ug:
# 		# 	applicants[index].rank_ug = float(a.rank_ug.split('%')[0][-1])/100
# 		# else:
# 		# 	applicants[index].rank_ug = -1

# 		if a.apply_for == "mphil":	
# 			applicants[index].apply_for = 0 
# 		elif a.apply_for == "phd":
# 			applicants[index].apply_for = 1
# 		else:
# 			applicants[index].apply_for = 2

# 		if a.onqsranking == 0:
# 			a.qsranking = 100

# 	return applicants

def prepare_dataset_333(applicants, features, features_value):
	transaction_list = list()
	# data_iterator = list()
	for applicant in applicants:
		transaction = []
		for f in features:
			if f:
				if isinstance(f, list):
					if isinstance(getattr(applicant, f[0]), str):
						if getattr(applicant, f[0]) == "ad":
							transaction.append("admit")
						elif getattr(applicant, f[0]) == "rej":
							transaction.append("reject")
						else:
							transaction.append(getattr(applicant, f[0]))
					else:
						if getattr(applicant, f[0]) >= features_value[str(f)]:
							transaction.append(str(f[0]) + " >= " + str(features_value[str(f)]))
						else:
							transaction.append(str(f[0]) + " < " + str(features_value[str(f)]))
				else:
					if isinstance(getattr(applicant, f), str):
						if getattr(applicant, f) == "ad":
							transaction.append("admit")
						elif getattr(applicant, f) == "rej":
							transaction.append("reject")
						else:
							transaction.append(getattr(applicant, f))
					else:
						if getattr(applicant, f) >= features_value[str(f)]:
							transaction.append(str(f) + " >= " + str(features_value[str(f)]))
						else:
							transaction.append(str(f) + " < " + str(features_value[str(f)]))
		transaction_list.append(transaction)
		# for item in transaction:
		# 	# de
		# 	# item_set.add(item)
		# 	item_set.add(frozenset([item]))
	return transaction_list

@csrf_exempt
def run_apriori_333(request):
	# shared variables
	form = ""
	json_str = ""
	description = []
	result_rule = []
	rank_rule = []
	applicants = Applicants.objects.filter(Q(year="Y15") | Q(year="Y16"))
	# applicants = Applicants.objects.filter(year="Y17")
	for index, a in enumerate(applicants):
		print(a.idnum)
	if request.method == 'GET':
		features = ["ad_result", "norm_gpa_ug", "qs_ug", "papers", "interest1", "apply_for"]
		features_value = {features[0]:0, features[1]: 0.86, features[2]: 112, features[3]: 4, features[4]: 0, features[5]: 0}
		form = Feature_selection_apriori
		description.append("Below are the sample association rules generated on the 2015 & 2016 Applicaiton data using Apriori algorithm.")
		description.append("By default, it uses all the features and threshold values generated by Decision Tree.")

	elif request.method == 'POST':
		form = Feature_selection_apriori(request.POST)
		if form.is_valid():

			feature_1 = form.cleaned_data.get('feature_1')
			# feature_1_value = form.cleaned_data.get('feature_1_value')
			feature_2 = form.cleaned_data.get('feature_2')
			feature_2_value = form.cleaned_data.get('feature_2_value')
			feature_3 = form.cleaned_data.get('feature_3')
			feature_3_value = form.cleaned_data.get('feature_3_value')
			feature_4 = form.cleaned_data.get('feature_4')
			feature_4_value = form.cleaned_data.get('feature_4_value')
			feature_5 = form.cleaned_data.get('feature_5')
			feature_6 = form.cleaned_data.get('feature_6')

			features = [feature_1, feature_2, feature_3, feature_4, feature_5, feature_6]
			features_value = {str(feature_1): 0, str(feature_2): feature_2_value, str(feature_3): feature_3_value, str(feature_4): feature_4_value, str(feature_5): 0, str(feature_6): 0}
		else:
			description.append("form is invalid")
			return render(request, 'apriori.html', {'form':form, 'description': description})
		description.append("Below are the association rules generated on the 2015 & 2016 Applicaiton data using Apriori algorithm.")
		description.append("It uses customized features and threshold values.")


	transaction_list = prepare_dataset_333(applicants, features, features_value)
	
	# print(transaction_list)
	results = list(apriori(transaction_list))
	

	json_str = results
	des, result_rule, rank_rule = compute_result(results)
	# description += des
	description.append("Support is an indication of how frequently the items appear in the database.")
	description.append("Confidence indicates the number of times the association rule have been found to be true.")

	return render(request, 'apriori.html', {'form':form, 'json_str':json_str,'description': description, 'result': result_rule, 'rules': rank_rule})
	
def compute_result_333(results):
	return

def compute_result(results):

	max_s = 0
	best_s_rule = ""
	best_s_statistics = []
	best_s_con = 0
	best_s_base = ""
	best_s_add = ""

	max_c = 0
	best_c_rule = ""
	best_c_items = ""
	best_c_support = 0
	best_c_base = ""
	best_c_add = ""
	best_c_con = 0

	items_list = []
	support_list = []

	items_list_3 = []
	support_list_3 = []
	
	des = []

	for r in results:
			# transform each r to a dictionary
			r = json.loads(r)
			
			des.append(str(r))

			# capture itemset for each rule
			first = True
			items = "{"
			for i in r['items']:		
				if first == False:
					items = items + ", "
				items = items + str(i)
				first = False
			items = items + "}"

			if len(r['items']) >= 3 and r['support'] > max_s:
				best_s_rule = items
				max_s = r['support']
				best_s_statistics = r['ordered_statistics']

			items_list.append(items)
			support_list.append(int(r['support']*100))

			if len(r['items']) >= 3:
				items_list_3.append(items)
				support_list_3.append(int(r['support']*100))

			for sta in r['ordered_statistics']:
				if sta['confidence'] > max_c and str(sta['items_add']) == "['admit']":
					best_c_items = items
					best_c_support = r['support']
					best_c_base = sta['items_base']
					best_c_add = sta['items_add']
					best_c_con = sta['confidence']
					best_c_rule = str(sta['items_base']) + "->" + str(sta['items_add'])
					max_c = sta['confidence']

	des.insert(0, "The best confidence rule is " + best_c_rule + " with the greatest confidence value " + str(max_c))
	des.insert(1, "The best support itemset is " + best_s_rule + " with the greatest support value " + str(max_s))
	
	for sta in best_s_statistics:
		if sta['confidence'] > best_s_con:
			best_s_base = str(sta['items_base'])
			best_s_add = str(sta['items_add'])
			best_s_con = sta['confidence']

	e_s = "Itemset with highest support and its highest confidence rule"
	support_r = {'itemset': best_s_rule, 'support': round(max_s,2), 'base': best_s_base, 'add': best_s_add, 'confidence': round(best_s_con,2), 'explanation': e_s}
	e_c = "Highest confidence rule and its support value"
	support_c = {'itemset': best_c_items, 'support': round(best_c_support,2), 'base': best_c_base, 'add': best_c_add, 'confidence': round(best_c_con,2), 'explanation': e_c}
	
	result_rule = []
	result_rule.insert(0, support_r)
	result_rule.insert(1, support_c)

	color = ['red', 'yellow', 'light-blue']

	indices = list(range(len(support_list_3)))
	indices.sort(key=lambda x: support_list_3[x])
	rank = [0] * len(indices)
	num = len(support_list_3)
	for i, x in enumerate(indices):
	    rank[x] = num - i
	s_list = []
	i_list = []
	for i, a in enumerate(support_list_3):
		if rank[i] == 1 or rank[i] == 2 or rank[i] == 3:
			s_list.append(a)
			i_list.append(items_list_3[i])

	support_list
	rank_rule = sorted(zip(s_list, i_list, color), reverse=True)[:3]
	return des, result_rule, rank_rule



# @csrf_exempt
# def run_apriori(request):
# 	description = []
# 	description.append("This is a sample Association Rule generated on the Applicaiton data using Apriori algorithm.")
# 	result_rule = []
# 	rank_rule = []
# 	color = ['red', 'yellow', 'light-blue']
# 	if request.method == 'GET':
# 		applicants = preprocess(Applicants.objects.all())
# 		applicants = Applicants.objects.filter(Q(year="Y15") | Q(year="Y16"))

# 		features = ["major_ug", "norm_gpa_ug", "papers", "qs_ug"]
# 		features_value = {features[0]:0, features[1]: 0.8, features[2]: 1, features[3]: 200}
# 		transaction_list, item_set = prepare_dataset1(applicants, features, features_value)
		
# 		results = list(apriori(transaction_list))
# 		index = 1
# 		max_support = 0
# 		best_support_rule = ""
# 		max_confidence = 0
# 		best_confidence_rule = ""
# 		for r in results:
# 			# print("Result", index)
# 			r = json.loads(r)
# 			# print("itemset:{", end="")
# 			start = True
# 			items = "{"
# 			for i in r['items']:		
# 				if start == False:
# 					# print(", ", end="")
# 					items = items + ", "
# 				# print(i, end="")
# 				items = items + str(i)
# 				start = False
# 			# print("}")
# 			items = items + "}"

# 			# print("Support:", r['support'], sep=" ")
# 			if r['support'] > max_support:
# 				best_support_rule = items
# 				max_support = r['support']
# 			# print("Ordered_statistics:")
# 			for sta in r['ordered_statistics']:
# 				if sta['confidence'] > max_confidence:
# 					best_confidence_rule = str(sta['items_base']) + "->" + str(sta['items_add'])
# 					max_confidence = sta['confidence']

# 			index += 1

# 		form = Feature_selection_apriori
# 		json_str = ""
# 		description.insert(1, "The best confidence rule is " + best_confidence_rule + " with the greatest confidence value " + str(max_confidence))
# 		description.insert(2, "The best support itemset is " + best_support_rule + " with the greatest support value " + str(max_support))
# 		return render(request, 'apriori.html', {'form':form, 'json_str':json_str,'description': description, 'result': result_rule, 'rules': rank_rule, 'color': color})
# 	elif request.method == 'POST':
# 		form = Feature_selection_apriori(request.POST)
# 		if form.is_valid():
# 			feature_1 = form.cleaned_data.get('feature_1')
# 			# feature_1_value = form.cleaned_data.get('feature_1_value')
# 			feature_2 = form.cleaned_data.get('feature_2')
# 			feature_2_value = form.cleaned_data.get('feature_2_value')
# 			feature_3 = form.cleaned_data.get('feature_3')
# 			feature_3_value = form.cleaned_data.get('feature_3_value')
# 			feature_4 = form.cleaned_data.get('feature_4')
# 			feature_4_value = form.cleaned_data.get('feature_4_value')
# 			feature_5 = form.cleaned_data.get('feature_5')
# 			feature_6 = form.cleaned_data.get('feature_6')
# 			# feature_5_value = form.cleaned_data.get('feature_5_value')
# 			features = [feature_1, feature_2, feature_3, feature_4, feature_5, feature_6]
# 			features_value = {str(feature_1): 1, str(feature_2): feature_2_value, str(feature_3): feature_3_value, str(feature_4): feature_4_value, str(feature_5): 1, str(feature_6): 1}
# 			# features_value = [feature_1_value, feature_2_value, feature_3_value]
# 		else:
# 			description.append("form is invalid")
# 			return render(request, 'apriori.html', {'form':form, 'description': description, 'result': result_rule, 'rules': rank_rule, 'color': color})

# 		# description.append(str(feature_1))
# 		# description.append(str(feature_1_value))
# 		# description.append(str(feature_2))
# 		# description.append(str(feature_2_value))
# 		# description.append(str(features))
# 		# return render(request, 'apriori.html', {'form':form, 'description': description})

# 		applicants = list(Applicants2016.objects.values())

# 		transaction_list, item_set = prepare_dataset(applicants, features, features_value)

# 		results = list(apriori(transaction_list))
# 		# print_to_output(results)
# 		# results = format_json(results)

# 		index = 1
# 		max_support = 0
# 		best_support_rule = ""
# 		max_confidence = 0
# 		best_confidence_rule = ""
# 		best_con_items = ""
# 		best_con_support = 0
# 		best_con_base = ""
# 		best_con_add = ""
# 		best_con_con = 0
# 		items_list = []
# 		support_list = []
# 		best_s_statistics = []
# 		for r in results:
# 			# print("Result", index)
# 			description.append(mark_safe('<br />'))
# 			description.append("Result "+str(index))
# 			r = json.loads(r)
# 			# print("itemset:{", end="")
# 			description.append("itemset:{")
# 			start = True
# 			items = "{"
# 			for i in r['items']:		
# 				if start == False:
# 					# print(", ", end="")
# 					items = items + ", "
# 					description[-1] = description[-1] + ", "
# 				# print(i, end="")
# 				description[-1] = description[-1] + str(i)
# 				items = items + str(i)
# 				start = False
# 			# print("}")
# 			description[-1] = description[-1] + "}"
# 			items = items + "}"

# 			# print("Support:", r['support'], sep=" ")
# 			description.append("Support: " + str(r['support']))
# 			if r['support'] > max_support:
# 				best_support_rule = items
# 				max_support = r['support']
# 				best_s_statistics = r['ordered_statistics']

# 			items_list.append(items)
# 			support_list.append(int(r['support']*100))

# 			# print("Ordered_statistics:")
# 			description.append("Ordered_statistics: ")
# 			for sta in r['ordered_statistics']:
# 				# print('  items_base: ', str(sta['items_base']))
# 				description.append("-  items_base: " + str(sta['items_base']))
# 				# print('    items_add: ', str(sta['items_add']))
# 				description.append("-    items_add: " + str(sta['items_add']))
# 				# print('    confidence: ', sta['confidence'])
# 				description.append("-    confidence: " + str(sta['confidence']))
# 				# print('    lift: ', sta['lift'])
# 				description.append("-    lift: " + str(sta['lift']))
# 				if sta['confidence'] > max_confidence and str(sta['items_add']) == "['shortlisted good']":
# 					best_con_items = items
# 					best_con_support = r['support']
# 					best_con_base = sta['items_base']
# 					best_con_add = sta['items_add']
# 					best_con_con = sta['confidence']
# 					best_confidence_rule = str(sta['items_base']) + "->" + str(sta['items_add'])
# 					max_confidence = sta['confidence']

# 			index += 1
# 		# description.append(str(results))
# 		description.insert(1, "The best confidence rule is " + best_confidence_rule + " with the greatest confidence value " + str(max_confidence))
# 		description.insert(2, "The best support itemset is " + best_support_rule + " with the greatest support value " + str(max_support))
		
# 		new_des = []
# 		new_des.insert(1, "The best confidence rule is " + best_confidence_rule + " with the greatest confidence value " + str(max_confidence))
# 		new_des.insert(2, "The best support itemset is " + best_support_rule + " with the greatest support value " + str(max_support))
		
# 		max_con = 0
# 		base = ""
# 		add = ""
# 		for sta in best_s_statistics:
# 			if sta['confidence'] > max_con:
# 				base = str(sta['items_base'])
# 				add = str(sta['items_add'])
# 				max_con = sta['confidence']
# 		e_s = "Itemset with highest support and its highest confidence rule"
# 		support_r = {'itemset': best_support_rule, 'support': round(max_support,2), 'base': base, 'add': add, 'confidence': round(max_con,2), 'explanation': e_s}
# 		e_c = "Highest confidence rule and its support value"
# 		support_c = {'itemset': best_con_items, 'support': round(best_con_support,2), 'base': best_con_base, 'add': best_con_add, 'confidence': round(best_con_con,2), 'explanation': e_c}
# 		result_rule.insert(0, support_r)
# 		result_rule.insert(1, support_c)

# 		# applicant_list = []
# 		# q = []
# 		# for i in items_list:
# 		# 	if "low-QSRanking" in i:
# 		# 		q = Applicants.objects.filter(="What")

# 		rank_rule = sorted(zip(support_list, items_list, color), reverse=True)[:3]
# 		# rank_rule = sorted(zip(rank_rule, color), reverse=True)[:3]
# 		print(rank_rule)
# 		return render(request, 'apriori.html', {'form':form, 'json_str':results, 'description': new_des, 'result': result_rule, 'rules': rank_rule, 'color': color})


def format_json(results):
	format_results = []
	for r in results:
		format_result = {}
		# print(type(r))
		re = json.loads(r)
		format_result['items'] = re['items']
		format_result['support'] = re['support']
		format_result['ordered_statistics'] = re['ordered_statistics']
		format_results.append(format_result)
	return format_results
	

def print_to_output(results):
	with open('apriori_output.txt', 'w') as outfile:
		json.dump(results, outfile)

#prepare dataset and item_set
# def prepare_dataset(applicants, features, features_value):
# 	transaction_list = list()
# 	item_set = set()
# 	data_iterator = list()
# 	for applicant in applicants:
# 		transaction = []
# 		for f in features:
# 			if f:
# 				if str(f[0]) == "qsranking":
# 					if applicant[f[0]] >= features_value[str(f)]:
# 						transaction.append("low-QSRanking")
# 					elif applicant[f[0]] == -1:
# 						transaction.append("no-QSRanking")
# 					else:
# 						transaction.append("high-QSRanking")
# 				elif str(f[0]) == "interest1" or str(f[0]) == "apply_for":
# 					transaction.append(str(applicant[f[0]]))
# 				else:
# 					if applicant[f[0]] >= features_value[str(f)]:
# 						transaction.append(str(f[0]) + " good")
# 					else:
# 						transaction.append(str(f[0]) + " bad")



		
# 		# if applicant['norm_gpa_ug'] >= 0.9038:
# 		# 	transaction.append("high-GPA")
# 		# else:
# 		# 	transaction.append("low-GPA")
# 		# if applicant['qsranking'] == -1 :
# 		# 	transaction.append("NA-QSRanking")
# 		# elif applicant['qsranking'] <= 50 :
# 		# 	transaction.append("high-QSRanking")
# 		# else:
# 		# 	transaction.append("low-QSRanking")
# 		transaction_list.append(transaction)
# 		# for item in transaction:
# 		# 	# de
# 		# 	# item_set.add(item)
# 		# 	item_set.add(frozenset([item]))
# 	return transaction_list, item_set


# def prepare_dataset1(applicants, features, features_value):
# 	transaction_list = list()
# 	item_set = set()
# 	data_iterator = list()
# 	for applicant in applicants:
# 		transaction = []
# 		for f in features:
# 			if f:
# 				if isinstance(getattr(applicant, f), str):
# 					transaction.append(getattr(applicant, f))
# 				else:
# 					if getattr(applicant, f) >= features_value[str(f)]:
# 						transaction.append(str(f) + " >= " + str(features_value[str(f)]))
# 					else:
# 						transaction.append(str(f) + " < " + str(features_value[str(f)]))
# 		transaction_list.append(transaction)
# 		# for item in transaction:
# 		# 	# de
# 		# 	# item_set.add(item)
# 		# 	item_set.add(frozenset([item]))
# 	return transaction_list, item_set

# #scan dataset and calculate support data
# def scan_data(transaction_list, item_set, min_support):
#     candidate = {}
#     for transaction in transaction_list:
#         for item in item_set:
#             if item.issubset(transaction):
#                 if not candidate.has_key(item): candidate[item]=1
#                 else: candidate[item] += 1
#     num_items = float(len(transaction_list))
#     ret_list = []
#     support_data = {}
#     for key in candidate:
#         support = candidate[key]/num_items
#         if support >= min_support:
#             ret_list.insert(0, key)
#         support_data[key] = support
#     return ret_list, support_data

# def apriori_join(item_list, k): #creates Ck
#     ret_list = []
#     len_item_list = len(item_list)
#     for i in range(len_item_list):
#         for j in range(i+1, len_item_list): 
#             l1 = list(item_list[i])[:k-2]
#             l2 = list(item_list[j])[:k-2]
#             l1.sort()
#             l2.sort()
# 	    #print "L1:",L1
# 	    #print "L2:",L2
# 	    #compare the first items to avoid duplicate
#             if l1==l2: #if first k-2 elements are equal,namely,besides the last item,all the items of the two sets are the same!
#                 ret_list.append(item_list[i] | item_list[j]) #set union
#     return ret_list


#format dataset
# @csrf_exempt
# def run_apriori(request):
# 	if request.method == 'GET':
# 		applicants = list(Applicants2016.objects.values())

# 		transaction_list, item_set = prepare_dataset(applicants)

# 		item_list, support_data = scan_data(transaction_list, item_set, 0.6)
# 		item_list = [item_list]
# 		k = 2
# 		while (len(item_list[k-2]) > 0):
# 	        freq_set = apriori_join(item_list[k-2], k)
# 	        ret_list, support_k = scan_data(transaction_list, freq_set, min_support)#scan DB to get Lk
# 	        support_data.update(support_k)
# 	        item_list.append(ret_list)
# 	        k += 1
# 	    return item_list, support_data
