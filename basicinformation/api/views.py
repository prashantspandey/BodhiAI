from rest_framework import generics
from django.utils import timezone
from celery.result import AsyncResult 
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from basicinformation.models import *
from django.http import Http404, HttpResponse
from .serializers import *
from QuestionsAndPapers.api.views import *
from basicinformation.marksprediction import *
from QuestionsAndPapers.models import *
from basicinformation.models import *
from basicinformation.marksprediction import *
import json
from basicinformation.nameconversions import *
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticated
)
from basicinformation.tasks import *
import datetime


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


class StudentShowDetialsAPIView(APIView):
    def get(self,request,format=None):
        try:
            my_profile = StudentDetails.objects.get(student = self.request.user)
            serializer_student_profile =\
            StudentProfileDetailsSerializer(my_profile)
            return Response(serializer_student_profile.data)
        except Exception as e:
            print(str(e))
            context =\
            {"id":None,"fullName":None,"phone":None,"address":None,"email":None,"fatherName":None,"parentPhone":None}
            return Response(context)


class StudentFillDetailsAPIView(APIView):
    def post(self,request,*args,**kwargs):
        name = request.POST['fullName']
        phone = request.POST['phone']
        address = request.POST['address']
        fatherName = request.POST['fathersName']
        parentPhone = request.POST['parentPhone']
        email = request.POST['email']
        try:
            my_profile = StudentDetails.objects.get(student =
                                                    self.request.user)
        except:

            my_profile = StudentDetails()
        my_profile.student = self.request.user
        my_profile.address = address
        my_profile.email = email
        my_profile.phone = phone
        my_profile.parentPhone = parentPhone
        my_profile.fatherName = fatherName
        my_profile.fullName = name
        my_profile.save()
        serialzer = StudentProfileDetailsSerializer(my_profile)
        return Response(serialzer.data)
        

#----------------------------------------------------------------------------------------
# Find out if student of teacher
class TeacherorStudentAPIView(APIView):
    def get(self,request,format = None):
        user = self.request.user
        user_type =user.groups.all()[0]
        user_type = user_type.name
        context = {'userType':user_type}
        return Response(context)
# ALL TEACHER APIs

#----------------------------------------------------------------------------------------
# returns the details about the last test created by teacher.

class LastClassTestPerformanceTeacherAPI(APIView):
    def get(self,request,format = None):
        #me = Teach(self.request.user)
        new_test =\
        SSCKlassTest.objects.filter(creator=self.request.user).order_by('published')[0]
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
                        weak_links[i]= \
                        me.online_problematicAreasNames(self.request.user,sub,i)
                        kk = me.online_problematicAreasNames(self.request.user,sub,i)
                        kk = kk.tolist()
                        weak_subs.append(weak_links[i])

                        weak_klass.append(i)
                        subs.append(sub)


                        #print(weak_links)
                        #print(weak_subs)
                    except Exception as e:
                        print(str(e))
            weak_subs_areas = list(zip(subs,weak_klass,weak_subs))
            print(type(weak_subs_areas))
            #weak_subs_areas = None
        except:
            weak_subs_areas = None


        return Response(weak_subs_areas)

#---------------------------------------------------------------------------------------


# returns the names of  weak areas by subject and batch taught by the teacher.
class TeacherWeakAreasBriefAndroid(APIView):
    def get(self,request,format=None):
        res = TeacherWeakAreasBriefAsync.delay(self.request.user.id)
        te_id = res.task_id
        res_final = AsyncResult(te_id)
        ars = res_final.get()
        ars_encode = bytes(ars,'utf-8')
        ars_dict = pickle.loads(ars_encode)
        return Response(ars_dict)








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
                    {'published':test.published,'num_questions':counter,'total_marks':max_marks,'class':test.klas.name,'subject':test.sub,'average':round(average_marks,2),'students_taken':taken_students}
        return Response(test_details)




#-------------------------------------------------------------------
class TeacherTestsOverviewAndroid(APIView):
    def get(self,request,format=None):
        new_test = SSCKlassTest.objects.filter(creator =
                                               self.request.user).order_by('published')[:3]
        test_details = {}
        max_marks = 0
        all_details = []
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


            test_details =\
                    {'testid':test.id,'published':test.published,'num_questions':counter,'total_marks':max_marks,'class':test.klas.name,'subject':test.sub,'average':round(average_marks,2),'students_taken':taken_students}
            all_details.append(test_details)
        return Response(all_details)


#-------------------------------------------------------------------

# Show hard questions in a test of all tests


#This has been put into celery#
class TeachersHardQuestionsAPIView(APIView):
    def get(self,request,format=None):
        res = TeacherHardQuestionsAsync.delay(self.request.user.id)
        res_id = res.task_id
        quest = AsyncResult(res_id)
        questions = quest.get()
        return Response(questions)

