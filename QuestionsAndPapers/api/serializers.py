from rest_framework import serializers
from QuestionsAndPapers.models import *


class SchoolDisplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = [
            'name',
        ]
class TimesUsedSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimesUsed
        fields = [
            'batch',
            'numUsed',
        ]


class ChoicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choices
        fields = [
            'id',
            'text',
            'picture',
            'explanation',
            'explanationPicture',
            'predicament',

        ]
class QuestionMinimumSerializer(serializers.ModelSerializer):
    class Meta:
        model = SSCquestions
        fields = [
            'id',
        ]
class SSCansweredQuestionSerializer(serializers.ModelSerializer):
    quest = QuestionMinimumSerializer()
    class Meta:
        model = SSCansweredQuestion
        fields = [
            'time',
            'quest',
        ]
class SSCQuestionSerializer(serializers.ModelSerializer):
    choices = serializers.SerializerMethodField() 
    #timesused = serializers.SerializerMethodField()
    class Meta:
        model = SSCquestions
        depth = 1
        fields = [
            'id',
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
    
    def get_timesused(self,obj):
        return\
    TimesUsedSerializer(obj.timesused_set.all(),many=True,read_only=True).data

class TestSerializer(serializers.ModelSerializer):
    sscquestions = serializers.SerializerMethodField() 
    #sscquestions = SSCQuestionSerializer()
    class Meta:
        model = SSCKlassTest
        fields = [
            'id',
            'max_marks',
            'published',
            'creator',
            'sub',
            'totalTime',
            'sscquestions',

        ]
    def get_sscquestions(self,obj):
        return\
    SSCQuestionSerializer(obj.sscquestions_set.all(),many=True,read_only=True).data


class SSCOnlineMarksSerializer(serializers.ModelSerializer):
    test = TestSerializer()
    sscansweredquestion = serializers.SerializerMethodField() 
    class Meta:
        model = SSCOnlineMarks
        fields = [
            'id',
            'marks',
            'testTaken',
            'timeTaken',
            'rightAnswers',
            'wrongAnswers',
            'skippedAnswers',
            'test',
            'sscansweredquestion',



        ]

    def get_sscansweredquestion(self,obj):
        return\
    SSCansweredQuestionSerializer(obj.sscansweredquestion_set.all(),many=True,read_only=True).data


