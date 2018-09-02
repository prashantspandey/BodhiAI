from rest_framework import serializers
from membership.models import *
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User

class CustomRegistrationSerializer(serializers.ModelSerializer):
   username =\
   serializers.CharField(max_length=30,validators=[UniqueValidator(queryset=User.objects.all(),message=\
   "This username already exists. / यह यूजरनाम पहले से उपस्थित है , कृपया दूसरा यूजरनाम चुने "

                                                                  )])
   password = serializers.CharField(min_length=8,write_only=True)
   first_name = serializers.CharField(max_length=100)

   def create(self,validated_data):
       user =\
       User.objects.create_user(validated_data['username'],validated_data['password'],validated_data['first_name'])
       return user

   class Meta:
       model = User
       fields = [
           'id',
           'username',
           'first_name',
           'password',

       ]
