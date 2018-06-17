from __future__ import unicode_literals

from django.db import models

# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

class Applicants(models.Model):
    idnum = models.TextField(blank=True, null=False, primary_key=True)
    reference_no = models.TextField(blank=True, null=True)
    year = models.TextField(db_column='Year', blank=True, null=True)  # Field name made lowercase.
    name = models.TextField(blank=True, null=True)
    ad_round = models.TextField(blank=True, null=True)
    ad_result = models.TextField(blank=True, null=True)
    ad_supervisor = models.TextField(blank=True, null=True)
    ad_group = models.TextField(blank=True, null=True)
    ad_degree = models.TextField(blank=True, null=True)
    ad_hkpf = models.TextField(blank=True, null=True)
    ad_scholarship = models.TextField(blank=True, null=True)
    gender = models.TextField(blank=True, null=True)
    apply_for = models.TextField(blank=True, null=True)
    university_ug = models.TextField(blank=True, null=True)
    qs_ug = models.IntegerField(db_column='QS_ug', blank=True, null=True)  # Field name made lowercase.
    qs_on_ug = models.IntegerField(db_column='QS_on_ug', blank=True, null=True)  # Field name made lowercase.
    major_ug = models.TextField(blank=True, null=True)
    major_ug_other = models.TextField(blank=True, null=True)
    gpa_ug = models.FloatField(blank=True, null=True)
    gpa_ug_scale = models.IntegerField(blank=True, null=True)
    rank_ug = models.TextField(blank=True, null=True)
    university_pg = models.TextField(blank=True, null=True)
    qs_pg = models.IntegerField(db_column='QS_pg', blank=True, null=True)  # Field name made lowercase.
    qs_on_pg = models.IntegerField(db_column='QS_on_pg', blank=True, null=True)  # Field name made lowercase.
    major_pg = models.TextField(blank=True, null=True)
    major_pg_other = models.TextField(blank=True, null=True)
    gpa_pg = models.FloatField(blank=True, null=True)
    gpa_pg_scale = models.IntegerField(blank=True, null=True)
    rank_pg = models.TextField(blank=True, null=True)
    interest1 = models.TextField(blank=True, null=True)
    interest2 = models.TextField(blank=True, null=True)
    interest3 = models.TextField(blank=True, null=True)
    english_tests = models.TextField(blank=True, null=True)
    papers = models.IntegerField(blank=True, null=True)
    hc = models.TextField(blank=True, null=True)
    tc = models.TextField(blank=True, null=True)
    toc = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    toefl = models.TextField(blank=True, null=True)
    cet6 = models.TextField(db_column='CET6', blank=True, null=True)  # Field name made lowercase.
    shortlisted = models.IntegerField(blank=True, null=True)
    norm_gpa_ug = models.FloatField(blank=True, null=True)
    norm_gpa_pg = models.FloatField(blank=True, null=True)
    qsranking = models.IntegerField(db_column='QSRanking', blank=True, null=True)  # Field name made lowercase.
    onqsranking = models.IntegerField(db_column='onQSRanking', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'applicants'

class Applicants2016(models.Model):
	reference_no = models.CharField(max_length=10, blank=True, null=False, primary_key=True)
	gender = models.CharField(max_length=1, blank=True, null=True)
	apply_for = models.CharField(max_length=10, blank=True, null=True)
	university_ug = models.CharField(max_length=30, blank=True, null=True)
	major_ug = models.CharField(max_length=10, blank=True, null=True)
	major_ug_other = models.CharField(max_length=30, blank=True, null=True)
	gpa_ug = models.FloatField(blank=True, null=True)
	gpa_ug_scale = models.FloatField(blank=True, null=True)
	rank_ug = models.CharField(max_length=20, blank=True, null=True)
	university_pg = models.CharField(max_length=30, blank=True, null=True)
	major_pg = models.CharField(max_length=10, blank=True, null=True)
	major_pg_other = models.CharField(max_length=30, blank=True, null=True)
	gpa_pg = models.FloatField(blank=True, null=True)
	gpa_pg_scale = models.FloatField(blank=True, null=True)
	rank_pg = models.CharField(max_length=20, blank=True, null=True)
	interest1 = models.CharField(db_column='Interest1', max_length=10, blank=True, null=True)  # Field name made lowercase.
	interest2 = models.CharField(db_column='Interest2', max_length=10, blank=True, null=True)  # Field name made lowercase.
	interest3 = models.CharField(db_column='Interest3', max_length=10, blank=True, null=True)  # Field name made lowercase.
	english_tests = models.CharField(max_length=50, blank=True, null=True)
	papers = models.IntegerField(blank=True, null=True)
	hc = models.TextField(blank=True, null=True)
	tc = models.TextField(blank=True, null=True)
	toc = models.TextField(blank=True, null=True)
	status = models.CharField(max_length=30, blank=True, null=True)
	toefl = models.IntegerField(blank=True, null=True)
	cet6 = models.IntegerField(db_column='CET6', blank=True, null=True)  # Field name made lowercase.
	shortlisted = models.IntegerField(blank=True, null=True)
	norm_gpa_ug = models.FloatField(blank=True, null=True)
	norm_gpa_pg = models.FloatField(blank=True, null=True)
	qsranking = models.IntegerField(db_column='QSRanking', blank=True, null=True)  # Field name made lowercase.
	onqsranking = models.IntegerField(db_column='onQSRanking', blank=True, null=True)  # Field name made lowercase.


	class Meta:
		managed = True
		db_table = 'applicants2016'



# class Applicants2014(models.Model):
# 	name = models.CharField(max_length=50, blank=True, null=False, primary_key=True)
# 	interest = models.CharField(max_length=50, blank=True, null=True)
# 	uni_ug = models.CharField(max_length=50, blank=True, null=True)
# 	uni_ug = models.CharField(max_length=50, blank=True, null=True)
# 	major_ug = models.CharField(max_length=50, blank=True, null=True)
# 	gpa_ug = models.CharField(max_length=50, blank=True, null=True)
# 	rank_ug = models.CharField(max_length=50, blank=True, null=True)
# 	uni_pg = models.CharField(max_length=50, blank=True, null=True)
# 	major_pg = models.CharField(max_length=50, blank=True, null=True)
# 	gpa_pg = models.CharField(max_length=50, blank=True, null=True)
# 	rank_pg = models.CharField(max_length=50, blank=True, null=True)
# 	english = models.CharField(max_length=50, blank=True, null=True)
# 	papers = models.CharField(max_length=50, blank=True, null=True)
# 	note = models.CharField(max_length=50, blank=True, null=True)
# 	shortlisted = models.CharField(max_length=50, blank=True, null=True)

# 	class Meta:
# 		managed = False
# 		db_table = 'Applicants2014'

class AuthGroup(models.Model):
	name = models.CharField(unique=True, max_length=80)

	class Meta:
		managed = False
		db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
	group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
	permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

	class Meta:
		managed = False
		db_table = 'auth_group_permissions'
		unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
	name = models.CharField(max_length=255)
	content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
	codename = models.CharField(max_length=100)

	class Meta:
		managed = False
		db_table = 'auth_permission'
		unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
	password = models.CharField(max_length=128)
	last_login = models.DateTimeField(blank=True, null=True)
	is_superuser = models.IntegerField()
	username = models.CharField(unique=True, max_length=150)
	first_name = models.CharField(max_length=30)
	last_name = models.CharField(max_length=30)
	email = models.CharField(max_length=254)
	is_staff = models.IntegerField()
	is_active = models.IntegerField()
	date_joined = models.DateTimeField()

	class Meta:
		managed = False
		db_table = 'auth_user'


class AuthUserGroups(models.Model):
	user = models.ForeignKey(AuthUser, models.DO_NOTHING)
	group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

	class Meta:
		managed = False
		db_table = 'auth_user_groups'
		unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
	user = models.ForeignKey(AuthUser, models.DO_NOTHING)
	permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

	class Meta:
		managed = False
		db_table = 'auth_user_user_permissions'
		unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
	action_time = models.DateTimeField()
	object_id = models.TextField(blank=True, null=True)
	object_repr = models.CharField(max_length=200)
	action_flag = models.SmallIntegerField()
	change_message = models.TextField()
	content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
	user = models.ForeignKey(AuthUser, models.DO_NOTHING)

	class Meta:
		managed = False
		db_table = 'django_admin_log'


class DjangoContentType(models.Model):
	app_label = models.CharField(max_length=100)
	model = models.CharField(max_length=100)

	class Meta:
		managed = False
		db_table = 'django_content_type'
		unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
	app = models.CharField(max_length=255)
	name = models.CharField(max_length=255)
	applied = models.DateTimeField()

	class Meta:
		managed = False
		db_table = 'django_migrations'


class DjangoSession(models.Model):
	session_key = models.CharField(primary_key=True, max_length=40)
	session_data = models.TextField()
	expire_date = models.DateTimeField()

	class Meta:
		managed = False
		db_table = 'django_session'

