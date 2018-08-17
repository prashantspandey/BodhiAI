from rest_framework import serializers
from QuestionsAndPapers.models import *


class SchoolDisplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = [
            'name',
        ]

class ChoicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choices
        fields = [
            'text',
            'picture',
            'explanation',
            'explanationPicture',
            'predicament',

        ]


class SSCQuestionSerializer(serializers.ModelSerializer):
    choices = serializers.SerializerMethodField() 
    class Meta:
        model = SSCquestions
        depth = 1
        fields = [
            'comprehension',
            'max_marks',
            'negative_marks',
            'text',
            'section_category',
            'picture',
            'source',
            'language',
            'choices',

        ]

    def get_choices(self,obj):
        return\
    ChoicesSerializer(obj.choices_set.all(),many=True,read_only=True).data