class TeachersHardQuestions3TestsAPIView(APIView):
    def get(self,request,format=None):
        res = TeacherHardQuestionsLast3TestsAsync.delay(self.request.user.id)
        res_id = res.task_id
        quest = AsyncResult(res_id)
        questions = quest.get()
        return Response(questions)




#-------------------------------------------------------------------

class TeacherSubjectsAPIView(APIView):
    def get(self,request,format=None):
        me = Teach(self.request.user)
        subjects = me.my_subjects_names()
        sub_dict = {'subjects':subjects}
        return Response(sub_dict)

class TeacherBatchesAPIView(APIView):
    def get(self,request,format=None):
        me = Teach(self.request.user)
        klasses = me.my_classes_names()
        class_dict = {'Batches':klasses}
        return Response(class_dict)
#-------------------------------------------------------------------
# APIs for teacher performance

class TeacherSelectionAPIView(APIView):
    def post(self,request,*args,**kwargs):
        if 'onlineTestAnalysis' in request.POST:
            which_klass = request.POST['onlineTestAnalysis']
            sub = bring_teacher_subjects_analysis.delay(user.id)
            te_id = sub.task_id
            res = AsyncResult(te_id)
            subs = res.get()
            context = {'subs': subs, 'which_class': which_klass}
            return Response(context)
class TeacherSubjectAPIView(APIView):
    def post(self,request,*args,**kwargs):
        if 'onlineschoolSubject' in request.POST:
            onlineSubject = request.POST['onlineschoolSubject']
            sub = onlineSubject.split(',')[0]
            which_class = onlineSubject.split(',')[1]
            trt = teacher_return_tests.delay(user.id,sub,which_class)
            te_id = trt.task_id
            res = AsyncResult(te_id)
            tests = res.get()
            o_tests = []
            for te in serializers.deserialize('json',tests):
                o_tests.append(te.object)
            context = {'tests': o_tests}
            return Response(context)

