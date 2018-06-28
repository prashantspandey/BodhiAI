from rest_framework import serializers
from QuestionsAndPapers.models import *


class SchoolDisplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = [
            'name',
        ]


class SSCQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SSCquestions
        fields = [
            'comprehension',
            'max_marks',
            'negative_marks',
            'text',
            'section_category',
            'topic_category',
            'picture',
            'source',
            'language',

        ]

