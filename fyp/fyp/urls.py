"""fyp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
#from mining1.views import applicant_list, applicant_detail
# from .views import index, applicant_list, applicant_detail, applicant_list1, applicant_map,applicant_chart,tsv,weight_tree

from .views import index, applicant_list, applicant_detail, applicant_list1, applicant_map, tsv, weight_tree
from .visualization import applicant_chart,applicant_chart_2
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles import views
from fyp.settings import MEDIA_ROOT
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from mining1.association_rule_1 import run_apriori_333
from mining1.logistic_regression import logistic, recommend_api, prediction
from mining1.decision_tree_c1 import decision_tree_c1
from mining1.decision_tree_classifier import decision_tree_c
from mining1.decision_tree_regression import decision_tree_r
#from mining1.k_means import k_means
#from mining1.network import neural_network
from mining1.text_mining1 import text_mining_1
from mining1.testing import decision_tree


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^index/$', index, name='index'),
    url(r'^index/(?P<year>\w+)$', index, name='index'),
    url(r'^api/v1/applicants/$', applicant_list, name='applicant_list'),
    url(r'^api/v1/chart/2/$', applicant_chart_2, name="applicant_chart_2"),
    url(r'^data/(?P<years>.*)/(?P<interest>.*)/(?P<axis>.*)/(?P<filt_ad>\w+).tsv/', tsv),
    url(r'^api/v1/chart/$', applicant_chart, name="applicant_chart"),
    url(r'^api/v1/applicants/(?P<year>.*)/(?P<id>\w+)/(?P<param>\w+)$', applicant_list1, name='applicant_list1'),
    url(r'^api/v1/applicant/(?P<pk>\w+)$', applicant_detail, name="applicant_detail"),
    #url(r'^api/v1/decision_tree/2014/$', decision_tree, name='decision_tree'),
    url(r'^api/v1/decision_tree/1/(?P<year>\w+)$', decision_tree_c, name='decision_tree_c'),
    #url(r'^api/v2/decision_tree/1/$', decision_tree_c1, name='decision_tree_c1'),
    url(r'^api/v1/text_mining/1/$', text_mining_1, name='text_mining_1'),
    url(r'^api/v1/decision_tree/2/(?P<year>\w+)$', decision_tree_r, name='decision_tree_r'),
    url(r'^api/v1/text_mining/1/$', text_mining_1, name='text_mining_1'),
    url(r'^api/v1/apriori/$', run_apriori_333, name='run_apriori'),
    url(r'^api/v1/logistic/$', logistic, name='logistic'),
    url(r'^api/v1/prediction/$', prediction, name='prediction'),
    url(r'^api/v1/recommend/$', recommend_api, name='recommend_api'),
    url(r'^api/v1/weightedtree/$', weight_tree, name='weight_tree'),
]

urlpatterns += [
        url(r'^static/(?P<path>.*)$', views.serve),
    ]