class TeacherTestSelectionAPIView(APIView):
    def post(self,request,*args,**kwargs):
        if 'onlinetestid' in request.POST:
            test_id = request.POST['onlinetestid']
            me = Teach(self.request.user)
            # get the number of students who took test
            online_marks =\
            SSCOnlineMarks.objects.filter(test__id=test_id,student__school =
                                          me.profile.school)
        # try to get result table associated with particular test
            try:
                result = TestRankTable.objects.get(test__id = test_id)
        # if no new student has taken the test then simply sort the old rank table
                if len(result.names) == len(online_marks):
                    result = me.combine_rankTable(result)

        # else generate new rank table, sort it and display it
                else:
                    asyn_rt = generate_testRankTable.delay(self.request.user.id,test_id)
                    result = 'None'
                    while result is 'None':
                        try:
                            result = TestRankTable.objects.filter(test__id =\
                                                          test_id).order_by('-time')[0]
                            result = combine_rankTable(result)

                        except :
                            pass
        # if no result table is found associated to particular test then generate
        # new rank table, sort it and display it

            except:
                asyn_rt = generate_testRankTable.delay(user.id,test_id)
                result = 'None'
                while result is 'None':
                    try:
                        result = TestRankTable.objects.filter(test__id =\
                                                      test_id).order_by('-time')[0]
                        result = me.combine_rankTable(result)
                    except: pass

        # try if result loader exists for the given test
        # in case of except
            # if result_loader doesn't exist then-
        # case 1 : teacher is clicking on the analysis for this test for 1st time
        #   hence, create a new result loader with this test
        #   and show it in the template

            try:
                result_loader = SscTeacherTestResultLoader.objects.get(test__id = test_id)
            except:

                new_rl = teacher_test_analysis_new.delay(test_id,user.id)
                te_id = new_rl.task_id
                res = AsyncResult(te_id)
                new_rl = None
                while new_rl is None:
                    try:
                        new_rl = SscTeacherTestResultLoader.objects.get(test__id = test_id)
                    except SscTeacherTestResultLoader.DoesNotExist:
                        pass
                max_marks = new_rl.test.max_marks
                average = new_rl.average
                percent_average = new_rl.percentAverage
                grade_s = new_rl.grade_s
                grade_a = new_rl.grade_a
                grade_b = new_rl.grade_b
                grade_c = new_rl.grade_c
                grade_d = new_rl.grade_d
                grade_e = new_rl.grade_e
                grade_f = new_rl.grade_f
                skipped_quests = new_rl.skipped
                skipped_freq = new_rl.skippedFreq
                sq = list(zip(skipped_quests,skipped_freq))
                freqQuests = new_rl.freqAnswersQuestions
                freqQuestsfreq = new_rl.freqAnswersFreq
                freq = list(zip(freqQuests,freqQuestsfreq))
                pro_quests = new_rl.problemQuestions
                pro_freq  = new_rl.problemQuestionsFreq
                problem_quests = list(zip(pro_quests,pro_freq))

                context = {'om':
                           online_marks,'test':new_rl.test,'average':new_rl.average
                           ,'percentAverage':new_rl.percentAverage,'maxMarks':max_marks,
                           'grade_s':new_rl.grade_s,'grade_a':new_rl.grade_a,'grade_b':new_rl.grade_b,'grade_c':new_rl.grade_c,
                           'grade_d':new_rl.grade_d,'grade_e':new_rl.grade_e,'grade_f':new_rl.grade_f,
                           'freq':freq,'sq':sq,'problem_quests':problem_quests,'ssc':True,'result':result}
                return Response(context)

    # result loader is found but don't know if more students have taken
    # the test, hence compare number of students in result loader with number of
    # online marks calculated above

            saved_marks = result_loader.onlineMarks.all()
            if len(online_marks) == len(saved_marks):
    # case 2 : if no new student has taken the test then just load and display
    # result_loder
                max_marks = result_loader.test.max_marks
                pro_quests = result_loader.problemQuestions
                pro_freq  = result_loader.problemQuestionsFreq
                average = result_loader.average
                percent_average = result_loader.percentAverage
                problem_quests = list(zip(pro_quests,pro_freq))
                grade_s = result_loader.grade_s
                grade_a = result_loader.grade_a
                grade_b = result_loader.grade_b
                grade_c = result_loader.grade_c
                grade_d = result_loader.grade_d
                grade_e = result_loader.grade_e
                grade_f = result_loader.grade_f
                skipped_quests = result_loader.skipped
                skipped_freq = result_loader.skippedFreq
                sq = list(zip(skipped_quests,skipped_freq))
                freqQuests = result_loader.freqAnswersQuestions
                freqQuestsfreq = result_loader.freqAnswersFreq
                freq = list(zip(freqQuests,freqQuestsfreq))
                context = {'om':
                           online_marks,'test':result_loader.test,'average':result_loader.average
                           ,'percentAverage':result_loader.percentAverage,'maxMarks':max_marks,
                           'grade_s':result_loader.grade_s,'grade_a':result_loader.grade_a,'grade_b':result_loader.grade_b,'grade_c':result_loader.grade_c,
                           'grade_d':result_loader.grade_d,'grade_e':result_loader.grade_e,'grade_f':result_loader.grade_f,
                           'freq':freq,'sq':sq,'problem_quests':problem_quests,'ssc':True,'result':result}
                return response(context)
    # case 3 : if more students have taken the test then result_loader has to be
    # updated and then displyed in the template
            else:
                new_rl = teacher_test_analysis_already.delay(test_id,user.id)
                rl_id = new_rl.task_id
                max_marks = result_loader.test.max_marks
                pro_quests = result_loader.problemQuestions
                pro_freq  = result_loader.problemQuestionsFreq
                average = result_loader.average
                percent_average = result_loader.percentAverage
                problem_quests = list(zip(pro_quests,pro_freq))
                grade_s = result_loader.grade_s
                grade_a = result_loader.grade_a
                grade_b = result_loader.grade_b
                grade_c = result_loader.grade_c
                grade_d = result_loader.grade_d
                grade_e = result_loader.grade_e
                grade_f = result_loader.grade_f
                skipped_quests = result_loader.skipped
                skipped_freq = result_loader.skippedFreq
                sq = list(zip(skipped_quests,skipped_freq))
                freqQuests = result_loader.freqAnswersQuestions
                freqQuestsfreq = result_loader.freqAnswersFreq
                freq = list(zip(freqQuests,freqQuestsfreq))
                context = {'om':
                           online_marks,'test':result_loader.test,'average':result_loader.average
                           ,'percentAverage':result_loader.percentAverage,'maxMarks':max_marks,
                           'grade_s':result_loader.grade_s,'grade_a':result_loader.grade_a,'grade_b':result_loader.grade_b,'grade_c':result_loader.grade_c,
                           'grade_d':result_loader.grade_d,'grade_e':result_loader.grade_e,'grade_f':result_loader.grade_f,
                           'freq':freq,'sq':sq,'problem_quests':problem_quests,'ssc':True,'result':result}
                return Response(context)

class GenerateRankTableAPIView(APIView):
    def post(self,request,*args,**kwargs):
        test_id = request.POST['onlinetestid']
        me = Teach(self.request.user)
        online_marks =\
        SSCOnlineMarks.objects.filter(test__id=test_id,student__school =
                                      me.profile.school)

    # try to get result table associated with particular test
        try:
            result = TestRankTable.objects.get(test__id = test_id)
    # if no new student has taken the test then simply sort the old rank table
            if len(result.names) == len(online_marks):
                result = me.combine_rankTable(result)
                return Response(result)

    # else generate new rank table, sort it and display it
            else:
                asyn_rt = generate_testRankTable.delay(user.id,test_id)
                result = 'None'
                while result is 'None':
                    try:
                        result = TestRankTable.objects.filter(test__id =\
                                                      test_id).order_by('-time')[0]
                        result = combine_rankTableDict(result)
                        return Response(result)

                    except Exception as e:
                        print(str(e))
    # if no result table is found associated to particular test then generate
    # new rank table, sort it and display it

        except:
            asyn_rt = generate_testRankTable.delay(self.request.user.id,test_id)
            result = 'None'
            while result is 'None':
                try:
                    result = TestRankTable.objects.filter(test__id =\
                                                  test_id).order_by('-time')[0]
                    result = me.combine_rankTableDict(result)
                    return Response(result)
                except Exception as e:
                    print(str(e))

