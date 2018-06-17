from django import forms
from django.utils.safestring import mark_safe
from mining1.models import Applicants

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field
from crispy_forms.bootstrap import (
	PrependedText, PrependedAppendedText, FormActions)

years = [ (d['year'],d['year']) for d in list(Applicants.objects.order_by('year').values('year').distinct())]
interests = [('all','All')] +[ (d['interest1'],d['interest1'])for d in list(Applicants.objects.order_by('interest1').values('interest1').distinct())]
apply_for = [ ('all','All')] + [(d['apply_for'],d['apply_for']) for d in list(Applicants.objects.order_by('apply_for').values('apply_for').distinct())]
ad_degree = [('all','All')] + [(d['ad_degree'],d['ad_degree']) for d in list(Applicants.objects.order_by('ad_degree').values('ad_degree').distinct())]

class Applicant_filter(forms.Form):

	filter_year = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(attrs={
                                  'checked':True,
                                  }), choices=years, required=True)
	filter_interest = forms.ChoiceField(widget=forms.Select, choices=interests, required=True)
	filter_admission =forms.BooleanField(initial=False,required=False)
	filter_hkpf = forms.BooleanField(initial=False,required=False)
	filter_application_program_type = forms.ChoiceField(widget=forms.Select, choices=apply_for, required=True)
	filter_admitted_program_type = forms.ChoiceField(widget=forms.Select, choices=ad_degree, required=True)
	helper = FormHelper()
	helper.form_method = 'POST'
	helper.form_class = 'form-horizontal'
	helper.label_class = 'col-sm-5'
	helper.field_class = 'col-sm-5'
	helper.layout = Layout(
		Field('filter_year'),
		Field('filter_interest'),
		Field('filter_admission'),
		Field('filter_hkpf'),
		Field('filter_application_program_type'),
		Field('filter_admitted_program_type'),
		FormActions(Submit('Submit', 'Submit', css_class='btn-primary'))
	)

class Feature_selection(forms.Form):
	OPTIONS = (
		("major_ug", "Undergraduate major"),
		("gpa_ug", "Undergraduate GPA"),
		("papers", "Papers published"),
		("toefl", "TOEFL score"),
		("qs_ug", "QS Ranking"))

	OPTIONS2 = (
		("1","Admission"),
		("2","HKPF"))
	select_years = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(attrs={
                                  'checked':True,
                                  }), choices=years, required=True)
	select_features = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(attrs={
								  'checked':True,
								  }), choices=OPTIONS, required=True)
	classified_on = forms.ChoiceField(widget=forms.Select, choices=OPTIONS2, required=True)
	helper = FormHelper()
	helper.form_method = 'POST'
	helper.form_class = 'form-horizontal'
	helper.label_class = 'col-sm-5'
	helper.field_class = 'col-sm-5'
	helper.layout = Layout(
		Field('select_years'),
		Field('select_features'),
		Field('classified_on'),
		FormActions(Submit('Submit', 'Submit', css_class='btn-primary'))
	)

class Feature_selection_chart(forms.Form):
	OPTIONS = [("gpa_ug", "Undergraduate GPA"),
		("papers", "Papers published"),
		("toefl", "TOEFL score"),
		("qs_ug", "QS Ranking")]
	OPTIONS2 = [("gender","Gender"),
	("interest1","Interest1"),
	("ad_result","Admission"),
	("year","Year"),
	("apply_for","Application Program Type"),
	("ad_degree","Admitted Program Type"),
	("ad_hkpf","HKPF"),
	("major_ug", "Undergraduate Major"),
	("ad_round", "Admitted Round")]
	filter_year = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(attrs={
                                  'checked':True,
                                  }), choices=years, required=True)
	filter_interest = forms.ChoiceField(widget=forms.Select, choices=interests, required=True)
	filter_admission =forms.BooleanField(initial=False,required=False)
	x_axis = forms.ChoiceField(widget=forms.Select,choices=OPTIONS,required=True)
	y_axis = forms.ChoiceField(widget=forms.Select,choices=OPTIONS,required=True)
	z_axis = forms.ChoiceField(widget=forms.Select,choices=OPTIONS2,required=True)

	helper = FormHelper()
	helper.form_method = 'POST'
	helper.form_class = 'form-horizontal'
	helper.label_class = 'col-sm-5'
	helper.field_class = 'col-sm-5'
	helper.layout = Layout(
		Field('filter_interest'),
		Field('filter_year'),
		Field('filter_admission'),
		Field('x_axis'),
		Field('y_axis'),
		Field('z_axis'),
		FormActions(Submit('Submit', 'Submit', css_class='btn-primary'))
	)

