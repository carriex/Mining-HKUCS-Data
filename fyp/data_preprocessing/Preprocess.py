
def readfeature(applicants):
	for index, a in enumerate(applicants):
		if "mph" in a.apply_for:
			applicants[index].apply_for = "MPhil"
		elif a.apply_for == "phd":
			applicants[index].apply_for = "PhD"
		elif a.apply_for == "either":
			applicants[index].apply_for = "PhD/MPhil"
		else:
			applicants[index].apply_for = a.apply_for
		if a.ad_hkpf == "1":
			a.ad_hkpf = "Awardee"
		else:
			a.ad_hkpf = "Non-Awardee"
		if 'Ph' in a.ad_degree:
			applicants[index].ad_degree = 'MPhil'


#This function preprocesses a set of applicants
def preprocess(applicants):	
	for index, a in enumerate(applicants):
		
		applicants[index].gpa_ug = a.gpa_ug/a.gpa_ug_scale
		if a.major_ug =='CS':
			applicants[index].major_ug = 1
		else:
			applicants[index].major_ug = 0
		if a.rank_ug is None or any(c.isalpha() for c in a.rank_ug):
			applicants[index].rank_ug = -1
		elif '/' in a.rank_ug and a.rank_ug.split('/')[0].isdigit() and a.rank_ug.split('/')[1].isdigit():
			applicants[index].rank_ug = float(a.rank_ug.split('/')[0])/float(a.rank_ug.split('/')[1])
		elif '%' in a.rank_ug and a.rank_ug.split('%')[0].isdigit():
			applicants[index].rank_ug = float(a.rank_ug.split('%')[0][-1])/100
		else:
			applicants[index].rank_ug = -1

		if "mph" in a.apply_for:	
			applicants[index].apply_for = 0 
		elif a.apply_for == "phd":
			applicants[index].apply_for = 1
		else:
			applicants[index].apply_for = 2

		if a.ad_result == "rej":
			applicants[index].ad_result = 0
		elif a.ad_degree == "PhD":
			applicants[index].ad_result = 1
		elif a.ad_result == "NA":
			applicants[index].ad_result = 0
		else:
			applicants[index].ad_result = 2

		if a.ad_hkpf != "1":
			applicants[index].ad_hkpf = 0

		if a.qs_on_ug == 0:
			applicants[index].qs_ug = 650
		if a.papers == 'NI':
			applicants[index].papers = 0
		if a.toefl == 'NI':
			applicants[index].toefl = 0
		if 'Ph' in a.ad_degree:
			applicants[index].ad_degree = 'MPhil'

	return applicants

def clearlabel(applicant):
	applicant['Reference No'] = applicant.pop('reference_no')
	applicant['Gender'] = applicant.pop('gender')
	applicant['Apply for ']  = applicant.pop('apply_for')
	applicant['Undergraduate University'] = applicant.pop('university_ug')
	applicant['Undergraduate Major'] = applicant.pop('major_ug')
	applicant['Undergraduate Major (other)'] = applicant.pop('major_ug_other') 
	applicant['Undergraduate GPA'] = applicant.pop('gpa_ug')
	applicant['Undergraduate GPA Scale'] = applicant.pop('gpa_ug_scale') 
	applicant['Undergraduate Ranking'] = applicant.pop('rank_ug') 
	applicant['Postgraduate University'] = applicant.pop('university_pg')
	applicant['Postgraduate Major'] = applicant.pop('major_pg') 
	applicant['Postgraduate Major (other)'] = applicant.pop('major_pg_other')
	applicant['Postgraduate GPA'] = applicant.pop('gpa_pg') 
	applicant['Postgraduate GPA Scale'] = applicant.pop('gpa_pg_scale')
	applicant['Postgraduate Ranking'] = applicant.pop('rank_pg') 
	applicant['1st Interest'] = applicant.pop('interest1') 
	applicant['2nd Inerest'] = applicant.pop('interest2')
	applicant['3rd Interest'] = applicant.pop('interest3') 
	applicant['English Test Scores'] = applicant.pop('english_tests') 
	applicant['Papers published'] = applicant.pop('papers')
	applicant['Helper\'s comment'] = applicant.pop('hc') 
	applicant['Teachers\' comment'] = applicant.pop('tc')
	applicant['Teachers\' comment 2'] = applicant.pop('toc') 
	applicant['Application Status'] = applicant.pop('status') 
	applicant['TOEFL Score'] = applicant.pop('toefl') 
	applicant['CET6 Score'] = applicant.pop('cet6') 
	applicant['Shortlisted or not '] = applicant.pop('shortlisted') 
	applicant['Undergraduate GPA (Norm)'] = applicant.pop('norm_gpa_ug')
	applicant['Postgraduate GPA (Norm)'] = applicant.pop('norm_gpa_pg')
	applicant['Undergraduate University QS Ranking'] = applicant.pop('qsranking')
	applicant.pop('onqsranking')