class TeacherTestBasicDetailsAPIView(APIView):
    def post(self,request,*args,**kwargs):
        test_id = request.POST['onlinetestid']
        me = Teach(self.request.user)
        online_marks =\
        SSCOnlineMarks.objects.filter(test__id=test_id,student__school =
                                      me.profile.school)

        try:
            result_loader = SscTeacherTestResultLoader.objects.get(test__id = test_id)
        except:

            new_rl = teacher_test_analysis_new.delay(test_id,user.id)
            te_id = new_rl.task_id
            res = AsyncResult(te_id)
            new_rl = None
            while new_rl is None:
                try:
                    new_rl = SscTeacherTestResultLoader.objects.get(test__id = test_id)
                except SscTeacherTestResultLoader.DoesNotExist:
                    pass
            max_marks = new_rl.test.max_marks
            average = new_rl.average
            percent_average = new_rl.percentAverage
            grade_s = new_rl.grade_s
            grade_a = new_rl.grade_a
            grade_b = new_rl.grade_b
            grade_c = new_rl.grade_c
            grade_d = new_rl.grade_d
            grade_e = new_rl.grade_e
            grade_f = new_rl.grade_f
            context =\
            {'maxMarks':max_marks,'average':average,'percent_average':percent_average,'grade_s':grade_s,'grade_a':grade_a,'grade_b':grade_b,'grade_c':grade_c,'grade_d':grade_d,'grade_e':grade_e,'grade_f':grade_f}
            return Response(context)
        saved_marks = result_loader.onlineMarks.all()
        if len(online_marks) == len(saved_marks):
            max_marks = result_loader.test.max_marks
            average = result_loader.average
            percent_average = result_loader.percentAverage
            grade_s = result_loader.grade_s
            grade_a = result_loader.grade_a
            grade_b = result_loader.grade_b
            grade_c = result_loader.grade_c
            grade_d = result_loader.grade_d
            grade_e = result_loader.grade_e
            grade_f = result_loader.grade_f
            context =\
            {'maxMarks':max_marks,'average':average,'percent_average':percent_average,'grade_s':grade_s,'grade_a':grade_a,'grade_b':grade_b,'grade_c':grade_c,'grade_d':grade_d,'grade_e':grade_e,'grade_f':grade_f}
            return Response(context)
        else:
            new_rl = teacher_test_analysis_already.delay(test_id,user.id)
            rl_id = new_rl.task_id
            max_marks = result_loader.test.max_marks
            average = result_loader.average
            percent_average = result_loader.percentAverage
            grade_s = result_loader.grade_s
            grade_a = result_loader.grade_a
            grade_b = result_loader.grade_b
            grade_c = result_loader.grade_c
            grade_d = result_loader.grade_d
            grade_e = result_loader.grade_e
            grade_f = result_loader.grade_f
            context =\
            {'maxMarks':max_marks,'average':average,'percent_average':percent_average,'grade_s':grade_s,'grade_a':grade_a,'grade_b':grade_b,'grade_c':grade_c,'grade_d':grade_d,'grade_e':grade_e,'grade_f':grade_f}
            return Response(context)

class TeacherTestQuestionsAPIView(APIView):
    def post(self,request,*args,**kwargs):
        test_id = request.POST['onlinetestid']
        me = Teach(self.request.user)
        # get the number of students who took test
        online_marks =\
        SSCOnlineMarks.objects.filter(test__id=test_id,student__school =
                                      me.profile.school)

        try:
            result_loader = SscTeacherTestResultLoader.objects.get(test__id = test_id)
        except:

            new_rl = teacher_test_analysis_new.delay(test_id,user.id)
            te_id = new_rl.task_id
            res = AsyncResult(te_id)
            new_rl = None
            while new_rl is None:
                try:
                    new_rl = SscTeacherTestResultLoader.objects.get(test__id = test_id)
                except SscTeacherTestResultLoader.DoesNotExist:
                    pass
            skipped_quests = new_rl.skipped
            skipped_freq = new_rl.skippedFreq
            sq = list(zip(skipped_quests,skipped_freq))
            freqQuests = new_rl.freqAnswersQuestions
            freqQuestsfreq = new_rl.freqAnswersFreq
            freq = list(zip(freqQuests,freqQuestsfreq))
            pro_quests = new_rl.problemQuestions
            pro_freq  = new_rl.problemQuestionsFreq
            problem_quests = list(zip(pro_quests,pro_freq))
            print(sq,freq)


        saved_marks = result_loader.onlineMarks.all()
        if len(online_marks) == len(saved_marks):
