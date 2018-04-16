from rest_framework import serializers
from basicinformation.models import *
from QuestionsAndPapers.models import SSCKlassTest


class SchoolDisplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = [
            'name',
        ]
class StudentModelSerializer(serializers.ModelSerializer):
    #school = SchoolDisplaySerializer()
    #user = serializers.SerializerMethodField()
    class Meta:
        model = Student
        fields = [
            'name',
        ]

    #def get_user(self,obj):
    #    return str(obj.studentuser.email)