class Feature_selection_chart_2(forms.Form):
	OPTIONS = [	("year","Year"),
	("gender","Gender"),
	("interest1","Interest1"),
	("ad_result","Admission"),
	("apply_for","Application Program Type"),
	("ad_degree","Admitted Program Type"),
	("ad_hkpf","HKPF"),
	("major_ug", "Undergraduate Major"),
	("ad_round", "Admitted Round")]
	OPTIONS2 = [("apply_for","Application Program Type"),
	("year","Year"),
	("gender","Gender"),
	("interest1","Interest1"),
	("ad_result","Admission"),
	("ad_degree","Admitted Program Type"),
	("ad_hkpf","HKPF"),
	("major_ug", "Undergraduate Major"),
	("ad_round", "Admitted Round")]

	filter_year = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(attrs={
                                  'checked':True,
                                  }), choices=years, required=True)
	filter_interest = forms.ChoiceField(widget=forms.Select, choices=interests, required=True)
	filter_admission =forms.BooleanField(initial=False,required=False)
	x_axis = forms.ChoiceField(widget=forms.Select,choices=OPTIONS,required=True)
	y_axis = forms.ChoiceField(widget=forms.Select,choices=OPTIONS2,required=True)

	helper = FormHelper()
	helper.form_method = 'POST'
	helper.form_class = 'form-horizontal'
	helper.label_class = 'col-sm-5'
	helper.field_class = 'col-sm-5'
	helper.layout = Layout(
		Field('filter_interest'),
		Field('filter_year'),
		Field('filter_admission'),
		Field('x_axis'),
		Field('y_axis'),
		FormActions(Submit('Submit', 'Submit', css_class='btn-primary'))
	)
	
attributes = [('apply_phd', 'apply_phd'), ('apply_mph', 'apply_mph'), ('qs_ug', 'qs_ug'), ('major_cs', 'major_cs'), ('attend_pg', 'attend_pg'), ('papers', 'papers'), ('norm_gpa_ug', 'norm_gpa_ug')]

class Feature_selection_logistic_2(forms.Form):
	OPTIONS = [('Y17', 'year 2017'),
			   ('Y16', 'year 2016'), 
			   ('Y15', 'year 2015')]
	OPTIONS2 = [('ad_result', 'admission result')]
	independent_variables = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(attrs={
                                  'checked': True,
                                  }), choices=attributes, required=True)
	train_year = forms.ChoiceField(label=mark_safe('Training model year'), widget=forms.Select,choices=OPTIONS,required=True)
	test_year = forms.ChoiceField(label=mark_safe('Target year'), widget=forms.Select,choices=OPTIONS,required=True)
	target = forms.ChoiceField(label=mark_safe('Dependent variables'), widget=forms.Select,choices=OPTIONS2,required=True)
	helper = FormHelper()
	helper.layout = Layout(
		Field('independent_variables'),
		Field('target'),
		Field('train_year'),
		Field('test_year'),
		FormActions(
			Submit('submit', 'Submit', css_class="btn-primary"),
		)
	)