# case 2 : if no new student has taken the test then just load and display
# result_loder
            pro_quests = result_loader.problemQuestions
            pro_freq  = result_loader.problemQuestionsFreq
            problem_quests = list(zip(pro_quests,pro_freq))
            skipped_quests = result_loader.skipped
            skipped_freq = result_loader.skippedFreq
            sq = list(zip(skipped_quests,skipped_freq))
            freqQuests = result_loader.freqAnswersQuestions
            freqQuestsfreq = result_loader.freqAnswersFreq
            freq = list(zip(freqQuests,freqQuestsfreq))
            print(sq,freq)
        else:
            new_rl = teacher_test_analysis_already.delay(test_id,user.id)
            rl_id = new_rl.task_id
            pro_quests = result_loader.problemQuestions
            pro_freq  = result_loader.problemQuestionsFreq
            problem_quests = list(zip(pro_quests,pro_freq))
            skipped_quests = result_loader.skipped
            skipped_freq = result_loader.skippedFreq
            sq = list(zip(skipped_quests,skipped_freq))
            freqQuests = result_loader.freqAnswersQuestions
            freqQuestsfreq = result_loader.freqAnswersFreq
            freq = list(zip(freqQuests,freqQuestsfreq))
            print(sq,freq)


class TeacherWeakAreasDetailAPIView(APIView):
    def post(self,request,*args,**kwargs):
        req = request.POST['weakAreas']
        which_class = req.split(',')[0]
        which_sub = req.split(',')[1]
        user = request.user
        me = Teach(user)
        res = \
        me.online_problematicAreaswithIntensityAverage(user,which_sub,which_class)
        res = me.change_topicNumbersNamesWeakAreas(res,which_sub)
        timing,freq_timing = me.weakAreas_timing(user,which_sub,which_class)
        timing = me.change_topicNumbersNamesWeakAreas(timing,which_sub)
        context =\
        {'which_class':which_class,'probAreas':res,'timing':timing}
        return Response(context)




#-------------------------------------------------------------------
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
                    strongAreas.append(str(i))
                    strongFreq.append(round(j,1))
            except Exception as e:
                print(str(e))
            #if freq == 0:
            #   context = {'noMistake':'noMistake'}
            #   return render(request,'basicinformation/student_weakAreas.html',context)
            # changing topic categories numbers to names
            freq_Names = me.changeTopicNumbersNames(freq,subject)

            print('{} skill names'.format(freq_Names))
            skills = list(zip(strongAreas,strongFreq))
            skills_names = me.changeTopicNumbersNames(skills,subject)
            if skills_names == None:
                continue
            strong_areas[subject] = {'strongTopics':skills_names}
        return Response(strong_areas)


class StudentTopicWiseProficiencyAndroid(APIView):
    def get(self,request,format=None):
        me = Studs(self.request.user)
        subjects = get_subject(self.request.user)
        strong_areas = {}
        overall = []
        for subject in subjects:
            freq = me.weakAreas_IntensityAverage(subject)
            strongAreas = []
            strongFreq = []
            try:
               for i,j in freq:
                    strongAreas.append(str(i))
                    strongFreq.append(round(j,1))
            except Exception as e:
                print(str(e))
            if freq == 0:
               context = {'noMistake':'noMistake'}
               return render(request,'basicinformation/student_weakAreas.html',context)
            # changing topic categories numbers to names
            freq_Names = me.changeTopicNumbersNames(freq,subject)
            skills = list(zip(strongAreas,strongFreq))
            skills_names = me.changeTopicNumbersNames(skills,subject)
            if skills_names == None:
                continue
            strong_areas = {'subject':subject,'strongTopics':skills_names}
            overall.append(strong_areas)
        return Response(overall)


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
                    {'subject':m.test.sub,'percent':round(percent,1),'attempted':attempted,'rightAnswers':right,'wrongAnswers':wrong,'total_questions':total_questions,'published':published,'time':time,'testid':m.test.id,'answer_id':m.id}
            all_marks.append(marks_dic)

        return Response(all_marks)


#---------------------------------------------------------------------

# Show average time taken to solve a questions in each topic

class StudentAverageTimeTopicAPIView(APIView):
    def get(self,request,format=None):
        me = Studs(self.request.user)
        subjects = get_subject(self.request.user)
        #average_timing_dict = {}
        timing = []
        for subject in subjects:
            timing_areawise,freq_timer = me.areawise_timing(subject)
            freq_timer = me.changeTopicNumbersNames(freq_timer,subject)
            timing_names = me.changeTopicNumbersNames(timing_areawise,subject)
            timing.append(timing_names)
        return Response(timing)


