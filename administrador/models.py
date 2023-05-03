# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import User


class AuthGroup(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    id = models.BigAutoField(primary_key=True)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    id = models.BigAutoField(primary_key=True)
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.IntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    id = models.BigAutoField(primary_key=True)
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
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


class ExamenesBreakdown(models.Model):
    id = models.BigAutoField(primary_key=True)
    answer = models.CharField(max_length=5)
    correct = models.CharField(max_length=5)
    exam = models.ForeignKey('ExamenesExam', on_delete=models.CASCADE)
    question = models.ForeignKey('PreguntasQuestion', on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'examenes_breakdown'


class ExamenesExam(models.Model):
    id = models.BigAutoField(primary_key=True)
    career = models.CharField(max_length=10)
    status_mod_1 = models.BooleanField(default=True)
    status_mod_2 = models.BooleanField(default=True)
    status_mod_3 = models.BooleanField(default=True)
    status_mod_4 = models.BooleanField(default=True)
    result_mod_1 = models.FloatField(default=0.0)
    result_mod_2 = models.FloatField(default=0.0)
    result_mod_3 = models.FloatField(default=0.0)
    result_mod_4 = models.FloatField(default=0.0)
    average = models.FloatField(default=0.0)
    stage = models.ForeignKey('ExamenesStage', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.career} - {self.stage} - {self.average}"
    
    def get_results(self, id_mod):
        respuestas = self.examenesbreakdown_set.filter(question__module__id=id_mod)
        total = len(respuestas)
        cuenta = 0
        for respuesta in respuestas:
            if respuesta.answer == respuesta.correct:
                cuenta += 1
        return total / cuenta

    class Meta:
        managed = False
        db_table = 'examenes_exam'


class ExamenesStage(models.Model):
    id = models.BigAutoField(primary_key=True)
    no_stage = models.BigIntegerField()
    application_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'examenes_stage'


class PreguntasModule(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 'preguntas_module'


class PreguntasQuestion(models.Model):
    id = models.BigAutoField(primary_key=True)
    question = models.TextField(blank=True, null=True)
    question_url = models.CharField(max_length=200, blank=True, null=True)
    resp1 = models.CharField(max_length=250)
    resp2 = models.CharField(max_length=250)
    resp3 = models.CharField(max_length=250, blank=True, null=True)
    resp4 = models.CharField(max_length=250, blank=True, null=True)
    correct = models.CharField(max_length=10)
    module = models.ForeignKey(PreguntasModule, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'preguntas_question'