class Feature_selection_logistic(forms.Form):

	year = forms.MultipleChoiceField(
		label=mark_safe(''),
		choices = (
			('Y16', 'year 2016'), 
			('Y15', 'year 2015')
		),
		initial = 'option_one',
		widget = forms.CheckboxSelectMultiple,
	)
	helper = FormHelper()
	helper.layout = Layout(
		Field('year', style="background: #ffffff; padding: 10px;"),
		FormActions(
			Submit('submit', 'Submit', css_class="btn-primary"),
		)
	)


class Feature_selection_apriori(forms.Form):
	OPTIONS1 = [
		("ad_result", "Admission result")]
	feature_1 = forms.MultipleChoiceField(label=mark_safe('Feature 1'), widget=forms.CheckboxSelectMultiple(attrs={'checked': True,}), choices=OPTIONS1, required=False)
	# feature_1_value = forms.FloatField(label='value 1', required=False)

	OPTIONS2 = [
		("norm_gpa_ug", "Normalized UG GPA")]
	feature_2 = forms.MultipleChoiceField(label=mark_safe('Feature 2'), widget=forms.CheckboxSelectMultiple(attrs={'checked': True,}), choices=OPTIONS2, required=False)
	feature_2_value = forms.FloatField(label=mark_safe('GPA threshold'), required=False, initial=0.86)

	OPTIONS3 = [
		("qs_ug", "UG QS ranking")] 
	feature_3 = forms.MultipleChoiceField(label=mark_safe('Feature 3'), widget=forms.CheckboxSelectMultiple(attrs={'checked': True,}), choices=OPTIONS3, required=False)
	feature_3_value = forms.FloatField(label=mark_safe('QS threshold'), required=False, initial=112)

	OPTIONS4 = [
		("papers", "Paper published")]
	feature_4 = forms.MultipleChoiceField(label=mark_safe('Feature 4'), widget=forms.CheckboxSelectMultiple(attrs={'checked': True,}), choices=OPTIONS4, required=False)
	feature_4_value = forms.FloatField(label=mark_safe('Paper threshold'), required=False, initial=4)

	OPTIONS5 = [
		("interest1", "Research interest")]
	feature_5 = forms.MultipleChoiceField(label=mark_safe('Feature 5'), widget=forms.CheckboxSelectMultiple(attrs={'checked': True,}), choices=OPTIONS5, required=False)
	# feature_5_value = forms.FloatField(label=mark_safe('value 5'), required=False)
	OPTIONS6 = [
		("apply_for", "Apply program type")]
	feature_6 = forms.MultipleChoiceField(label=mark_safe('Feature 6'), widget=forms.CheckboxSelectMultiple(attrs={'checked': True,}), choices=OPTIONS6, required=False)
	
	# helper = FormHelper()
	# helper.form_method = 'POST'
	# helper.add_input(Submit('Submit', 'Submit', css_class='btn-primary'))
	helper = FormHelper()
	helper.form_method = 'POST'
	helper.form_class = 'form-horizontal'
	helper.label_class = 'col-sm-5'
	helper.field_class = 'col-sm-4'
	helper.layout = Layout(
		Field('feature_1'),
		Field('feature_2'),
		Field('feature_2_value'),
		Field('feature_3'),
		Field('feature_3_value'),
		Field('feature_4'),
		Field('feature_4_value'),
		Field('feature_5'),		
		Field('feature_6'),
		FormActions(Submit('Submit', 'Submit', css_class='btn-primary'))
	)

class Applicant_selection(forms.Form):
	OPTIONS = ()
	length = len(Applicants.objects.all())
	applicants = Applicants.objects.all()[(length/2):length]
	for a in applicants:
		if a.tc != '':
			a.reference_no = a.reference_no.replace('\r', '')
			choice = (a.reference_no, a.reference_no)
			OPTIONS = (choice,) + OPTIONS

	applicant = forms.ChoiceField(widget=forms.Select, choices=OPTIONS, required=True)
