from django.shortcuts import render
from data_preprocessing.mysql_connector import connect_mysql, make_query, close_dbc
from django.http import HttpResponse, JsonResponse
from mining1.models import Applicants2016

# Create your views here.

# def create_dataset(request):
# 	dbc = connect_mysql("fypdb")
# 	dataset = make_query(dbc, "333", "333")

# 	close_dbc(dbc)
# 	return JsonResponse(dataset, safe=False)

