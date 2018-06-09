from rest_framework import generics
from celery.result import AsyncResult
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from basicinformation.models import *
from django.http import Http404, HttpResponse
from .serializers import *
from basicinformation.marksprediction import *
from QuestionsAndPapers.models import *
from basicinformation.models import *
from basicinformation.marksprediction import *
import json
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticated
)
from basicinformation.tasks import *



class StudentListAPIView(generics.ListAPIView):
    serializer_class = StudentModelSerializer
    def get_queryset(self):
        return Student.objects.all()

class StudentDetailAPIView(APIView):

    def get(self,request,format=None):
        user = self.request.user
        username = user.username
        email = user.email
        first_name = user.first_name
        me = Studs(user)
        school_name = me.profile.school.name
        subjects = me.my_subjects_names()

        my_details =\
        {'username':username,'email':email,'firstName':first_name,'school':school_name,'subjects':subjects}
        return Response(my_details)


        

# Return all the information about tests that a student has to take to be
# displayed on the home screen

class FrontPageTestAPIView(APIView):
    def get(self,request,format=None):
        me = Studs(self.request.user)
        tests = me.toTake_Tests(20)
        all_tests = []
        for key,value in tests.items():
            topics = value['topics']
            subject = value['subject']
            test_id = key
            j_topics = json.dumps(topics)
            j_subject = json.dumps(subject)
            j_testid = json.dumps(test_id)
            j_creator = json.dumps(value['creator'])
            j_questions = json.dumps(value['num_questions'])
            psudo_test =\
            {'topics':j_topics,'subject':j_subject,'test_id':j_testid,'creator':j_creator,'num_questions':j_questions}
            all_tests.append(psudo_test)
        return Response(all_tests)

class PreviousSubjectPerformance(APIView):
    serializers = SSCOnlineMarksModelSerializer
    def get(self,request,format=None):
        me = Studs(self.request.user)
        all_subjects = me.my_subjects_names()
        test_info = me.test_marks_api(all_subjects)
        #online_marks = SSCOnlineMarks.objects.filter(student = me.profile)
        print(test_info)
        return Response(test_info)

class UplodatQuestionsAPI(APIView):
    def post(self,request,*args,**kwargs):
        name = request.POST['name']
        studs = Student.objects.all()
        num_studs = len(studs)
        text = 'Success! Hello %s, there are %s students at BodhiAI'\
        %(name,num_studs)
        return Response(text)


class LastClassTestPerformanceTeacherAPI(APIView):
    def get(self,request,format = None):
        #me = Teach(self.request.user)
        new_test = SSCKlassTest.objects.filter(creator =
                                              self.request.user).order_by('published')[3]
        counter = 0
        quest_marks = 0
        for quest in new_test.sscquestions_set.all():
            counter = counter + 1
            quest_marks = quest_marks + quest.max_marks
            
        publised_date = new_test.published
        subject = new_test.sub
        my_tests = SSCOnlineMarks.objects.filter(test__creator =
                                                 self.request.user,test
                                                 =new_test )
        marks = []
        for test in my_tests:
            marks.append((test.marks/quest_marks)*100)
        info =\
        {'subject':subject,'date':publised_date,'test_takers':len(my_tests),'marks':marks,'num_questions':counter}
        return Response(info)



class TeacherWeakAreasBrief(APIView):
    def get(self,request,format=None):
        me = Teach(self.request.user)
        subjects = me.my_subjects_names()
        weak_subs_areas_dict = []
        teach_klass = TeacherClasses.objects.filter(teacher=me.profile)
        klasses = []
        if len(teach_klass) != 0:
            for kl in teach_klass:
                klasses.append(kl.klass)
        else:
            klasses = me.my_classes_names()
            for kl in klasses:
                new_teach_klass = TeacherClasses()
                new_teach_klass.teacher = me.profile
                new_teach_klass.klass = kl
                new_teach_klass.numStudents = 0
                new_teach_klass.save()


        #weak_ar = teacher_home_weak_areas.delay(self.request.user.id)
        weak_ar = teacher_home_weak_areas(self.request.user.id)
        #print(weak_ar)
        #te_id = weak_ar.task_id
        #res = AsyncResult(te_id)

        #klasses,subjects = res.get()
        
        weak_links = {}
        weak_klass = []
        weak_subs = []
        subs = []
        try:
            for sub in subjects:
                for i in klasses:
                    try:
                        print('%s this is i' %i)
                        weak_links[i]= \
                        me.online_problematicAreasNames(self.request.user,sub,i)
                        kk = me.online_problematicAreasNames(self.request.user,sub,i)
                        weak_subs.append(weak_links[i])

                        weak_klass.append(i)
                        subs.append(sub)


                        #print(weak_links)
                        #print(weak_subs)
                    except Exception as e:
                        print(str(e))
            weak_subs_areas = list(zip(subs,weak_klass,weak_subs))
            #weak_subs_areas = None
        except:
            weak_subs_areas = None

        return Response(weak_subs_areas)


class TeacherTestsOverview(APIView):
    def get(self,request,format=None):
        new_test = SSCKlassTest.objects.filter(creator =
                                               self.request.user).order_by('published')[:3]
        test_details = {}
        max_marks = 0
        counter = 0
        for test in new_test:
            for quest in test.sscquestions_set.all():
                max_marks = max_marks + quest.max_marks
                counter = counter + 1
            student_marks = SSCOnlineMarks.objects.filter(test = test)
            taken_students = len(student_marks)
            all_marks = []
            for stu in student_marks:
                all_marks.append((stu.marks/max_marks)*100)
            try:
                average_marks = sum(all_marks)/len(all_marks)
            except:
                average_marks = 0


            test_details[test.id] =\
                    {'published':test.published,'num_questions':counter,'total_marks':max_marks,'class':test.klas.name,'subject':test.sub,'average':average_marks,'students_taken':taken_students}
        return Response(test_details)