#---------------------------------------------------------------------
class StudentAverageTimeTopicAndroidAPIView(APIView):
    def get(self,request,format=None):
        me = Studs(self.request.user)
        subjects = get_subject(self.request.user)
        average_timing_dict = {}
        timing = []
        for subject in subjects:
            timing_areawise,freq_timer = me.areawise_timing(subject)
            freq_timer = me.changeTopicNumbersNames(freq_timer,subject)
            timing_names = me.changeTopicNumbersNames(timing_areawise,subject)
            if timing_names == None:
                continue
            average_timing_dict =\
            {'subject':subject,'topics_timing':timing_names}
            timing.append(average_timing_dict)
        return Response(timing)


# Student performance API
#---------------------------------------------------------------------
class StudentPerformanceBatchesAPIView(APIView):
    def get(self,request,format=None):
        me = Teach(self.request.user)
        all_klasses = me.my_classes_names_cache()
        my_batches = {'myBatches':all_klasses}
        return Response(my_batches)

#---------------------------------------------------------------------
# TimeTable APIs
#---------------------------------------------------------------------
class TeacherTimeTableAPIView(APIView):
    def get(self,request,format=None):
        me = Teach(self.request.user)
        time_table = TimeTable.objects.filter(teacher = me.profile,active=True)
        serialzer =TimeTableModelSerializer(time_table,many=True)
        return Response(serialzer.data)


class TeacherTimeTableFirst(APIView):
    def get(self,request,format=None):
        me = Teach(self.request.user)
        batches = me.my_classes_names_cache()
        context = {'batches':batches}
        return Response(context)


class TeacherCreateTimeTable(APIView):
    def post(self,request,*args,**kwargs):
        me = Teach(self.request.user)
        date = request.POST['timetable_date']
        note = request.POST['timetable_note']
        timeStart = request.POST['timetable_timeStart']
        timeEnd = request.POST['timetable_timeEnd']
        batch = request.POST['timetable_batch']
        subject = request.POST['timetable_sub']
        time_table = TimeTable()
        date = datetime.datetime.strptime(date,"%m-%d-%Y")
        final_date = date.date()
        batch = klass.objects.get(school = me.my_school(),name=batch)
        my_subjects = me.my_subjects_names()
        time_table.batch = batch
        time_table.date = final_date
        time_table.timeStart = timeStart
        time_table.timeEnd = timeEnd
        time_table.note = note
        time_table.teacher = me.profile
        time_table.created = timezone.now()
        if subject in my_subjects:
            time_table.sub = subject
            time_table.save()
            serialzer = TimeTableModelSerializer(time_table)
            return Response(serialzer.data)
        else:
            context = {'error':'There was some error'}
            return Response(context)

class StudentShowTimeTableAPIView(APIView):
    def get(self,request,format=None):
        me = Studs(self.request.user)
        batch = me.get_batch()
        all_time_tables = []
        all_time_tables_serializer = []
        time_table = TimeTable.objects.filter(batch = batch)
        for time_tab in time_table:
            all_time_tables.append(TimeTableModelSerializer(time_tab).data)
        return Response(all_time_tables)


class StudentTestPerformanceDetailedAPIView(APIView):
    def post(self,request,*args,**kwargs):
        test_id = request.POST['test_id']
        sub = request.POST['subject']
        me = Studs(self.request.user)
        #visible_tests(test_id)
        try:
            test = SSCOfflineMarks.objects.get(student=me.profile, test__id=test_id)
            mode = 'offline'
        except:
            test = SSCOnlineMarks.objects.get(student=me.profile, test__id=test_id)
            te = SSCKlassTest.objects.get(id = test_id)
            mode = 'online'

        student_type = 'SSC'
        if mode == 'online':
