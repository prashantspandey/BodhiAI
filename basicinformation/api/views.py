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

# ALL TEACHER APIs

#----------------------------------------------------------------------------------------
# returns the details about the last test created by teacher.

class LastClassTestPerformanceTeacherAPI(APIView):
    def get(self,request,format = None):
        #me = Teach(self.request.user)
        new_test = SSCKlassTest.objects.filter(creator =
                                              self.request.user).order_by('published')[3]
        counter = 0
        quest_marks = 0
        test_id = new_test.id
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
            marks.append((test.marks/test.test.max_marks)*100)
        info =\
                {'subject':subject,'date':publised_date,'test_takers':len(my_tests),'marks':marks,'num_questions':counter,'test_id':test_id}
        return Response(info)

#---------------------------------------------------------------------------------------

# returns the names of  weak areas by subject and batch taught by the teacher.
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

#---------------------------------------------------------------------------------------

# returns details about last few tests given out by the teacher(eg. date
# published,total marks,subject,class,number of students who have taken the
# test etc...)


class TeacherTestsOverview(APIView):
    def get(self,request,format=None):
        new_test = SSCKlassTest.objects.filter(creator =
                                               self.request.user).order_by('published')[:3]
        test_details = {}
        max_marks = 0
        for test in new_test:
            max_marks = test.max_marks
            counter = len(test.sscquestions_set.all())
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

# ALL STUDENT APIs



# Helper functions for Students APIs
#-------------------------------------------------------------------
def get_subject(user):
    me = Studs(user)
    taken_tests =\
    SSCOnlineMarks.objects.filter(student=me.profile).order_by('testTaken')
    prev_performance = {}
    subjects = []
    for test in taken_tests:
        subjects.append(test.test.sub)
    subjects = list(unique_everseen(subjects))
    return subjects

#--------------------------------------------------------------------
# returns the marks of all the tests taken by student.

class StudentPreviousPerformanceBriefAPIView(APIView):
    def get(self,request,format=None):
        me = Studs(self.request.user)
        taken_tests =\
        SSCOnlineMarks.objects.filter(student=me.profile).order_by('testTaken')
        prev_performance = {}
        subjects = []
        for test in taken_tests:
            subjects.append(test.test.sub)
        subjects = list(unique_everseen(subjects))
        for sub in subjects:
            marks = []
            date = []
            for test in taken_tests:
                if test.test.sub == sub:
                    percentage = (test.marks/test.test.max_marks)*100
                    marks.append(percentage)
                    date.append(test.testTaken)
                prev_performance[sub]  = {'marks':marks,'date':date}
        return Response(prev_performance)


#---------------------------------------------------------------------
#Same as above but for android

class StudentPreviousPerformanceBriefAndroidAPIView(APIView):
    def get(self,request,format=None):
        me = Studs(self.request.user)
        taken_tests =\
        SSCOnlineMarks.objects.filter(student=me.profile).order_by('testTaken')
        past_performance = []
        prev_performance = {}
        overall = {}
        subjects = []
        for test in taken_tests:
            subjects.append(test.test.sub)
        subjects = list(unique_everseen(subjects))
        for sub in subjects:
            marks = []
            date = []
            for test in taken_tests:
                if test.test.sub == sub :
                    percentage = (test.marks/test.test.max_marks)*100
                    marks.append(percentage)
                    date.append(test.testTaken)
                prev_performance= {'subject':sub,'marks':marks, 'date':date}
            past_performance.append(prev_performance)
        return Response(past_performance)

#---------------------------------------------------------------------

# Gets all the area proficiecy in all the subjects a student studies

class StudentTopicWiseProficiency(APIView):
    def get(self,request,format=None):
        me = Studs(self.request.user)
        subjects = get_subject(self.request.user)
        strong_areas = {}
        for subject in subjects:

            freq = me.weakAreas_IntensityAverage(subject)
            strongAreas = []
            strongFreq = []
            try:
               for i,j in freq:
                    strongAreas.append(i)
                    calc = float(100-j)
                    strongFreq.append(round(calc,1))
            except Exception as e:
                print(str(e))
            if freq == 0:
               context = {'noMistake':'noMistake'}
               return render(request,'basicinformation/student_weakAreas.html',context)
            # changing topic categories numbers to names
            freq_Names = me.changeTopicNumbersNames(freq,subject)
            skills = list(zip(strongAreas,strongFreq))
            skills_names = me.changeTopicNumbersNames(skills,subject)
            strong_areas[subject] = {'strongTopics':skills_names}
        return Response(strong_areas)



#---------------------------------------------------------------------

# Shows basic details of taken test by students 

class StudentTakenTestsDetailsAPIView(APIView):
    def get(self,request,format=None):
        me = Studs(self.request.user)
        marks = SSCOnlineMarks.objects.filter(student=
                                              me.profile).order_by('test__published')
        marks_dic = {}
        all_marks = []
        #percent = []
        #attempted = []
        #right = []
        #wrong = []
        for m in marks:
            percent_calc = ((m.marks/m.test.max_marks)*100)
            percent = percent_calc
            attempted = (len(m.allAnswers))
            right = (len(m.rightAnswers))
            wrong = (len(m.wrongAnswers))
            published = m.testTaken
            time = m.timeTaken
            total_questions = len(m.test.sscquestions_set.all())
            marks_dic =\
                    {'subject':m.test.sub,'percent':round(percent,1),'attempted':attempted,'rightAnswers':right,'wrongAnswers':wrong,'total_questions':total_questions,'published':published,'time':time}
            all_marks.append(marks_dic)

        return Response(all_marks)


#---------------------------------------------------------------------

# Show average time taken to solve a questions in each topic

class StudentAverageTimeTopicAPIView(APIView):
    def get(self,request,format=None):
        me = Studs(self.request.user)
        subjects = get_subject(self.request.user)
        timing = []
        for subject in subjects:
            timing_areawise,freq_timer = me.areawise_timing(subject)
            freq_timer = me.changeTopicNumbersNames(freq_timer,subject)
            timing_names = me.changeTopicNumbersNames(timing_areawise,subject)
            timing.append(timing_names)
        return Response(timing)


#---------------------------------------------------------------------









