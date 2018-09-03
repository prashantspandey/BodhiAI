from rest_framework import serializers
from membership.models import *
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
from basicinformation.api.serializers import *
from QuestionsAndPapers.api.serializers import *

class CustomRegistrationSerializer(serializers.ModelSerializer):
   username =\
   serializers.CharField(max_length=30,validators=[UniqueValidator(queryset=User.objects.all(),message=\
   "This username already exists. / यह यूजरनाम पहले से उपस्थित है , कृपया दूसरा यूजरनाम चुने "

                                                                  )])
   password = serializers.CharField(min_length=8,write_only=True)
   first_name = serializers.CharField(max_length=100)

   def create(self,validated_data):
       print(validated_data['username'])
       print(validated_data['password'])
       print(validated_data['first_name'])
       user =\
       User.objects.create_user(username=validated_data['username'],password = validated_data['password'],first_name
                                =validated_data['first_name'])
       return user

   class Meta:
       model = User
       fields = [
           'id',
           'username',
           'first_name',
           'password',

       ]


class StudentConfirmationSerializer(serializers.ModelSerializer):
    teacher = TeacherSerializer()
    student = StudentDetailSerializer()
    school = SchoolDisplaySerializer()
    class Meta:
       model = StudentConfirmation

       fields = [
           'id',
           'name',
           'student',
           'teacher',
           'batch',
           'school',
           'phone',
           'confirm',
       ]