# Look for a cached test analyis , if found then show it
# if there is a change in number of tests then just update a few things and
# show it
# If cache not found then calculate the fields, create a cached version and
# show it on front end.
            try:
                te = SSCKlassTest.objects.get(id = test_id)
                analysis = StudentTestAnalysis.objects.get(student =\
                                                           me.profile,test =te)
                myPercent = analysis.myPercent
                classAverage = analysis.klassAverage
                classAveragePercent = analysis.klassAveragePercent
                myPercentile = analysis.myPercentile
                allKlassMarks = analysis.allKlassMarks
                freqAnswerId = analysis.freqAnswerId
                freqAnswer = analysis.freqAnswer
                freq = list(zip(freqAnswerId,freqAnswer))
                weakCategories = analysis.weakCategories
                weakAccuracies = analysis.weakAccuracies
                weak_areas = list(zip(weakCategories,weakAccuracies))
                numRight = analysis.numRight
                numWrong = analysis.numWrong
                numSkipped = analysis.numSkipped
                overallAccuracy = analysis.overallAccuracy
                subjectwiseAccuracySub = analysis.subjectwiseAccuracySub
                subjectwiseAccuracy = analysis.subjectwiseAccuracy
                subjectwise_acc =\
                list(zip(subjectwiseAccuracySub,subjectwiseAccuracy))
                areaTimeCategory = analysis.areaTimeCategory
                areaTime = analysis.areaTime
                area_timing = list(zip(areaTimeCategory,areaTime))
                hours = analysis.hour
                mins = analysis.minute
                seconds = analysis.second
                if hours == 0:
                    tt = '{} minutes and {} seconds'.format(mins,seconds)
                if hours == 0 and mins == 0:
                    tt = '{} seconds'.format(seconds)
                if hours > 0:
                    tt = '{} hours {} minutes and {}\
                    seconds'.format(hours,mins,seconds)

                if sub == 'SSCMultipleSections':
                    weak_names = weak_areas
                    timing = area_timing
                else:
                    weak_names = me.changeTopicNumbersNames(weak_areas,sub)
                    timing = me.changeTopicNumbersNames(area_timing,sub)
                if len(tests) != len(allKlassMarks):
                    percentile, all_marks = me.online_findPercentile(test_id)
                    average, percent_average = \
                        me.online_findAverageofTest(test_id, percent='p')
                    percentile = percentile * 100
                    all_marks = [((i / test.test.max_marks) * 100) for i in all_marks]
                    analysis.myPercentile = percentile
                    analysis.allKlassMarks = all_marks
                    analysis.klassAverage = average
                    analysis.klassAveragePercent = percent_average
                    analysis.save()
                    allKlassMarks = all_marks
                    myPercentile = percentile
                    classAverage = average
                    classAveragePercent = percent_average
                test_serializer = SSCOnlineMarksSerializer(test)
                context = \
                    {'test': test_serializer.data, 'average': classAverage,
                     'percentAverage': classAveragePercent,
                     'my_percent': myPercent, 'percentile': myPercentile,
                     'allMarks': allKlassMarks,
                     'freq':\
                     freq,'topicTiming':timing,
                     'numberRight':numRight,'numberWrong':numWrong,'numberSkipped':numSkipped,'accuracy':overallAccuracy,'subjectwise_accuracy':subjectwise_acc,'tt':tt}
                return \
                    Response(context)




            except Exception as e:
                print(str(e))
                old_analysis = StudentTestAnalysis.objects.filter(student =\
                                                           me.profile,test =te)
                if len(old_analysis) > 1:
                    for i in old_analysis:
                        i.delete()

                analysis = StudentTestAnalysis()
                my_marks_percent = (test.marks / test.test.max_marks) * 100
                analysis.myPercent = my_marks_percent
                average, percent_average = \
                    me.online_findAverageofTest(test_id, percent='p')
                analysis.klassAverage = average
                analysis.klassAveragePercent = percent_average
                percentile, all_marks = me.online_findPercentile(test_id)
                percentile = percentile * 100
                analysis.myPercentile = percentile

                all_marks = [((i / test.test.max_marks) * 100) for i in all_marks]
                analysis.allKlassMarks = all_marks

                freq = me.online_QuestionPercentage(test_id)
                freq_id = []
                freq_freq = []
                for i,j in freq:
                    freq_id.append(i)
                    freq_freq.append(j)
                analysis.freqAnswerId = freq_id
                analysis.freqAnswer = freq_freq
                # converting test time seconds to hours and minutes
                test_totalTime = test.timeTaken
                hours = int(test_totalTime/3600)
                t = int(test_totalTime%3600)
                mins = int(t/60)
                seconds =int(t%60)
                if hours == 0:
                    tt = '{} minutes and {} seconds'.format(mins,seconds)
                    analysis.hour = 0
                    analysis.minute = mins
                    analysis.second = seconds
                if hours == 0 and mins == 0:
                    tt = '{} seconds'.format(seconds)
                    analysis.hour = 0
                    analysis.minute = 0
                    analysis.second = seconds

                if hours > 0:
                    tt = '{} hours {} minutes and {}\
                    seconds'.format(hours,mins,seconds)
                    analysis.hour = hours
                    analysis.minute = mins
                    analysis.second = seconds

                try:
                    if tt:
                        pass
                except:
                    tt = None

                ra,wa,sp,accuracy = me.test_statistics(test_id)
                analysis.numRight = ra
                analysis.numWrong = wa
                analysis.numSkipped = sp
                analysis.overallAccuracy = accuracy
                weak_areas = me.weakAreas_Intensity(sub,singleTest = test_id)
                weak_cat = []
                weak_acc = []
                for i,j in weak_areas:
                    weak_cat.append(i)
                    weak_acc.append(j)
                analysis.weakCategories = weak_cat
                analysis.weakAccuracies = weak_acc
                sk_weak = me.skipped_testwise(test_id,me.profile)
                area_timing,freq = me.areawise_timing(sub,test_id)
                weak_time_cat = []
                weak_time = []
                for k,v in area_timing:
                    weak_time_cat.append(k)
                    weak_time.append(v)
                analysis.areaTimeCategory = weak_time_cat
                analysis.areaTime = weak_time
                subjectwise_accuracy = me.test_SubjectAccuracy(test_id)
                sub_weak = []
                sub_weak_acc = []
                for i,j in subjectwise_accuracy.items():
                    sub_weak.append(i)
                    sub_weak_acc.append(j)
                analysis.subjectwiseAccuracySub = sub_weak
                analysis.subjectwiseAccuracy = sub_weak_acc
                analysis.student = me.profile
                analysis.test = te
                analysis.save()

                if sub == 'SSCMultipleSections':
                    weak_names = weak_areas
                    timing = area_timing
                else:
                    weak_names = me.changeTopicNumbersNames(weak_areas,sub)
                    timing = me.changeTopicNumbersNames(area_timing,sub)
                test_serializer = SSCOnlineMarksSerializer(test)

                context = \
                    {'thistest': test_serializer.data, 'average': average, 'percentAverage': percent_average,
                     'my_percent': my_marks_percent, 'percentile': percentile, 'allMarks': all_marks,
                     'freq':\
                     freq,'student_type':student_type,'topicWeakness':weak_names,'topicTiming':timing,
                     'numberRight':ra,'numberWrong':wa,'numberSkipped':sp,'accuracy':accuracy,'subjectwise_accuracy':subjectwise_accuracy,'tt':tt}
                return \
                    Response(context)

class StudentFindMyRankAPIView(APIView):
    def get(self,request,format=None):
        me = Studs(self.request.user)
        my_tests = SSCOnlineMarks.objects.filter(student = me.profile)
        all_ids = []
        all_context = []
        for i in my_tests:
            all_ids.append(i.test.id)
        for teid in all_ids:
            context = me.find_my_rank(teid)
           
            all_context.append(context)
        if len(all_context) == 0:
            all_context = {'NoTest':"Please take at-least one test so that we can calculate your rank.\
            कृपया एक टेस्ट लीजिये ताकि हम आपकी रैंक पता लगा पायें "}
            return Response(all_context)
        else:
            return Response(all_context)


class TeacherShowAllStudentsAPIView(APIView):
    def get(self,request,format=None):
        me = Teach(self.request.user)

        my_students = Student.objects.filter(school = me.my_school())
        number_students = len(my_students)
        student_serializer = StudentModelSerializer(my_students,many=True)
        context =\
        {'students':student_serializer.data,'number_students':number_students}
        return Response(context)


class StudentAverageTimingDetailAPIView(APIView):
    def post(self,request,*args,**kwargs):
        me = Studs(self.request.user)

        subject = request.POST['subject']
        chapter = request.POST['chapter']
        average_timing = request.POST['average_timing']
        chapter = changeIndividualNumberNames(chapter,subject)
        print('chapter {}'.format(chapter))
        result = me.student_weak_timing_details(me.profile.id,subject,chapter)
        context = {'result':result,'overall_average_timing':average_timing}
        return Response(context)


class TeacherAnalysisShowTestsAPIView(APIView):
    def post(self,request,*args,**kwargs):
        subject = request.POST['subject']
        batch = request.POST['batch']
        all_tests = SSCKlassTest.objects.filter(creator = self.request.user)
        all_ids = []
        all_dates = []
        all_test_dict = {}
        for i in all_tests:
            all_ids.append(i.id)
            all_dates.append(i.published)
        overall_list = list(zip(all_ids,all_dates))
        all_test_dict = {'ids':overall_list}
        return Response(all_test_dict)

class TeacherAnalysisIndividualSendStudentAPIView(APIView):
    def post(self,request,*args,**kwargs):
        test_id = request.POST['test_id']
        mark = SSCOnlineMarks.objects.filter(test__id = test_id)
        students = []
        for i in mark:
            serializer = StudentModelSerializer(i.student)
            students.append(serializer.data)
        context = {'students':students}

        return Response(context)


class TeacherAnalysisIndividualStudentAPIView(APIView):
    def post(self,request,*args,**kwargs):
        me = Teach(self.request.user)
        test_id = request.POST['test_id']
        student_id = request.POST['student_id']
        student = Student.objects.get(id = int(student_id))
        mark = SSCOnlineMarks.objects.get(test__id = test_id,student = student)
        serializer = SSCOnlineMarksSerializer(mark)
        return Response(serializer.data)

class StudentShowPerformanceSubjectsAPIView(APIView):
    def get(self,request,format=None):
        me = Studs(self.request.user)
        subjects = me.already_takenTests_Subjects()
        context = {'subjects':subjects}
        return Response(context)

class StudentShowPerformanceTestsAPIView(APIView):
    def post(self,request,*args,**kwargs):
        me = Studs(self.request.user)
        subject = request.POST['subject']
        tests = SSCOnlineMarks.objects.filter(student =
                                              me.profile,test__sub = subject)
        test_date = []
        test_id = []
        for i in tests:
            test_date.append(i.testTaken)
            test_id.append(i.id)

        test_details = list(zip(test_id,test_date))
        context = {'test_details':test_details}
        return Response(context)


