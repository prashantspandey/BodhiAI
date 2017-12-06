import numpy as np
import pickle
import math
import itertools
from datetime import datetime, date
from django.utils import timezone
from .models import Subject
from more_itertools import unique_everseen
from QuestionsAndPapers.models import *
from xhtml2pdf import pisa
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.db.models import Q
#'''
#load pickles for data transformation and prediction (hindi)
#'''
#pickle_in_hindi =  open('basicinformation/preprocesshindihy.pickle','rb')
#svm_pickle_hindi = open('basicinformation/svmhindihhy.pickle', 'rb')
#sca_hindi = pickle.load(pickle_in_hindi)
#svmhindihhy = pickle.load(svm_pickle_hindi)
#
#'''
#load pickles for data transformation and prediction (maths)
#'''
#pickle_in_maths = open('basicinformation/preprocesshindihy.pickle', 'rb')
#knn7_pickle_maths = open('basicinformation/svmhindihhy.pickle', 'rb')
#sca_maths = pickle.load(pickle_in_maths)
#knn7mathshhy = pickle.load(knn7_pickle_maths)
#
#'''
#load pickles for data transformation and prediction (english)
#'''
#pickle_in_english = open('basicinformation/preprocesshindihy.pickle', 'rb')
#knn7_pickle_english = open('basicinformation/svmhindihhy.pickle', 'rb')
#sca_english = pickle.load(pickle_in_english)
#knn7englishhhy = pickle.load(knn7_pickle_english)
#
#'''
#load pickles for data transformation and prediction (science)
#'''
#pickle_in_science = open('basicinformation/preprocesshindihy.pickle', 'rb')
#knn7_pickle_science = open('basicinformation/svmhindihhy.pickle', 'rb')
#sca_science = pickle.load(pickle_in_science)
#knn7sciencehhy = pickle.load(knn7_pickle_science)

# test1,test2,test3,age,section
# x = np.array([[9, 10, 10, 12, 1]])
# x = sca.transform(x)
# print(x)
# prd = svmhindihhy.predict(x)
# print(prd)


def hindi_3testhyprediction(test1, test2, test3, DOB, section):
    '''
    convert test marks into numpy arrays
    '''
    t1 = int(test1)
    t2 = int(test2)
    t3 = int(test3)

    if section == 'a':
        section = 1
    elif section == 'b':
        section = 2

    '''
    calculate age using DOB (dd/mm/year)
    '''
    days_in_year = 365.2425
    age = int((date(2018, 4, 1) - DOB).days / days_in_year)
    # age = int((date.today() - DOB).days / days_in_year)

    overall = np.array([[t1, t2, t3, age, section]])

    '''
        transform(scale) data to original data of school
    '''
    overall = sca_hindi.transform(overall)
    '''
        predict the hy marks using the trained ml algorithm
    '''
    prediction = svmhindihhy.predict(overall)
    return prediction


def maths_3testhyprediction(test1, test2, test3, DOB, section):
    '''
    convert test marks into numpy arrays
    '''
    t1 = int(test1)
    t2 = int(test2)
    t3 = int(test3)

    if section == 'a':
        section = 1
    elif section == 'b':
        section = 2

    '''
        calculate age using DOB (dd/mm/year)
    '''
    days_in_year = 365.2425
    age = int((date(2018, 4, 1) - DOB).days / days_in_year)

    overall = np.array([[t1, t2, t3, age, section]])

    '''
        transform(scale) data to original data of school
    '''
    overall = sca_maths.transform(overall)
    '''
        predict the hy marks using the trained ml algorithm
    '''
    prediction = knn7mathshhy.predict(overall)
    return prediction


def english_3testhyprediction(test1, test2, test3, DOB, section):
    '''
    convert test marks into numpy arrays
    '''
    t1 = int(test1)
    t2 = int(test2)
    t3 = int(test3)

    if section == 'a':
        section = 1
    elif section == 'b':
        section = 2

    '''
        calculate age using DOB (dd/mm/year)
    '''
    days_in_year = 365.2425
    age = int((date(2018, 4, 1) - DOB).days / days_in_year)

    overall = np.array([[t1, t2, t3, age, section]])

    '''
        transform(scale) data to original data of school
    '''
    overall = sca_english.transform(overall)
    '''
        predict the hy marks using the trained ml algorithm
    '''
    prediction = knn7englishhhy.predict(overall)
    return prediction


def science_3testhyprediction(test1, test2, test3, DOB, section):
    '''
    convert test marks into numpy arrays
    '''
    t1 = int(test1)
    t2 = int(test2)
    t3 = int(test3)

    if section == 'a':
        section = 1
    elif section == 'b':
        section = 2

        '''
            calculate age using DOB (dd/mm/year)
        '''
    days_in_year = 365.2425

    age = int((date(2018, 4, 1) - DOB).days / days_in_year)

    overall = np.array([[t1, t2, t3, age, section]])

    '''
        transform(scale) data to original data of school
    '''
    overall = sca_science.transform(overall)
    '''
        predict the hy marks using the trained ml algorithm
    '''
    prediction = knn7sciencehhy.predict(overall)
    return prediction


def predictionConvertion(prediction):
    try:
        prediction = prediction[0]
    except:
        pass

    if prediction == 0:
        conversion = 35
    elif prediction == 1:
        conversion = 45
    elif prediction == 2:
        conversion = 55
    elif prediction == 3:
        conversion = 65
    elif prediction == 4:
        conversion = 75
    elif prediction == 5:
        conversion = 85
    elif prediction == 6:
        conversion = 95
    else:
        conversion = '404'
    return conversion


# function for updating all the half yearly predictions (whole database)


def update_all_predictedmarks():
    subject = Subject.objects.all()
    alluniquestudents = []
    alluniquestudents = list(unique_everseen(alluniquestudents))
    for i in subject:
        alluniquestudents.append(i.student)
    allsubjects = []
    for j in alluniquestudents:
        allsubjects.extend(j.subject_set.all())

    for thisSubject in allsubjects:
        if thisSubject.name == 'Hindi':
            cl = str(thisSubject.student.klass)
            if cl[-1] == 'a':
                section = 'a'
            else:
                section = 'b'
            thisSubject.predicted_hy = int(
                hindi_3testhyprediction(thisSubject.test1, thisSubject.test2, thisSubject.test3,
                                        thisSubject.student.dob, section))

            thisSubject.save()
        elif thisSubject.name == 'English':
            cl = str(thisSubject.student.klass)
            if cl[-1] == 'a':
                section = 'a'
            else:
                section = 'b'
            thisSubject.predicted_hy = int(
                english_3testhyprediction(thisSubject.test1, thisSubject.test2, thisSubject.test3,
                                          thisSubject.student.dob, section))
            thisSubject.save()

        elif thisSubject.name == 'Maths':
            cl = str(thisSubject.student.klass)
            if cl[-1] == 'a':
                section = 'a'
            else:
                section = 'b'
            thisSubject.predicted_hy = int(
                maths_3testhyprediction(thisSubject.test1, thisSubject.test2, thisSubject.test3,
                                        thisSubject.student.dob, section))
            thisSubject.save()

        elif thisSubject.name == 'Science':
            cl = str(thisSubject.student.klass)
            if cl[-1] == 'a':
                section = 'a'
            else:
                section = 'b'
            thisSubject.predicted_hy = int(
                science_3testhyprediction(thisSubject.test1, thisSubject.test2, thisSubject.test3,
                                          thisSubject.student.dob, section))
            thisSubject.save()

        else:
            pass


def get_predicted_marks(user, subjects):
    try:
        hindi = subjects.get(name='Hindi')
        predicted_hindihy = predictionConvertion(hindi.predicted_hy)
    except:
        predicted_hindihy = 0
    try:
        maths = subjects.get(name='Maths')
        predicted_mathshy = predictionConvertion(maths.predicted_hy)
    except:
        predicted_mathshy = 0
    try:
        english = subjects.get(name='English')
        predicted_englishhy = predictionConvertion(english.predicted_hy)
    except:
        predicted_englishhy = 0
    try:
        science = subjects.get(name='Science')
        predicted_sciencehy = predictionConvertion(science.predicted_hy)
    except:
        predicted_sciencehy = 0

    return predicted_hindihy, predicted_mathshy, predicted_englishhy, predicted_sciencehy


def averageoftest(test, test2=None, test3=None):
    if test2 is None and test3 is None:
        testmarks = np.array(test)
        return np.mean(testmarks)
    elif test3 is None:
        testmarks = np.array(test)
        testmarks2 = np.array(test2)
        return np.mean(testmarks), np.mean(testmarks2)
    else:
        testmarks = np.array(test)
        testmarks2 = np.array(test2)
        testmarks3 = np.array(test3)
        return np.mean(testmarks), np.mean(testmarks2), np.mean(testmarks3)


# all the helper functions for teacher pages

def teacher_get_students_classwise(req):
    user = req.user
    profile = user.teacher
    subject = profile.subject_set.all()

    allstudents = []  # list of subjects of all students (taught by the teacher)
    klass_dict = {}  # dictionary for subjects of individual classes
    all_klasses = []  # list of all unique classes taught by the teacher
    all_klasses = list(unique_everseen(all_klasses))

    for i in subject:
        allstudents.append(i)
        all_klasses.append(str(i.student.klass))

    # fill out the dictionary for subjects of each class
    for k in all_klasses:
        sub9a = []
        for j in subject:
            if str(j.student.klass) == str(k):
                sub9a.append(j)
                temp_dict = {str(k): sub9a}
                klass_dict.update(temp_dict)
    return klass_dict, all_klasses


def teacher_get_testmarks_classwise(req, klass_dict):
    klass_test1_dict = {}  # dictionary to hold test1 marks of different classes
    klass_test2_dict = {}
    klass_test3_dict = {}

    # fill out the above dictionaries

    for i in klass_dict.values():
        kk = i
        klasstest1 = []
        klasstest2 = []
        klasstest3 = []

        for j in kk:
            klasstest1.append(j.test1)
            klasstest2.append(j.test2)
            klasstest3.append(j.test3)
            testm1 = {str(j.student.klass): klasstest1}
            testm2 = {str(j.student.klass): klasstest2}
            testm3 = {str(j.student.klass): klasstest3}
        klass_test1_dict.update(testm1)
        klass_test2_dict.update(testm2)
        klass_test3_dict.update(testm3)
    return klass_test1_dict, klass_test2_dict, klass_test2_dict


def teacher_get_classwise_studnetNames(request, klass_dict):
    ktdict = {}
    for i in klass_dict.values():
        kk = i
        kt = []
        for k in kk:
            kt.append(k.student)
            stu1 = {str(k.student.klass): kt}
        ktdict.update(stu1)
    return ktdict


def teacher_get_classwise_listofStudents(request, studict):
    kl0 = []
    kl1 = []
    kl2 = []
    kl3 = []
    kl4 = []
    kl5 = []
    nine_a = []
    nine_b = []
    nine_c = []
    ten_a = []
    ten_b = []
    ten_c = []

    for i, n in enumerate(studict.values()):
        eval('kl' + str(i)).extend(n)
    for i in kl0:

        if str(i.klass) == '9th a':
            nine_a = kl0
            break

    for i in kl1:
        if str(i.klass) == '9th b':
            nine_b = kl1
            break
    return nine_a, nine_b


def teacher_listofStudents(profile, klass):
    listofstudents = []
    subject_list = profile.subject_set.filter(student__klass__name=klass)
    for i in subject_list:
        listofstudents.append(i)
    return listofstudents


def teacher_listofStudentsMarks(profile, which_class):
    marks_class_test1 = []
    marks_class_test2 = []
    marks_class_test3 = []
    marks_class_predictedHy = []
    sub_class = profile.subject_set.filter(student__klass__name=which_class)
    if not sub_class:
        pass
    else:
        for i in sub_class:
            if i.test1:
                marks_class_test1.append(i.test1)
            if i.test2:
                marks_class_test2.append(i.test2)
            if i.test3:
                marks_class_test3.append(i.test3)
            if i.predicted_hy:
                marks_class_predictedHy.append(i.predicted_hy)
    return marks_class_test1, marks_class_test2, marks_class_test3, marks_class_predictedHy


def find_grade_from_marks(test1, test2=None, test3=None):
    test1_grade = []
    test2_grade = []
    test3_grade = []
    test1 = np.array(test1)
    if test2 is None:
        for i, n in enumerate(test1):
            if n < 4:
                test1_grade.append('F')
            if 4 <= n < 5:
                test1_grade.append('E')
            if 5 <= n < 6:
                test1_grade.append('D')
            if 6 <= n < 7:
                test1_grade.append('C')
            if 7 <= n < 8:
                test1_grade.append('B')
            if 8 <= n < 9:
                test1_grade.append('A')
            if 9 <= n <= 10:
                test1_grade.append('S')
        return test1_grade
    elif test3 is None:

        test2 = np.array(test2)

        for i, n in enumerate(test1):
            if n < 4:
                test1_grade.append('F')
            if 4 <= n < 5:
                test1_grade.append('E')
            if 5 <= n < 6:
                test1_grade.append('D')
            if 6 <= n < 7:
                test1_grade.append('C')
            if 7 <= n < 8:
                test1_grade.append('B')
            if 8 <= n < 9:
                test1_grade.append('A')
            if 9 <= n <= 10:
                test1_grade.append('S')

        for i, n in enumerate(test2):
            if n < 4:
                test2_grade.append('F')
            if 4 <= n < 5:
                test2_grade.append('E')
            if 5 <= n < 6:
                test2_grade.append('D')
            if 6 <= n < 7:
                test2_grade.append('C')
            if 7 <= n < 8:
                test2_grade.append('B')
            if 8 <= n < 9:
                test2_grade.append('A')
            if 9 <= n <= 10:
                test2_grade.append('S')
        return test1_grade, test2_grade
    else:
        test2 = np.array(test2)
        test3 = np.array(test3)
        for i, n in enumerate(test1):
            if n < 4:
                test1_grade.append('F')
            if 4 <= n < 5:
                test1_grade.append('E')
            if 5 <= n < 6:
                test1_grade.append('D')
            if 6 <= n < 7:
                test1_grade.append('C')
            if 7 <= n < 8:
                test1_grade.append('B')
            if 8 <= n < 9:
                test1_grade.append('A')
            if 9 <= n <= 10:
                test1_grade.append('S')

        for i, n in enumerate(test2):
            if n < 4:
                test2_grade.append('F')
            if 4 <= n < 5:
                test2_grade.append('E')
            if 5 <= n < 6:
                test2_grade.append('D')
            if 6 <= n < 7:
                test2_grade.append('C')
            if 7 <= n < 8:
                test2_grade.append('B')
            if 8 <= n < 9:
                test2_grade.append('A')
            if 9 <= n < 11:
                test2_grade.append('S')
        for i, n in enumerate(test3):
            if n < 4:
                test3_grade.append('F')
            if 4 <= n < 5:
                test3_grade.append('E')
            if 5 <= n < 6:
                test3_grade.append('D')
            if 6 <= n < 7:
                test3_grade.append('C')
            if 7 <= n < 8:
                test3_grade.append('B')
            if 8 <= n < 9:
                test3_grade.append('A')
            if 9 <= n <= 10:
                test3_grade.append('S')
        return test1_grade, test2_grade, test3_grade


def find_grade_fromMark_predicted(predicted):
    predicted = np.array(predicted)
    retpred = []
    for i, n in enumerate(predicted):
        if n == 0:
            retpred.append('F')
        elif n == 1:
            retpred.append('E')
        elif n == 2:
            retpred.append('D')
        elif n == 3:
            retpred.append('C')
        elif n == 4:
            retpred.append('B')
        elif n == 5:
            retpred.append('A')
        elif n == 6:
            retpred.append('S')
    return retpred


def find_frequency_grades(test1, test2=None, test3=None):
    t1_fg_a = 0
    t1_fg_b = 0
    t1_fg_c = 0
    t1_fg_d = 0
    t1_fg_e = 0
    t1_fg_f = 0
    t1_fg_s = 0

    t2_fg_a = 0
    t2_fg_b = 0
    t2_fg_c = 0
    t2_fg_d = 0
    t2_fg_f = 0
    t2_fg_e = 0
    t2_fg_s = 0

    t3_fg_a = 0
    t3_fg_b = 0
    t3_fg_c = 0
    t3_fg_d = 0
    t3_fg_e = 0
    t3_fg_f = 0
    t3_fg_s = 0
    if test2 is None:

        for i in test1:
            if i == 'E':
                t1_fg_e = t1_fg_e + 1
            elif i == 'F':
                t1_fg_f = t1_fg_f + 1
            elif i == 'A':
                t1_fg_a = t1_fg_a + 1
            elif i == 'B':
                t1_fg_b = t1_fg_b + 1
            elif i == 'C':
                t1_fg_c = t1_fg_c + 1
            elif i == 'D':
                t1_fg_d = t1_fg_d + 1
            elif i == 'S':
                t1_fg_s = t1_fg_s + 1
        return t1_fg_a, t1_fg_b, t1_fg_c, t1_fg_d, t1_fg_e, t1_fg_f, t1_fg_s

    elif test3 is None:
        for i in test1:
            if i == 'E':
                t1_fg_e = t1_fg_e + 1
            elif i == 'F':
                t1_fg_f = t1_fg_f + 1
            elif i == 'A':
                t1_fg_a = t1_fg_a + 1
            elif i == 'B':
                t1_fg_b = t1_fg_b + 1
            elif i == 'C':
                t1_fg_c = t1_fg_c + 1
            elif i == 'D':
                t1_fg_d = t1_fg_d + 1
            elif i == 'S':
                t1_fg_s = t1_fg_s + 1

        for i in test2:
            if i == 'E':
                t2_fg_e = t2_fg_e + 1
            elif i == 'F':
                t2_fg_f = t2_fg_f + 1
            elif i == 'A':
                t2_fg_a = t2_fg_a + 1
            elif i == 'B':
                t2_fg_b = t2_fg_b + 1
            elif i == 'C':
                t2_fg_c = t2_fg_c + 1
            elif i == 'D':
                t2_fg_d = t2_fg_d + 1
            elif i == 'S':
                t2_fg_s = t2_fg_s + 1

        return t1_fg_a, t1_fg_b, t1_fg_c, t1_fg_d, t1_fg_e, t1_fg_f, t1_fg_s, \
               t2_fg_a, t2_fg_b, t2_fg_c, t2_fg_d, t2_fg_e, t2_fg_f, t2_fg_s
    else:
        for i in test1:
            if i == 'E':
                t1_fg_e = t1_fg_e + 1
            elif i == 'F':
                t1_fg_f = t1_fg_f + 1
            elif i == 'A':
                t1_fg_a = t1_fg_a + 1
            elif i == 'B':
                t1_fg_b = t1_fg_b + 1
            elif i == 'C':
                t1_fg_c = t1_fg_c + 1
            elif i == 'D':
                t1_fg_d = t1_fg_d + 1
            elif i == 'S':
                t1_fg_s = t1_fg_s + 1

        for i in test2:
            if i == 'E':
                t2_fg_e = t2_fg_e + 1
            elif i == 'F':
                t2_fg_f = t2_fg_f + 1
            elif i == 'A':
                t2_fg_a = t2_fg_a + 1
            elif i == 'B':
                t2_fg_b = t2_fg_b + 1
            elif i == 'C':
                t2_fg_c = t2_fg_c + 1
            elif i == 'D':
                t2_fg_d = t2_fg_d + 1
            elif i == 'S':
                t2_fg_s = t2_fg_s + 1
        for i in test3:
            if i == 'E':
                t3_fg_e = t3_fg_e + 1
            elif i == 'F':
                t3_fg_f = t3_fg_f + 1
            elif i == 'A':
                t3_fg_a = t3_fg_a + 1
            elif i == 'B':
                t3_fg_b = t3_fg_b + 1
            elif i == 'C':
                t3_fg_c = t3_fg_c + 1
            elif i == 'D':
                t3_fg_d = t3_fg_d + 1
            elif i == 'S':
                t3_fg_s = t3_fg_s + 1
        return t1_fg_a, t1_fg_b, t1_fg_c, t1_fg_d, t1_fg_e, t1_fg_f, t1_fg_s, \
               t2_fg_a, t2_fg_b, t2_fg_c, t2_fg_d, t2_fg_e, t2_fg_f, t2_fg_s, \
               t3_fg_a, t3_fg_b, t3_fg_c, t3_fg_d, t3_fg_e, t3_fg_f, t3_fg_s
















        # def create_teacher(num):
        #     for i in range(3, num):
        #         us = User.objects.create_user(username='teacher' + str(i),
        #                                       email='teacher' + str(i) + '@gmail.com',
        #                                       password='dnpandey')
        #         us.save()
        #         gr = Group.objects.get(name='Teachers')
        #         gr.user_set.add(us)
        #
        #         teach = Teacher(teacheruser=us, experience=5, name=us.username)
        #         teach.save()
        #
        #
        # def create_student(num):
        #     for i in range(4, num):
        #         us = User.objects.create_user(username='student' + str(i),
        #                                       email='studentss' + str(i) + '@gmail.com',
        #                                       password='dnpandey')
        #         us.save()
        #         gr = Group.objects.get(name='Students')
        #         gr.user_set.add(us)
        #         cl = klass.objects.all()
        #         classes = []
        #         for k in cl:
        #             classes.append(k)
        #         stu = Student(studentuser=us, klass=classes[0], rollNumber=int(str(i) + '00'), name='stu' + str(i),
        #                       dob=timezone.now(), pincode=int(str(405060)))
        #         stu.save()
        #         sub = Subject(name='Science', student=stu)
        #         sub.save()


# class way

class Studs:
    def __init__(self, user):
        self.profile = user.student
        self.institution = self.profile.school.category
    def get_dob(self):
        return self.profile.dob


    def get_section(self):
        return self.profile.klass.name[-1]


    def my_subjects_objects(self):
        subs = self.profile.subject_set.all()
        subjects = []
        for sub in subs:
            subjects.append(sub)
        return subjects

    def my_subjects_names(self):
        subs = self.profile.subject_set.all()
        subjects = []
        for sub in subs:
            subjects.append(sub.name)
        subjects = list(unique_everseen(subjects))
        return subjects


    def readmarks(self,subject):
        subjects = self.profile.subject_set.get(name = subject)
        test1 =test2 = test3 = testhy = test4 = testpredhy = -1
        test1 = subjects.test1
        test2 = subjects.test2
        test3 = subjects.test3
        testhy = subjects.hy
        test4 = subjects.test4
        testpredhhy = subjects.predicted_hy

        return test1,test2,test3,testhy,test4,testpredhy        


    def hindi_3testhyprediction(self,test1, test2, test3, DOB, section):
        '''
        convert test marks into numpy arrays
        '''
        t1 = int(test1)
        t2 = int(test2)
        t3 = int(test3)

        if section == 'a':
            section = 1
        elif section == 'b':
            section = 2

        '''
        calculate age using DOB (dd/mm/year)
        '''
        days_in_year = 365.2425
        age = int((date(2018, 4, 1) - DOB).days / days_in_year)
        # age = int((date.today() - DOB).days / days_in_year)

        overall = np.array([[t1, t2, t3, age, section]])

        '''
            transform(scale) data to original data of school
        '''
        overall = sca_hindi.transform(overall)
        '''
            predict the hy marks using the trained ml algorithm
        '''
        prediction = svmhindihhy.predict(overall)
        return prediction


    def maths_3testhyprediction(self,test1, test2, test3, DOB, section):
        '''
        convert test marks into numpy arrays
        '''
        t1 = int(test1)
        t2 = int(test2)
        t3 = int(test3)

        if section == 'a':
            section = 1
        elif section == 'b':
            section = 2

        '''
            calculate age using DOB (dd/mm/year)
        '''
        days_in_year = 365.2425
        age = int((date(2018, 4, 1) - DOB).days / days_in_year)

        overall = np.array([[t1, t2, t3, age, section]])

        '''
            transform(scale) data to original data of school
        '''
        overall = sca_maths.transform(overall)
        '''
            predict the hy marks using the trained ml algorithm
        '''
        prediction = knn7mathshhy.predict(overall)
        return prediction


    def english_3testhyprediction(self,test1, test2, test3, DOB, section):
        '''
        convert test marks into numpy arrays
        '''
        t1 = int(test1)
        t2 = int(test2)
        t3 = int(test3)

        if section == 'a':
            section = 1
        elif section == 'b':
            section = 2

        '''
            calculate age using DOB (dd/mm/year)
        '''
        days_in_year = 365.2425
        age = int((date(2018, 4, 1) - DOB).days / days_in_year)

        overall = np.array([[t1, t2, t3, age, section]])

        '''
            transform(scale) data to original data of school
        '''
        overall = sca_english.transform(overall)
        '''
            predict the hy marks using the trained ml algorithm
        '''
        prediction = knn7englishhhy.predict(overall)
        return prediction


    def science_3testhyprediction(self,test1, test2, test3, DOB, section):
        #convert test marks into numpy arrays
        t1 = int(test1)
        t2 = int(test2)
        t3 = int(test3)

        if section == 'a':
            section = 1
        elif section == 'b':
            section = 2

            '''
                calculate age using DOB (dd/mm/year)
            '''
        days_in_year = 365.2425

        age = int((date(2018, 4, 1) - DOB).days / days_in_year)

        overall = np.array([[t1, t2, t3, age, section]])

        '''
            transform(scale) data to original data of school
        '''
        overall = sca_science.transform(overall)
        '''
            predict the hy marks using the trained ml algorithm
        '''
        prediction = knn7sciencehhy.predict(overall)
        return prediction


    def predictionConvertion(self, prediction):
        try:
            prediction = prediction[0]
        except:
            pass

        if prediction == 0:
            conversion = 35
        elif prediction == 1:
            conversion = 45
        elif prediction == 2:
            conversion = 55
        elif prediction == 3:
            conversion = 65
        elif prediction == 4:
            conversion = 75
        elif prediction == 5:
            conversion = 85
        elif prediction == 6:
            conversion = 95
        else:
            conversion = '404'
        return conversion

    def allOnlinetests(self):
        if self.profile.school.category == 'School':
            my_tests = KlassTest.objects.filter(testTakers=self.profile)
        elif self.profile.school.category == 'SSC':
            #  adding all tests papers created by BodhiAI 
            #for all the students who register 
            if self.profile.school.name== 'BodhiAI':
                all_tests = SSCKlassTest.objects.filter(creator__username =
                                                        'BodhiAI')
                already_taken_marks =\
                SSCOnlineMarks.objects.filter(student=self.profile)
                already_taken_tests = []
                takeable_tests = []
                for i in already_taken_marks:
                    already_taken_tests.append(i.test)
                new_tests = []
                for at in all_tests:
                    if at in already_taken_tests:
                        pass
                    else:
                        new_tests.append(at)
                for i in new_tests:
                    if i.sub != None or i.sub != '':
                        takeable_tests.append(i)
                    else:
                        pass
                    
                for t in takeable_tests:
                    t.testTakers.add(self.profile)
                    return takeable_tests
            else:
                all_tests = SSCKlassTest.objects.filter(testTakers =
                                                        self.profile)
                return all_tests
    def already_takenTests_Subjects(self):
        taken_tests = SSCOnlineMarks.objects.filter(test__testTakers =
                                                    self.profile)
        subs = []
        for i in taken_tests:
            if i.test.sub != '':
                subs.append(i.test.sub)
        return list(unique_everseen(subs))
    def subjects_NotTakenTests(self):
        tests = SSCKlassTest.objects.filter(testTakers=self.profile)
        sub_list = []
        for i in tests:
            if i.sub != None or i.sub != '':
                sub_list.append(i.sub)
        return list(unique_everseen(sub_list))
    def subjects_OnlineTest(self):
        my_tests = self.allOnlinetests()
        subs = []
        if my_tests:
            for i in my_tests:
                subs.append(i.sub)
            subs = list(unique_everseen(subs))
            return subs
        else:
            return None

    def OnlineTestsSubwise(self, subject):
        if self.profile.school.category == 'School':
            my_tests = KlassTest.objects.filter(testTakers=self.profile, sub=
        subject)
        elif self.profile.school.category == 'SSC':
            my_tests = SSCKlassTest.objects.filter(testTakers =
                                                   self.profile,sub = subject)
        return my_tests

# Finds if student has already taken the test
    def is_onlineTestTaken(self, test_id):
        try:
            if self.institution == 'School':
                test = OnlineMarks.objects.get(test__id=test_id, student=
            self.profile)
                return test
            elif self.institution == 'SSC':
                test = SSCOnlineMarks.objects.get(test__id = test_id ,student =
                                                  self.profile)
                return test
        except Exception as e:
            print(str(e))
            return None

# Tests that are not taken 
    def toTake_Tests(self):
        if self.institution == 'School':
           pass
        elif self.institution == 'SSC':
            all_tests = SSCKlassTest.objects.filter(testTakers = self.profile)
            takeable_tests = []
            for i in all_tests:
                if i.sub != None or i.sub == '':
                    takeable_tests.append(i)
            new_tests = {}
            for n,i in enumerate(takeable_tests):
                topics = []
                already_taken = SSCOnlineMarks.objects.filter(student =\
                                                           self.profile,test__id =i.id)
                if len(already_taken)>0:
                    continue
                else:
                    count_quest = 0
                    for j in i.sscquestions_set.all():
                        count_quest += 1
                        cat =\
                        self.changeIndividualNames(j.topic_category,j.section_category)
                        topics.append(cat)
                    topics = list(unique_everseen(topics))
                    new_tests[i.id] =\
                    {'subject':i.sub,'topics':topics,'num_questions':count_quest}
            return new_tests

            
            

       
# Finds average of a test
    def online_findAverageofTest(self, test_id, percent=None):
        if percent:
            if self.institution == 'School':
                test = OnlineMarks.objects.filter(test__id=test_id)
            elif self.institution == 'SSC':
                test = SSCOnlineMarks.objects.filter(test__id=test_id)
            all_marks = []
            all_marks_percent = []
            for te in test:
                all_marks.append(int(te.marks))
                all_marks_percent.append((te.marks / te.test.max_marks) * 100)
            average = np.mean(all_marks)
            percent_average = np.mean(all_marks_percent)
            return average, percent_average


        else:
            if self.institution == 'School':
                test = OnlineMarks.objects.filter(test__id=test_id)
            elif self.institution == 'SSC':
                test = SSCOnlineMarks.objects.filter(test__id=test_id)
            all_marks = []
            for te in test:
                all_marks.append(int(te.marks))
            average = np.mean(all_marks)

            return average

# Finds student's percentile in a particular test
    def online_findPercentile(self, test_id):
        if self.institution == 'School':
            test = OnlineMarks.objects.filter(test__id=test_id)
            my_score = OnlineMarks.objects.get(test__id=test_id, student=self.profile)
        elif self.institution == 'SSC':
            test = SSCOnlineMarks.objects.filter(test__id=test_id)
            my_score = SSCOnlineMarks.objects.get(test__id=test_id, student=self.profile)
        all_marks = []
        for te in test:
            all_marks.append(te.marks)
        num_students = len(all_marks)
        my_score = my_score.marks
        same_marks = -1
        less_marks = 0
        for i in all_marks:
            if i == my_score:
                same_marks += 1
            elif i < my_score:
                less_marks += 1
        if same_marks == -1:
            percentile = ((less_marks-same_marks) / num_students)
        else:
            percentile = ((less_marks + (0.5 * same_marks)) / num_students)
        return percentile, all_marks

    def online_QuestionPercentage(self, test_id):
        if self.institution == 'School':
            online_marks = OnlineMarks.objects.filter(test__id=test_id)
        elif self.institution == 'SSC':
            online_marks = SSCOnlineMarks.objects.filter(test__id=test_id)
        all_answers = []
        for aa in online_marks:
            all_answers.extend(aa.allAnswers)
        unique, counts = np.unique(all_answers, return_counts=True)
        freq = np.asarray((unique, counts)).T
        return freq


    def offline_QuestionPercentage(self, test_id):
        if self.institution == 'School':
            offline_marks = OnlineMarks.objects.filter(test__id=test_id)
        elif self.institution == 'SSC':
            offline_marks = SSCOfflineMarks.objects.filter(test__id=test_id)
        all_answers = []
        for aa in offline_marks:
            all_answers.extend(aa.allAnswers)
        unique, counts = np.unique(all_answers, return_counts=True)
        freq = np.asarray((unique, counts)).T
        return freq

    def offline_findPercentile(self,test_id):
        if self.institution == 'School':
            test = OnlineMarks.objects.filter(test__id=test_id)
            my_score = OnlineMarks.objects.get(test__id=test_id, student=self.profile)
        elif self.institution == 'SSC':
            test = SSCOfflineMarks.objects.filter(test__id=test_id)
            my_score = SSCOfflineMarks.objects.get(test__id=test_id, student=self.profile)
        all_marks = []
        for te in test:
            all_marks.append(te.marks)
        num_students = len(all_marks)
        my_score = my_score.marks
        same_marks = -1
        less_marks = 0
        for i in all_marks:
            if i == my_score:
                same_marks += 1
            elif i < my_score:
                less_marks += 1
        if same_marks == -1:
            percentile = ((less_marks-same_marks) / num_students)
        else:
            percentile = ((less_marks + (0.5 * same_marks)) / num_students)
        return percentile, all_marks
    

    def offline_findAverageofTest(self, test_id, percent=None):
        if percent:
            if self.institution == 'School':
                test = OnlineMarks.objects.filter(test__id=test_id)
            elif self.institution == 'SSC':
                test = SSCOfflineMarks.objects.filter(test__id=test_id)
            all_marks = []
            all_marks_percent = []
            for te in test:
                all_marks.append(int(te.marks))
                all_marks_percent.append((te.marks / te.test.max_marks) * 100)
            average = np.mean(all_marks)
            percent_average = np.mean(all_marks_percent)
            return average, percent_average


        else:
            if self.institution == 'School':
                test = OnlineMarks.objects.filter(test__id=test_id)
            elif self.institution == 'SSC':
                test = SSCOfflineMarks.objects.filter(test__id=test_id)
            all_marks = []
            for te in test:
                all_marks.append(int(te.marks))
            average = np.mean(all_marks)

            return average

# Finds number of right, wrong and skipped answers, also finds accuracy in a
# test    
    def test_statistics(self,testid):
        if self.institution == 'Schoool':
            pass
        elif self.institution == 'SSC':
            # get instance of onlinemarks with testid
            marks = SSCOnlineMarks.objects.get(student = self.profile,test__id
                                               = testid)
            if marks:
                right_answers = 0
                wrong_answers = 0
                skipped_answers = 0
            # counts number of right,wrong and skipped answers
                for ra in marks.rightAnswers:
                    right_answers += 1
                for wa in marks.wrongAnswers:
                    wrong_answers += 1
                for sp in marks.skippedAnswers:
                    skipped_answers += 1
            # finds accuracy on the basis of counting done above
                try: 
                    accuracy = ((right_answers)/(right_answers+wrong_answers))*100
                except Exception as e:
                    accuracy = 0
                return right_answers,wrong_answers,skipped_answers,accuracy
    def offline_test_statistics(self,test_id):
        if self.institution == 'Schoool':
            pass
        elif self.institution == 'SSC':
            # get instance of onlinemarks with testid
            marks = SSCOfflineMarks.objects.get(student = self.profile,test__id
                                               = test_id)
            if marks:
                right_answers = 0
                wrong_answers = 0
                skipped_answers = 0
            # counts number of right,wrong and skipped answers
                for ra in marks.rightAnswers:
                    right_answers += 1
                for wa in marks.wrongAnswers:
                    wrong_answers += 1
                for sp in marks.skippedAnswers:
                    skipped_answers += 1
            # finds accuracy on the basis of counting done above
                try: 
                    accuracy = ((right_answers)/(right_answers+wrong_answers))*100
                except Exception as e:
                    accuracy = 0
                return right_answers,wrong_answers,skipped_answers,accuracy


# Finds the subjectwise accuracy (eg. SSCMultipleSections) of a test
    def test_SubjectAccuracy(self,testid):
        if self.institution == 'School':
            pass
        elif self.institution == 'SSC':
            # get onlinemarks object of a particular test
            marks = SSCOnlineMarks.objects.get(student = self.profile,test__id
                                               = testid)
            right_answers = []
            wrong_answers = []
            skipped_answers = []
            subjectra = []
            subjectwa = []
            subjectsa = []
            # find all the right answers with their subjects
            for ra in marks.rightAnswers:
                question = SSCquestions.objects.get(choices__id = ra)
                sub = question.section_category
                right_answers.append(question.id)
                subjectra.append(sub)
            # find all the wrong answers with their subjects
            for wa in marks.wrongAnswers:
                question = SSCquestions.objects.get(choices__id = wa)
                sub = question.section_category
                wrong_answers.append(question.id)
                subjectwa.append(sub)
            # find all the skipped answers with their subjects
            for sa in marks.skippedAnswers:
                question = SSCquestions.objects.get(id = sa)
                sub = question.section_category
                skipped_answers.append(question.id)
                subjectsa.append(sub)
            # zip answers with their subjects
            ra = list(zip(subjectra,right_answers))
            wa = list(zip(subjectwa,wrong_answers))
            sp= list(zip(subjectsa,skipped_answers))
            # find unique questions ids and thier counts
            unique, counts = np.unique(ra, return_counts=True)
            raf = np.asarray((unique, counts)).T
            unique, counts = np.unique(wa, return_counts=True)
            waf = np.asarray((unique, counts)).T
            unique, counts = np.unique(sp, return_counts=True)
            spf = np.asarray((unique, counts)).T
            new_ra = {}
            # if subject is in student's subject then add subject count to a
            # dictionary
            for i,j in raf:
                if  i in self.my_subjects_names():
                    new_ra[i] = j
            new_wa = {}
            for i,j in waf:
                if  i in self.my_subjects_names():
                    new_wa[i] = j
            new_sa = {}
            for i,j in spf:
                if  i in self.my_subjects_names():
                    new_sa[i] = j
            # if length of right or wrong answer dictionaries are not same then
            # add the missing subject to the shorter dictionary (works when
            # accuracy of one of the subjects is 100%)
            if len(new_ra) > len(new_wa):
                for i in new_ra.keys():
                    if not i in new_wa.keys():
                        new_wa[i] = 0
            elif len(new_ra) < len(new_wa):
                for i in new_wa.keys():
                    if not i in new_ra.keys():
                        new_ra[i] = 0
            # find subject accuracy by comparing number of right and wrong  answers per
            # subject
            sub_accuracy = {}
            for rk,rv in new_ra.items():
                for wk,wv in new_wa.items():
                    if rk == wk:
                        accuracy =\
                        ((int(new_ra[wk]))/((int(new_ra[wk])+int(new_wa[wk])))*100)
                        sub_accuracy[wk] = accuracy
            return sub_accuracy
    def offline_test_SubjectAccuracy(self,testid):
        if self.institution == 'School':
            pass
        elif self.institution == 'SSC':
            # get onlinemarks object of a particular test
            marks = SSCOfflineMarks.objects.get(student = self.profile,test__id
                                               = testid)
            right_answers = []
            wrong_answers = []
            skipped_answers = []
            subjectra = []
            subjectwa = []
            subjectsa = []
            # find all the right answers with their subjects
            for ra in marks.rightAnswers:
                question = SSCquestions.objects.get(choices__id = ra)
                sub = question.section_category
                right_answers.append(question.id)
                subjectra.append(sub)
            # find all the wrong answers with their subjects
            for wa in marks.wrongAnswers:
                question = SSCquestions.objects.get(choices__id = wa)
                sub = question.section_category
                wrong_answers.append(question.id)
                subjectwa.append(sub)
            # find all the skipped answers with their subjects
            for sa in marks.skippedAnswers:
                question = SSCquestions.objects.get(id = sa)
                sub = question.section_category
                skipped_answers.append(question.id)
                subjectsa.append(sub)
            # zip answers with their subjects
            ra = list(zip(subjectra,right_answers))
            wa = list(zip(subjectwa,wrong_answers))
            sp= list(zip(subjectsa,skipped_answers))
            # find unique questions ids and thier counts
            unique, counts = np.unique(ra, return_counts=True)
            raf = np.asarray((unique, counts)).T
            unique, counts = np.unique(wa, return_counts=True)
            waf = np.asarray((unique, counts)).T
            unique, counts = np.unique(sp, return_counts=True)
            spf = np.asarray((unique, counts)).T
            new_ra = {}
            # if subject is in student's subject then add subject count to a
            # dictionary
            for i,j in raf:
                if  i in self.my_subjects_names():
                    new_ra[i] = j
            new_wa = {}
            for i,j in waf:
                if  i in self.my_subjects_names():
                    new_wa[i] = j
            new_sa = {}
            for i,j in spf:
                if  i in self.my_subjects_names():
                    new_sa[i] = j
            # if length of right or wrong answer dictionaries are not same then
            # add the missing subject to the shorter dictionary (works when
            # accuracy of one of the subjects is 100%)
            if len(new_ra) > len(new_wa):
                for i in new_ra.keys():
                    if not i in new_wa.keys():
                        new_wa[i] = 0
            elif len(new_ra) < len(new_wa):
                for i in new_wa.keys():
                    if not i in new_ra.keys():
                        new_ra[i] = 0
            # find subject accuracy by comparing number of right and wrong  answers per
            # subject
            sub_accuracy = {}
            for rk,rv in new_ra.items():
                for wk,wv in new_wa.items():
                    if rk == wk:
                        accuracy =\
                        ((int(new_ra[wk]))/((int(new_ra[wk])+int(new_wa[wk])))*100)
                        sub_accuracy[wk] = accuracy
            return sub_accuracy

# Finds the overall weak topics of a student,else if singleTest is true then
# finds weak topics of single  test 
    def weakAreas(self,subject,singleTest = None):
        if self.institution == 'School':
            my_marks = OnlineMarks.objects.filter(student = self.profile,test__sub
                                             = subject)
        elif self.institution == 'SSC':
            if singleTest == None:
                my_marks = SSCOnlineMarks.objects.filter(student = self.profile,test__sub
                                                 = subject)
                all_marks = SSCOnlineMarks.objects.filter(student= self.profile,
                                                    test__sub =
                                                    'SSCMultipleSections')
                offline_my_marks =\
                SSCOfflineMarks.objects.filter(student=self.profile,test__sub=subject)
                offline_all_marks = SSCOfflineMarks.objects.filter(student =
                                                                   self.profile,test__sub
                                                                   =
                                                                   'SSCMultipleSections')


                indi_my_marks = None
            else:
                indi_my_marks = SSCOnlineMarks.objects.get(student=
                                                         self.profile,test__id =
                                                         singleTest)
                my_marks = None
                all_marks = None
                offline_my_marks = None
                offline_all_marks = None

        wrong_Answers = []
        skipped_Answers = []
        # if onetest object is present then adds all the wrong and skipped
        # answers to separate lists
        if indi_my_marks:
            for wa in indi_my_marks.wrongAnswers:
                wrong_Answers.append(wa)
            for sp in indi_my_marks.skippedAnswers:
                skipped_Answers.append(sp)
        # same as above, but when single subject tests are present
        if my_marks:
            for om in my_marks:
                for wa in om.wrongAnswers:
                    wrong_Answers.append(wa)
                for sp in om.skippedAnswers:
                    skipped_Answers.append(sp)

        # same as above, but when multiple subject tests are present
        if all_marks:
            for om in all_marks:
                for wa in om.wrongAnswers:
                    wrong_Answers.append(wa)
                for sp in om.skippedAnswers:
                    skipped_Answers.append(sp)
        # same as above, but when for offline my marks
        if offline_my_marks:
            for om in offline_my_marks:
                for wa in om.wrongAnswers:
                    wrong_Answers.append(wa)
                for sp in om.skippedAnswers:
                    skipped_Answers.append(sp)
        # same as above, but when for offline marks for multiple subjects
        if offline_all_marks:
            for om in offline_all_marks:
                for wa in om.wrongAnswers:
                    wrong_Answers.append(wa)
                for sp in om.skippedAnswers:
                    skipped_Answers.append(sp)

        wq=[]
        for i in wrong_Answers:
            if self.institution == 'School':
                qu = Questions.objects.get(choices__id = i)
            elif self.institution == 'SSC':
            # finds the questions objects of wrong questions
                try:
                    qu = SSCquestions.objects.get(choices__id = i)
                except Exception as e:
                    print(str(e))
                    continue
                if subject == 'SSCMultipleSections':
                    quid = qu.id
                    wq.append(quid)
                else:
                    if qu.section_category == subject:
                        quid = qu.id
                        wq.append(quid)
        for i in skipped_Answers:
            if self.institution == 'School':
                try:
                    qu = Questions.objects.get(id = i)
                except Exception as e:
                    print(str(e))
                    continue
            elif self.institution == 'SSC':
            # finds the questions objects of skipped questions
                try:
                    qu = SSCquestions.objects.get(id = i)
                except Exception as e:
                    print(str(e))
                    continue
                if subject == 'SSCMultipleSections':
                    quid = qu.id
                    wq.append(quid)
                else:
                    if qu.section_category == subject:
                        quid = qu.id
                        wq.append(quid)
        # finds unique questions with thier frequency
        unique, counts = np.unique(wq, return_counts=True)
        waf = np.asarray((unique, counts)).T
        nw_ind = []
        # sorts the list 
        kk = np.sort(waf,0)[::-1]
        for u in kk[:,1]:
            for z,w in waf:
                if u == w:
                    if z in nw_ind:
                        continue
                    else:
                        nw_ind.append(z)
                        break
        final_freq = np.asarray((nw_ind,kk[:,1])).T
        return final_freq


        
# Finds the weak topic intensity, i.e. returns a list with topic name and
# number of wrong questions
    def weakAreas_Intensity(self,subject,singleTest = None):
        if singleTest == None:
            arr = self.weakAreas(subject)
        else:
            arr = self.weakAreas(subject,singleTest = singleTest)
            catSubject = []
            catCategory = []
        anal = []
        num = []
        for u,k in arr: 
            if self.institution == 'School':
                qu = Questions.objects.get(id = u)
            elif self.institution == 'SSC':
                qu = SSCquestions.objects.get(id = u)
            if subject == 'SSCMultipleSections':
                quest_cat = qu.topic_category
                quest_sub = qu.section_category
                name_cat = self.changeIndividualNames(quest_cat,quest_sub)
                anal.append(name_cat)
                num.append(k)
            else:
                category = qu.topic_category
                anal.append(category)
                num.append(k)
        analysis = list(zip(anal,num))
        final_analysis = []
        final_num = []
        for u,k in analysis:
            if u in final_analysis:
                ind = final_analysis.index(u)
                temp = final_num[ind]
                final_num[ind] = temp + k
            else:
                final_analysis.append(u)
                final_num.append(k)

        waf = list(zip(final_analysis,final_num))
        return waf


    def weakAreas_IntensityAverage(self,subject):
        arr = self.weakAreas_Intensity(subject)
        if self.institution  == 'School':
            pass
        elif self.institution == 'SSC':
            marks = SSCOnlineMarks.objects.filter(student =
                                                  self.profile,test__sub =
                                                  subject)
            all_marks = SSCOnlineMarks.objects.filter(student=
                                                      self.profile,test__sub='SSCMultipleSections')
            offline_marks =\
            SSCOfflineMarks.objects.filter(student=self.profile,test__sub =
                                           subject)
            offline_all_marks = SSCOfflineMarks.objects.filter(student =
                                                               self.profile,
                                                               test__sub =
                                                               'SSCMultipleSections')
            all_ids = []
            for mark in marks:
                for total in mark.allAnswers:
                    try:
                        quest = SSCquestions.objects.get(choices__id = total)
                    except Exception as e:
                        print(str(e))
                        continue
                    all_ids.append(quest.topic_category) 
                for sk in mark.skippedAnswers:
                    try:
                        quest = SSCquestions.objects.get(id = sk)
                    except Exception as e:
                        print(str(e))
                        continue
                    all_ids.append(quest.topic_category)
            # finds question ids from mixed category tests
            if all_marks:
                for mark in all_marks:
                    for total in mark.allAnswers:
                        try:
                            quest = SSCquestions.objects.get(choices__id = total)
                        except Exception as e:
                            print(str(e))
                            continue
                        if quest.section_category == subject:
                            all_ids.append(quest.topic_category) 
                    for sk in mark.skippedAnswers:
                        try:
                            quest = SSCquestions.objects.get(id = sk)
                        except Exception as e:
                            print(str(e))
                            continue
                        if quest.section_category == subject:
                            all_ids.append(quest.topic_category)
            if offline_marks:
                for mark in offline_marks:
                    for total in mark.allAnswers:
                        try:
                            quest = SSCquestions.objects.get(choices__id = total)
                        except Exception as e:
                            print(str(e))
                            continue
                        all_ids.append(quest.topic_category) 
                    for sk in mark.skippedAnswers:
                        try:
                            quest = SSCquestions.objects.get(id = sk)
                        except Exception as e:
                            print(str(e))
                            continue
                        all_ids.append(quest.topic_category)
            if offline_all_marks:
                for mark in offline_all_marks:
                    for total in mark.allAnswers:
                        try:
                            quest = SSCquestions.objects.get(choices__id = total)
                        except Exception as e:
                            print(str(e))
                            continue
                        if quest.section_category == subject:
                            all_ids.append(quest.topic_category) 
                    for sk in mark.skippedAnswers:
                        try:
                            quest = SSCquestions.objects.get(id = sk)
                        except Exception as e:
                            print(str(e))
                            continue
                        if quest.section_category == subject:
                            all_ids.append(quest.topic_category)





            unique, counts = np.unique(all_ids, return_counts=True)
            cat_quests = np.asarray((unique, counts)).T
            arr = np.array(arr)
            average_cat = []
            average_percent = []

            if len(arr)>0:
                for i,j in cat_quests:
                    if i in arr[:,0]:
                        ind = np.where(arr==i)
                        now_arr = arr[ind[0],1]
                        average =(int(now_arr[0])/int(j)*100)
                        average_cat.append(i)
                        average_percent.append(average)
                weak_average = list(zip(average_cat,average_percent))
                return weak_average
            else:
                return 0
    def weakAreas_timing(self,subject):
        arr = self.weakAreas(subject)
        anal = []
        num = []
        for u,k in arr:
            if self.institution == 'School':
                qu = Questions.objects.get(id = u)
            elif self.institution == 'SSC':
                qu = SSCquestions.objects.get(id = u)
            
            category = qu.topic_category
            anal.append(category)
            num.append(k)
        analysis = list(zip(anal,num))
        quest = []
        time_list = []
        if self.institution == 'SSC':
            myMarks = SSCOnlineMarks.objects.filter(student =
                                                    self.profile,test__sub = subject)
            allMyMarks =\
                SSCOnlineMarks.objects.filter(student=self.profile,test__sub=
                                              'SSCMultipleSections')
            if myMarks:
                for t in myMarks:
                    for time in t.sscansweredquestion_set.all():
                        if time.quest.id in arr[:,0]:
                            quest.append(int(time.quest.id))
                            time_list.append(int(time.time))
            if allMyMarks:
                for t in myMarks:
                    for time in t.sscansweredquestion_set.all():
                        if time.quest.id in arr[:,0] and time.quest.section_category == subject:
                            quest.append(int(time.quest.id))
                            time_list.append(int(time.time))

        timer = list(zip(quest,time_list))

    def areawise_timing(self,subject,singleTest = None):
        all_questions = []
        all_timing = []
        if singleTest == None:
            if self.institution == 'School':
                marks = OnlineMarks.objects.filter(test__sub = subject,student =
                                                self.profile)
                for om in marks:
                    for aq in om.sscansweredquestion_set.all():
                        all_questions.append(aq.quest.topic_category)
                        all_timing.append(aq.time)

            elif self.institution == 'SSC':
                marks = SSCOnlineMarks.objects.filter(test__sub = subject, student =
                                                      self.profile)
                if marks:
                    for om in marks:
                        for aq in om.sscansweredquestion_set.all():
                            all_questions.append(aq.quest.topic_category)
                            all_timing.append(aq.time)


                all_marks =\
                SSCOnlineMarks.objects.filter(student=self.profile,test__sub=
                                              'SSCMultipleSections')
                if all_marks:
                    for om in all_marks:
                        for aq in om.sscansweredquestion_set.all():
                            if aq.quest.section_category == subject:
                                all_questions.append(aq.quest.topic_category)
                                all_timing.append(aq.time)
        else:
            if self.institution == 'SSC':
                indi_marks = SSCOnlineMarks.objects.get(student = self.profile,test__id =
                                                        singleTest)

                if indi_marks:
                    for aq in indi_marks.sscansweredquestion_set.all():
                        if subject == 'SSCMultipleSections':
                            category =\
                                self.changeIndividualNames(aq.quest.topic_category,aq.quest.section_category)
                            all_questions.append(category)
                            all_timing.append(aq.time)

                        else:
                            if aq.quest.section_category == subject:
                                all_questions.append(aq.quest.topic_category)
                                all_timing.append(aq.time)


        areawise_timing = list(zip(all_questions,all_timing))
        dim1 = list(unique_everseen(all_questions))
        dim3 = []
        dim4 = []
        freq = []
        for j in dim1:
            k_val = 0
            n = 0
            for x,y in areawise_timing:
                if j == x and y != -1:
                    k_val += y
                    n += 1
            dim3.append(j)
            try:
                average_time = float(k_val/n)
                dim4.append(average_time)
                freq.append(n)
            except:
                pass
        timing = list(zip(dim3,dim4))
        freq_list = list(zip(dim3,freq))
        return timing,freq_list

    def offline_weakAreas(self,subject,singleTest = None):
        if self.institution == 'School':
            my_marks = OnlineMarks.objects.filter(student = self.profile,test__sub
                                             = subject)
        elif self.institution == 'SSC':
            if singleTest == None:
                my_marks = SSCOfflineMarks.objects.filter(student = self.profile,test__sub
                                                 = subject)
                all_marks = SSCOfflineMarks.objects.filter(student= self.profile,
                                                    test__sub =
                                                    'SSCMultipleSections')
                indi_my_marks = None
            else:
                indi_my_marks = SSCOfflineMarks.objects.get(student=
                                                         self.profile,test__id =
                                                         singleTest)
                my_marks = None
                all_marks = None

        wrong_Answers = []
        skipped_Answers = []
        # if onetest object is present then adds all the wrong and skipped
        # answers to separate lists
        if indi_my_marks:
            for wa in indi_my_marks.wrongAnswers:
                wrong_Answers.append(wa)
            for sp in indi_my_marks.skippedAnswers:
                skipped_Answers.append(sp)
        # same as above, but when single subject tests are present
        if my_marks:
            for om in my_marks:
                for wa in om.wrongAnswers:
                    wrong_Answers.append(wa)
                for sp in om.skippedAnswers:
                    skipped_Answers.append(sp)

        # same as above, but when multiple subject tests are present
        if all_marks:
            for om in all_marks:
                for wa in om.wrongAnswers:
                    wrong_Answers.append(wa)
                for sp in om.skippedAnswers:
                    skipped_Answers.append(sp)
        wq=[]
        for i in wrong_Answers:
            if self.institution == 'School':
                qu = Questions.objects.get(choices__id = i)
            elif self.institution == 'SSC':
            # finds the questions objects of wrong questions
                qu = SSCquestions.objects.get(choices__id = i)
                if subject == 'SSCMultipleSections':
                    quid = qu.id
                    wq.append(quid)
                else:
                    if qu.section_category == subject:
                        quid = qu.id
                        wq.append(quid)
        for i in skipped_Answers:
            if self.institution == 'School':
                qu = Questions.objects.get(id = i)
            elif self.institution == 'SSC':
            # finds the questions objects of skipped questions
                qu = SSCquestions.objects.get(id = i)
                if subject == 'SSCMultipleSections':
                    quid = qu.id
                    wq.append(quid)
                else:
                    if qu.section_category == subject:
                        quid = qu.id
                        wq.append(quid)
        # finds unique questions with thier frequency
        unique, counts = np.unique(wq, return_counts=True)
        waf = np.asarray((unique, counts)).T
        nw_ind = []
        # sorts the list 
        kk = np.sort(waf,0)[::-1]
        for u in kk[:,1]:
            for z,w in waf:
                if u == w:
                    if z in nw_ind:
                        continue
                    else:
                        nw_ind.append(z)
                        break
        final_freq = np.asarray((nw_ind,kk[:,1])).T
        return final_freq

    def offline_weakAreas_Intensity(self,subject,singleTest = None):
        if singleTest == None:
            arr = self.offline_weakAreas(subject)
        else:
            arr = self.offline_weakAreas(subject,singleTest = singleTest)
            catSubject = []
            catCategory = []
        anal = []
        num = []
        for u,k in arr: 
            if self.institution == 'School':
                qu = Questions.objects.get(id = u)
            elif self.institution == 'SSC':
                qu = SSCquestions.objects.get(id = u)
            if subject == 'SSCMultipleSections':
                quest_cat = qu.topic_category
                quest_sub = qu.section_category
                name_cat = self.changeIndividualNames(quest_cat,quest_sub)
                anal.append(name_cat)
                num.append(k)
            else:
                category = qu.topic_category
                anal.append(category)
                num.append(k)
        analysis = list(zip(anal,num))
        final_analysis = []
        final_num = []
        for u,k in analysis:
            if u in final_analysis:
                ind = final_analysis.index(u)
                temp = final_num[ind]
                final_num[ind] = temp + k
            else:
                final_analysis.append(u)
                final_num.append(k)

        waf = list(zip(final_analysis,final_num))
        return waf

    def offline_weakAreas_IntensityAverage(self,subject):
        arr = self.offline_weakAreas_Intensity(subject)
        if self.institution == 'School':
            pass
        elif self.institution == 'SSC':
            marks = SSCOfflineMarks.objects.filter(student =
                                                  self.profile,test__sub =
                                                  subject)
            all_marks = SSCOfflineMarks.objects.filter(student=
                                                      self.profile,test__sub='SSCMultipleSections')
            all_ids = []
            for mark in marks:
                for total in mark.allAnswers:
                    quest = SSCquestions.objects.get(choices__id = total)
                    all_ids.append(quest.topic_category) 
                for sk in mark.skippedAnswers:
                    quest = SSCquestions.objects.get(id = sk)
                    all_ids.append(quest.topic_category)
            # finds question ids from mixed category tests
            if all_marks:
                for mark in all_marks:
                    for total in mark.allAnswers:
                        quest = SSCquestions.objects.get(choices__id = total)
                        if quest.section_category == subject:
                            all_ids.append(quest.topic_category) 
                    for sk in mark.skippedAnswers:
                        quest = SSCquestions.objects.get(id = sk)
                        if quest.section_category == subject:
                            all_ids.append(quest.topic_category)

            unique, counts = np.unique(all_ids, return_counts=True)
            cat_quests = np.asarray((unique, counts)).T
            arr = np.array(arr)
            average_cat = []
            average_percent = []

            if len(arr)>0:
                for i,j in cat_quests:
                    if i in arr[:,0]:
                        ind = np.where(arr==i)
                        now_arr = arr[ind[0],1]
                        average =(int(now_arr[0])/int(j)*100)
                        average_cat.append(i)
                        average_percent.append(average)
                weak_average = list(zip(average_cat,average_percent))
                return weak_average
            else:
                return 0







    def changeTopicNumbersNames(self,arr,subject):
        namedarr = []
        timing = []
        if subject == 'English':
            for i,j in arr:
                if i == '1.1':
                    namedarr.append('Word Meanings')
                    timing.append(j)
                elif i == '1.2':
                    namedarr.append('Idiom/Phrase Meaning')
                    timing.append(j)
                elif i == '2.1':
                    namedarr.append('Antonyms')
                    timing.append(j)
                elif i == '3.1':
                    namedarr.append('Alternate Phrases/Underlined')
                    timing.append(j)
                elif i == '3.2':
                    namedarr.append('Alternate words/Fill in the blanks')
                    timing.append(j)
                elif i == '4.1':
                    namedarr.append('Re-Arrangement')
                    timing.append(j)
                elif i == '5.1':
                    namedarr.append('Spelling')
                    timing.append(j)
                elif i == '6.1':
                    namedarr.append('Substitution')
                    timing.append(j)
                elif i == '7.1':
                    namedarr.append('Random')
                    timing.append(j)
                elif i == '8.1':
                    namedarr.append('Spot the Error')
                    timing.append(j)
                elif i == '9.1':
                    namedarr.append('Passage')
                    timing.append(j)
            return list(zip(namedarr,timing))
        if subject == 'General-Intelligence':
            for i,j in arr:
                if i == '1.1':
                    namedarr.append('Paper Cutting and Folding')
                    timing.append(j)
                elif i == '1.2':
                    namedarr.append('Mirror and Water Image')
                    timing.append(j)
                elif i == '1.3':
                    namedarr.append('Embedded Figures')
                    timing.append(j)
                elif i == '1.4':
                    namedarr.append('Figure Completion')
                    timing.append(j)
                elif i == '1.5':
                    namedarr.append('Counting Embedded Figures')
                    timing.append(j)
                elif i == '1.6':
                    namedarr.append('Counting in figures')
                    timing.append(j)
                elif i == '2.1':
                    namedarr.append('Analogous pair')
                    timing.append(j)
                elif i == '2.2':
                    namedarr.append('Multiple Analogy')
                    timing.append(j)
                elif i == '2.3':
                    namedarr.append('Choosing the analogous pair')
                    timing.append(j)
                elif i == '2.4':
                    namedarr.append('Number analogy (series pattern)')
                    timing.append(j)
                elif i =='2.5':
                    namedarr.append('Number analogy (missing)')
                    timing.append(j)
                elif i == '2.6':
                    namedarr.append('Alphabet based analogy')
                    timing.append(j)
                elif i == '2.7':
                    namedarr.append('Mixed analogy')
                    timing.append(j)
                elif i == '3.1':
                    namedarr.append('Series Completion (Diagram)')
                    timing.append(j)
                elif i == '3.2':
                    namedarr.append('Analogy (Diagram)')
                    timing.append(j)
                elif i == '3.3':
                    namedarr.append('Classification (Diagram)')
                    timing.append(j)
                elif i == '3.4':
                    namedarr.append('Dice & Boxes')
                    timing.append(j)
                elif i == '2.8':
                    namedarr.append('Ruled based analogy')
                    timing.append(j)
                elif i == '2.9':
                    namedarr.append('Alphabet series (missing)')
                    timing.append(j)
                elif i == '4.1':
                    namedarr.append('Age')
                    timing.append(j)
                elif i == '5.1':
                    namedarr.append('Matrix')
                    timing.append(j)
                elif i == '6.1':
                    namedarr.append('Word Creation')
                    timing.append(j)
                elif i == '7.1':
                    namedarr.append('Odd one out')
                    timing.append(j)
                elif i == '8.1':
                    namedarr.append('Height')
                    timing.append(j)
                elif i == '9.1':
                    namedarr.append('Direction')
                    timing.append(j)
                elif i =='10.1':
                    namedarr.append('Statement & Conclusion')
                    timing.append(j)
                elif i == '11.1':
                    namedarr.append('Venn Diagram')
                    timing.append(j)
                elif i == '12.1':
                    namedarr.append('Missing number')
                    timing.append(j)
                elif i == '13.1':
                    namedarr.append('Logical Sequence of words')
                    timing.append(j)
                elif i == '14.1':
                    namedarr.append('Clock/Time')
                    timing.append(j)
                elif i == '15.1':
                    namedarr.append('Mathematical Operations')
                    timing.append(j)
                elif i == '16.1':
                    namedarr.append('Coding Decoding')
                    timing.append(j)
                elif i == '17.1':
                    namedarr.append('Series Test')
                    timing.append(j)




            return list(zip(namedarr,timing))
        if subject == 'Quantitative-Analysis':
            for i,j in arr:
                if i == '1.1':
                    namedarr.append('Probability')
                    timing.append(j)
                elif i == '2.1':
                    namedarr.append('Percentage')
                    timing.append(j)
                elif i == '3.1':
                    namedarr.append('Pipes & Cisterns')
                    timing.append(j)
                elif i == '4.1':
                    namedarr.append('Simplification')
                    timing.append(j)
                elif i == '5.1':
                    namedarr.append('Permutations')
                    timing.append(j)
                elif i == '6.1':
                    namedarr.append('Simple Interest')
                    timing.append(j)
                elif i == '7.1':
                    namedarr.append('Partnership')
                    timing.append(j)
                elif i == '8.1':
                    namedarr.append('Averages')
                    timing.append(j)
                elif i == '9.1':
                    namedarr.append('Compound Interest')
                    timing.append(j)
                elif i == '11.1':
                    namedarr.append('Mixture and Alligations')
                    timing.append(j)
                elif i == '12.1':
                    namedarr.append('LCM & HCF')
                    timing.append(j)
                elif i == '13.1':
                    namedarr.append('Inequalities')
                    timing.append(j)
                elif i == '14.1':
                    namedarr.append('Ages')
                    timing.append(j)
                elif i == '15.1':
                    namedarr.append('Chain Rule')
                    timing.append(j)
                elif i == '16.1':
                    namedarr.append('Mensuration')
                    timing.append(j)
                elif i == '17.1':
                    namedarr.append('Ratio & Proportions')
                    timing.append(j)
                elif i == '18.1':
                    namedarr.append('Time & Distance')
                    timing.append(j)
                elif i == '19.1':
                    namedarr.append('Time & Work')
                    timing.append(j)
                elif i == '20.1':
                    namedarr.append('Number Series')
                    timing.append(j)
                elif i == '21.1':
                    namedarr.append('Number System')
                    timing.append(j)
                elif i == '22.1':
                    namedarr.append('Quadratic Equations')
                    timing.append(j)
                elif i == '23.1':
                    namedarr.append('Data Sufficiency')
                    timing.append(j)
                elif i == '24.1':
                    namedarr.append('Profit & Loss')
                    timing.append(j)
            return list(zip(namedarr,timing))
        if subject == 'General-Knowledge':
            for i,j in arr:
                if i == '1.1':
                    namedarr.append('Inventions & Innovators')
                    timing.append(j)
                if i == '2.1':
                   namedarr.append('Bird Sanctuary')
                   timing.append(j)
                if i == '3.1':
                   namedarr.append('Books & Authors')
                   timing.append(j)
                if i == '4.1':
                   namedarr.append('Countries, Capitals & Currencies')
                   timing.append(j)
                if i == '5.1':
                   namedarr.append('Current Affairs')
                   timing.append(j)
                if i == '6.1':
                   namedarr.append('Economics')
                   timing.append(j)
                if i == '7.1':
                   namedarr.append('General Science')
                   timing.append(j)
                if i == '8.1':
                   namedarr.append('Biology')
                   timing.append(j)
                if i == '9.1':
                   namedarr.append('Chemistry')
                   timing.append(j)
                if i == '10.1':
                   namedarr.append('Science & Technology')
                   timing.append(j)
                if i == '11.1':
                   namedarr.append('Physics')
                   timing.append(j)
                if i == '12.1':
                   namedarr.append('Geography')
                   timing.append(j)
                if i == '13.1':
                   namedarr.append('National Organizations')
                   timing.append(j)
                if i == '14.1':
                   namedarr.append('History')
                   timing.append(j)
                if i == '15.1':
                   namedarr.append('Honors & Awards')
                   timing.append(j)
                if i == '16.1':
                   namedarr.append('Important Dates')
                   timing.append(j)
                if i == '17.1':
                   namedarr.append('Indian Agriculture')
                   timing.append(j)
                if i == '18.1':
                   namedarr.append('Indian Constitution')
                   timing.append(j)
                if i == '19.1':
                   namedarr.append('Indian Culture')
                   timing.append(j)
                if i == '20.1':
                   namedarr.append('Indian Museums')
                   timing.append(j)
                if i == '21.1':
                   namedarr.append('Polity (India)')
                   timing.append(j)
                if i == '22.1':
                   namedarr.append('Sports')
                   timing.append(j)
                if i == '23.1':
                   namedarr.append('Superlatives(India)')
                   timing.append(j)
                if i == '24.1':
                   namedarr.append('Symbols of States (India)')
                   timing.append(j)
                if i == '25.1':
                   namedarr.append('Tiger Reserve')
                   timing.append(j)
                if i == '26.1':
                   namedarr.append('UNESCO Word Heritage Sites(India)')
                   timing.append(j)
                if i == '27.1':
                   namedarr.append('World Organizations')
                   timing.append(j)
                if i == '28.1':
                   namedarr.append('Polity (World)')
                   timing.append(j)
            return list(zip(namedarr,timing))

    def convertTopicNumbersNames(self,arr,subject):
        namedarr = []
        if subject == 'English':
            for i in arr:
                if i == '1.1':
                    namedarr.append('Word Meanings')
                elif i == '1.2':
                    namedarr.append('Idiom/Phrase Meaning')
                elif i == '2.1':
                    namedarr.append('Antonyms')
                elif i == '3.1':
                    namedarr.append('Alternate Phrases/Underlined')
                elif i == '3.2':
                    namedarr.append('Alternate words/Fill in the blanks')
                elif i == '4.1':
                    namedarr.append('Re-Arrangement')
                elif i == '5.1':
                    namedarr.append('Spelling')
                elif i == '6.1':
                    namedarr.append('Substitution')
                elif i == '7.1':
                    namedarr.append('Random')
                elif i == '8.1':
                    namedarr.append('Spot the Error')
                elif i == '9.1':
                    namedarr.append('Passage')
            return namedarr
        if subject == 'General-Intelligence':
            for i in arr:
                if i == '1.1':
                    namedarr.append('Paper Cutting and Folding')
                elif i == '1.2':
                    namedarr.append('Mirror and Water Image')
                elif i == '1.3':
                    namedarr.append('Embedded Figures')
                elif i == '1.4':
                    namedarr.append('Figure Completion')
                elif i == '1.5':
                    namedarr.append('Counting Embedded Figures')
                elif i == '1.6':
                    namedarr.append('Counting in figures')
                elif i == '2.1':
                    namedarr.append('Analogous pair')
                elif i == '2.2':
                    namedarr.append('Multiple Analogy')
                elif i == '2.3':
                    namedarr.append('Choosing the analogous pair')
                elif i == '2.4':
                    namedarr.append('Number analogy (series pattern)')
                elif i =='2.5':
                    namedarr.append('Number analogy (missing)')
                elif i == '2.6':
                    namedarr.append('Alphabet based analogy')
                elif i == '2.7':
                    namedarr.append('Mixed analogy')
                elif i == '3.1':
                    namedarr.append('Series Completion (Diagram)')
                elif i == '3.2':
                    namedarr.append('Analogy (Diagram)')
                elif i == '3.3':
                    namedarr.append('Classification (Diagram)')
                elif i == '3.4':
                    namedarr.append('Dice & Boxes')
                elif i == '2.8':
                    namedarr.append('Ruled based analogy')
                elif i == '2.9':
                    namedarr.append('Alphabet series (missing)')
                elif i == '4.1':
                    namedarr.append('Age')
                elif i == '5.1':
                    namedarr.append('Matrix')
                elif i == '6.1':
                    namedarr.append('Word Creation')
                elif i == '7.1':
                    namedarr.append('Odd one out')
                elif i == '8.1':
                    namedarr.append('Height')
                elif i == '9.1':
                    namedarr.append('Direction')
                elif i =='10.1':
                    namedarr.append('Statement & Conclusion')
                elif i == '11.1':
                    namedarr.append('Venn Diagram')
                elif i == '12.1':
                    namedarr.append('Missing number')
                elif i == '13.1':
                    namedarr.append('Logical Sequence of words')
                elif i == '14.1':
                    namedarr.append('Clock/Time')
                elif i == '15.1':
                    namedarr.append('Mathematical Operations')
                elif i == '16.1':
                    namedarr.append('Coding Decoding')
                elif i == '17.1':
                    namedarr.append('Series Test')







            return namedarr
        if subject == 'Qualitative-Analysis':
            for i in arr:
                if i == '1.1':
                    namedarr.append('Probability')
                elif i == '2.1':
                    namedarr.append('Percentage')
                elif i == '3.1':
                    namedarr.append('Pipes & Cisterns')
                elif i == '4.1':
                    namedarr.append('Simplification')
                elif i == '5.1':
                    namedarr.append('Permutations')
                elif i == '6.1':
                    namedarr.append('Simple Interest')
                elif i == '7.1':
                    namedarr.append('Partnership')
                elif i == '8.1':
                    namedarr.append('Averages')
                elif i == '9.1':
                    namedarr.append('Compound Interest')
                elif i == '11.1':
                    namedarr.append('Mixture and Alligations')
                elif i == '12.1':
                    namedarr.append('LCM & HCF')
                elif i == '13.1':
                    namedarr.append('Inequalities')
                elif i == '14.1':
                    namedarr.append('Ages')
                elif i == '15.1':
                    namedarr.append('Chain Rule')
                elif i == '16.1':
                    namedarr.append('Mensuration')
                elif i == '17.1':
                    namedarr.append('Ratio & Proportions')
                elif i == '18.1':
                    namedarr.append('Time & Distance')
                elif i == '19.1':
                    namedarr.append('Time & Work')
                elif i == '20.1':
                    namedarr.append('Number Series')
                elif i == '21.1':
                    namedarr.append('Number System')
                elif i == '22.1':
                    namedarr.append('Quadratic Equations')
                elif i == '23.1':
                    namedarr.append('Data Sufficiency')
            return namedarr 
        if subject == 'General-Knowledge':
            for i in arr:
                if i == '1.1':
                    namedarr.append('Inventions & Innovators')
                if i == '2.1':
                   namedarr.append('Bird Sanctuary')
                if i == '3.1':
                   namedarr.append('Books & Authors')
                if i == '4.1':
                   namedarr.append('Countries, Capitals & Currencies')
                if i == '5.1':
                   namedarr.append('Current Affairs')
                if i == '6.1':
                   namedarr.append('Economics')
                if i == '7.1':
                   namedarr.append('General Science')
                if i == '8.1':
                   namedarr.append('Biology')
                if i == '9.1':
                   namedarr.append('Chemistry')
                if i == '10.1':
                   namedarr.append('Science & Technology')
                if i == '11.1':
                   namedarr.append('Physics')
                if i == '12.1':
                   namedarr.append('Geography')
                if i == '13.1':
                   namedarr.append('National Organizations')
                if i == '14.1':
                   namedarr.append('History')
                if i == '15.1':
                   namedarr.append('Honors & Awards')
                if i == '16.1':
                   namedarr.append('Important Dates')
                if i == '17.1':
                   namedarr.append('Indian Agriculture')
                if i == '18.1':
                   namedarr.append('Indian Constitution')
                if i == '19.1':
                   namedarr.append('Indian Culture')
                if i == '20.1':
                   namedarr.append('Indian Museums')
                if i == '21.1':
                   namedarr.append('Polity (India)')
                if i == '22.1':
                   namedarr.append('Sports')
                if i == '23.1':
                   namedarr.append('Superlatives(India)')
                if i == '24.1':
                   namedarr.append('Symbols of States (India)')
                if i == '25.1':
                   namedarr.append('Tiger Reserve')
                if i == '26.1':
                   namedarr.append('UNESCO Word Heritage Sites(India)')
                if i == '27.1':
                   namedarr.append('World Organizations')
                if i == '28.1':
                   namedarr.append('Polity (World)')
            return namedarr
    def changeIndividualNames(self,i,subject):
        if subject == 'English':
            if i == '1.1':
                return 'Word Meanings'
            elif i == '1.2':
                return 'Idiom/Phrase Meaning'
            elif i == '2.1':
                return 'Antonyms'
            elif i == '3.1':
                return 'Alternate Phrases/Underlined'
            elif i == '3.2':
                return 'Alternate words/Fill in the blanks'
            elif i == '4.1':
                return 'Re-Arrangement'
            elif i == '5.1':
                return 'Spelling'
            elif i == '6.1':
                return 'Substitution'
            elif i == '7.1':
                return 'Random'
            elif i == '8.1':
                return 'Spot the Error'
            elif i == '9.1':
                return 'Passage'
        if subject == 'General-Intelligence':
            if i == '1.1':
                return 'Paper Cutting and Folding'
            elif i == '1.2':
                return 'Mirror and Water Image'
            elif i == '1.3':
                return 'Embedded Figures'
            elif i == '1.4':
                return 'Figure Completion'
            elif i == '1.5':
                return 'Counting Embedded Figures'
            elif i == '1.6':
                return 'Counting in figures'
            elif i == '2.1':
                return 'Analogous pair'
            elif i == '2.2':
                return 'Multiple Analogy'
            elif i == '2.3':
                return 'Choosing the analogous pair'
            elif i == '2.4':
                return 'Number analogy (series pattern)'
            elif i =='2.5':
                return 'Number analogy (missing)'
            elif i == '2.6':
                return 'Alphabet based analogy'
            elif i == '2.7':
                return 'Mixed analogy'
            elif i == '3.1':
                return 'Series Completion (Diagram)'
            elif i == '3.2':
                return 'Analogy (Diagram)'
            elif i == '3.3':
                return 'Classification (Diagram)'
            elif i == '3.4':
                return 'Dice & Boxes'
            elif i == '2.8':
                return 'Ruled based analogy'
            elif i == '2.9':
                return 'Alphabet series (missing)'
            elif i == '4.1':
                return 'Age'
            elif i == '5.1':
                return 'Matrix'
            elif i == '6.1':
                return 'Word Creation'
            elif i == '7.1':
                return 'Odd one out'
            elif i == '8.1':
                return 'Height'
            elif i == '9.1':
                return 'Direction'
            elif i =='10.1':
                return 'Statement & Conclusion'
            elif i == '11.1':
                return 'Venn Diagram'
            elif i == '12.1':
                return 'Missing number'
            elif i == '13.1':
                return 'Logical Sequence of words'
            elif i == '14.1':
                return 'Clock/Time'
            elif i == '15.1':
                return 'Mathematical Operations'
            elif i == '16.1':
                return 'Coding Decoding'
            elif i == '17.1':
                return 'Series Test'








        if subject == 'Quantitative-Analysis':
                if i == '1.1':
                    return 'Probability'
                elif i == '2.1':
                    return 'Percentage'
                elif i == '3.1':
                    return 'Pipes & Cisterns'
                elif i == '4.1':
                    return 'Simplification'
                elif i == '5.1':
                    return 'Permutations'
                elif i == '6.1':
                    return 'Simple Interest'
                elif i == '7.1':
                    return 'Partnership'
                elif i == '8.1':
                    return 'Averages'
                elif i == '9.1':
                    return 'Compound Interest'
                elif i == '11.1':
                    return 'Mixture and Alligations'
                elif i == '12.1':
                    return 'LCM & HCF'
                elif i == '13.1':
                    return 'Inequalities'
                elif i == '14.1':
                    return 'Ages'
                elif i == '15.1':
                    return 'Chain Rule'
                elif i == '16.1':
                    return 'Mensuration'
                elif i == '17.1':
                    return 'Ratio & Proportions'
                elif i == '18.1':
                    return 'Time & Distance'
                elif i == '19.1':
                    return 'Time & Work'
                elif i == '20.1':
                    return 'Number Series'
                elif i == '21.1':
                    return 'Number System'
                elif i == '22.1':
                    return 'Quadratic Equations'
                elif i == '23.1':
                    return 'Data Sufficiency'
        if subject == 'General-Knowledge':
                if i == '1.1':
                    return 'Inventions & Innovators'
                if i == '2.1':
                   return 'Bird Sanctuary'
                if i == '3.1':
                   return 'Books & Authors'
                if i == '4.1':
                   return 'Countries, Capitals & Currencies'
                if i == '5.1':
                   return 'Current Affairs'
                if i == '6.1':
                   return 'Economics'
                if i == '7.1':
                   return 'General Science'
                if i == '8.1':
                   return 'Biology'
                if i == '9.1':
                   return 'Chemistry'
                if i == '10.1':
                   return 'Science & Technology'
                if i == '11.1':
                   return 'Physics'
                if i == '12.1':
                   return 'Geography'
                if i == '13.1':
                   return 'National Organizations'
                if i == '14.1':
                   return 'History'
                if i == '15.1':
                   return 'Honors & Awards'
                if i == '16.1':
                   return 'Important Dates'
                if i == '17.1':
                   return 'Indian Agriculture'
                if i == '18.1':
                   return 'Indian Constitution'
                if i == '19.1':
                   return 'Indian Culture'
                if i == '20.1':
                   return 'Indian Museums'
                if i == '21.1':
                   return 'Polity (India)'
                if i == '22.1':
                   return 'Sports'
                if i == '23.1':
                   return 'Superlatives(India)'
                if i == '24.1':
                   return 'Symbols of States (India)'
                if i == '25.1':
                   return 'Tiger Reserve'
                if i == '26.1':
                   return 'UNESCO Word Heritage Sites(India)'
                if i == '27.1':
                   return 'World Organizations'
                if i == '28.1':
                   return 'Polity (World)'





    def improvement(self,subject):
        if self.institution == 'School':
            pass
        elif self.institution == 'SSC':
            marks = SSCOnlineMarks.objects.filter(student =
                                                  self.profile,test__sub =
                                                  subject)
            mixed_marks =\
            SSCOnlineMarks.objects.filter(student=self.profile,test__sub =
                                          'SSCMultipleSections')
            if marks:
                if len(marks)>1:
                    change = []
                    when = []
                    for j,k in enumerate(marks):
                        if j == len(marks)-1:
                            break
                        this = (k.marks/k.test.max_marks)*100 
                        that = marks[j+1]
                        that = (that.marks/that.test.max_marks)*100
                        diff = that-this
                        this_time = k.testTaken 
                        that_time = marks[j+1]
                        that_time = that_time.testTaken
                        time_diff = that_time - this_time
                        when.append(time_diff)
                        change.append(diff)
                    total_diff = list(zip(when,change))
                    return total_diff
                else:
                    return 'more than one needed'
            #if mixed_marks:
            #    if len(mixed_marks)>1:
            #        change = []
            #        for j,k in enumerate(mixed_marks):
            #            if j == len(mixed_marks)-1:
            #                break
            #            this = (k.marks/k.test.max_marks)*100 
            #            that = marks[j+1]
            #            that = (that.marks/that.test.max_marks)*100
            #            diff = that-this
            #            change.append(diff)
            #        return diff
            #    else:
            #        return 'more than one needed'


    def section_improvement(self,subject):
        if self.institution == 'School':
            pass
        elif self.institution == 'SSC':
            marks =\
            SSCOnlineMarks.objects.filter(student=self.profile,test__sub=subject).order_by('testTaken')
            mixed_marks =\
            SSCOnlineMarks.objects.filter(student=self.profile,test__sub='SSCMultipleSections').order_by('testTaken')
            total = []
            if marks:
                for i in marks:
                    total.append(i)
            if mixed_marks:
                for j in mixed_marks:
                    total.append(j)
            total.sort(key=lambda r:r.testTaken)

            topics = []
            day = []
            ra = []
            wa = []
            overall_accuracy = []
            for i in total:
                for r in i.rightAnswers:
                    rq = SSCquestions.objects.get(choices__id = r)
                    if rq.section_category == subject:
                        ra.append(rq)
                        cat = rq.topic_category
                        topics.append(cat)
                for w in i.wrongAnswers:
                    wq = SSCquestions.objects.get(choices__id = w)
                    if wq.section_category == subject:
                        wa.append(wq)
                        cat = wq.topic_category
                        topics.append(cat)
                topics = list(unique_everseen(topics))
                accuracy_dict = {}
                for j in topics:
                    right = 0
                    wrong = 0
                    for r in ra:
                        if r.topic_category == j:
                            right += 1
                    for w in wa:
                        if w.topic_category == j:
                            wrong += 1
                    total = right + wrong
                    accuracy = ((right-wrong)/total)*100
                    tp_j = self.changeIndividualNames(j,subject)
                    topic_accuracy = np.array([tp_j,accuracy,i.testTaken])
                    overall_accuracy.append(topic_accuracy)
            overall_accuracy = np.array(overall_accuracy)
            tp = []
            final_accuracy = []
            another_dict = {}
            try:
                for i in overall_accuracy[:,0]:
                    tp.append(i)
            except:
                return 0
            tp = list(unique_everseen(tp))
            for i in tp:
                name = eval("'topic'+str(i)")
                name_d = name
                name = []
                for n,j in enumerate(overall_accuracy[:,0]):
                    if j == i:
                        name.append(overall_accuracy[n])
                final_accuracy.append(name)
                another_dict[i] = {'dic':name}
            final_accuracy = np.array(final_accuracy)
            return another_dict
                   

            

                  




    def sectionwise_improvement(self,subject):
        if self.institution == 'School':
            pass
        elif self.institution == 'SSC':
            marks = SSCOnlineMarks.objects.filter(student =
                                                  self.profile,test__sub=
                                                  subject).order_by('id')
            mixed_marks = SSCOnlineMarks.objects.filter(student=
                                                        self.profile,test__sub
                                                        ='SSCMultipleSections').order_by('id')
            # get all the categories of questions that student has taken 
            all_categories = []
            if len(marks) > 1:
                all_answers = []
                quests = []
                skipped_answers = []
                for i in marks:
                    for aa in i.allAnswers:
                        all_answers.append(aa)
                    for sp in i.skippedAnswers:
                        skipped_answers.append(sp)
                for quest_id in all_answers:
                    quests.append(SSCquestions.objects.get(choices__id =
                                                           quest_id))
                #for quest_id in skipped_answers:
                #    quests.append(SSCquestions.objects.get(id = quest_id))
                for q in quests:
                    all_categories.append(q.topic_category)

            if mixed_marks:
                all_answers = []
                quests = []
                skipped_answers = []
                for i in mixed_marks:
                    for aa in i.allAnswers:
                        all_answers.append(aa)
                    for sp in i.skippedAnswers:
                        skipped_answers.append(sp)
                for quest_id in all_answers:
                    quests.append(SSCquestions.objects.get(choices__id =
                                                           quest_id))
                #for quest_id in skipped_answers:
                #    quests.append(SSCquestions.objects.get(id = quest_id))
                for q in quests:
                    all_categories.append(q.topic_category)
            all_categories = list(unique_everseen(all_categories))
            changes = {}
            changes_mixed = {}

            # get changes in accuracy topic wise (all questions answered
            # excluding not attempted questions)
            for tp in all_categories:
                test_count = 0
                for i in marks:
                    test_count += 1
                    rightCount = 0
                    allCount = 0
                    wCount = 0
                    for ra in i.rightAnswers:
                        quest = SSCquestions.objects.get(choices__id = ra)
                        if quest.topic_category == tp:
                            rightCount += 1
                            allCount += 1
                    for wa in i.wrongAnswers:
                        quest = SSCquestions.objects.get(choices__id = wa)
                        if quest.topic_category == tp:
                            wCount += 1
                            allCount += 1
                    #for sp in i.skippedAnswers:
                    #    quest = SSCquestions.objects.get(id = sp)
                    #    if quest.topic_category == tp:
                    #        wCount += 1
                    #        allCount += 1
                    try:
                        total = (((rightCount - wCount)/(rightCount+wCount))*100)
                        tpp = self.changeIndividualNames(tp,subject)

                        changes[str(tp)+','+str(test_count)] = {'topic':
                                                                tpp,'index':
                                                                test_count,'percent':total,'time':i.testTaken,'test_id':i.id}
                    except Exception as e:
                        print(str(e))
                test_count_mixed = 0
                for i in mixed_marks:
                    test_count_mixed += 1
                    rightCount = 0
                    allCount = 0
                    wCount = 0
                    for ra in i.rightAnswers:
                        quest = SSCquestions.objects.get(choices__id = ra)
                        if quest.topic_category == tp:
                            rightCount += 1
                            allCount += 1
                    for wa in i.wrongAnswers:
                        quest = SSCquestions.objects.get(choices__id = wa)
                        if quest.topic_category == tp:
                            wCount += 1
                            allCount += 1
                    for sp in i.skippedAnswers:
                        quest = SSCquestions.objects.get(id = sp)
                        if quest.topic_category == tp:
                            wCount += 1
                            allCount += 1
                    try:
                        total = (((rightCount - wCount)/(rightCount + wCount))*100)
                        tpp = self.changeIndividualNames(tp, subject)
                        changes_mixed[str(tp)+','+str(test_count)] = {'topic':
                                                                tpp,'index':
                                                                test_count_mixed,'percent':total,'time':i.testTaken,
                                                                      'test_id':i.id}
                    except Exception as e:
                        print(str(e))
            names_categories =\
            self.convertTopicNumbersNames(all_categories,subject)
            return changes,changes_mixed,names_categories

    def plot_improvement(self,subject):
        changes,mixed_changes,all_categories = self.sectionwise_improvement(subject)
        all_ids = []
        for key,value in changes.items():
            all_ids.append(value['test_id'])
        all_ids = list(unique_everseen(all_ids))
        all_ids.sort()

        #for i in all_ids:
        #    for k,v in changes.items():
        #        if v['test_id'] == i:
        #          time.append(v['time'])
        #          topic.append(v['topic'])
        #          percent.append(v['percent'])
        #          ind.append(i)
        #    overall = list(zip(ind,topic,percent,time))
        overall = {}
        final_list = []
        if all_categories:
            for i in all_categories:
                time = []
                testid = []
                ind = []
                percent = []

                for k,v in changes.items():
                    if changes[k]['topic'] == i:
                        time.append(changes[k]['time'])
                        testid.append(changes[k]['test_id'])
                        percent.append(changes[k]['percent'])
                overall[i] =\
                        {'time':time,'testid':testid,'percent':percent}
        if overall:
            return overall
        else:
            return None


class Teach:
    def __init__(self, user):
        self.profile = user.teacher
        self.institution = self.profile.school.category


    def my_classes_objects(self, klass_name=None):
        if klass_name:
            subs = self.profile.subject_set.all()
            if subs:
                klasses = []
                for sub in subs:
                    if sub.student.klass.name == klass_name:
                        klasses.append(sub.student.klass)
                return klasses[0]
            else:
                return None

        subs = self.profile.subject_set.all()
        if subs:
            klasses = []
            for sub in subs:
                klasses.append(sub.student.klass)
            return klasses
        else:
            return None

    def my_classes_names(self):
        subs = self.profile.subject_set.all()
        if subs:
            klasses = []
            for sub in subs:
                klasses.append(sub.student.klass.name)
            klasses = list(unique_everseen(klasses))
            return klasses
        else:
            return None

    def my_subjects_names(self):
        subs = self.profile.subject_set.all()
        subjects = []
        for i in subs:
            subjects.append(i.name)
        subjects = list(unique_everseen(subjects))
        return subjects

    def my_school(self):
        school = self.profile.school
        return school

    def listofStudents(self, klass):
        listofstudents = []
        subject_list = self.profile.subject_set.filter(student__klass__name=klass)
        for i in subject_list:
            listofstudents.append(i.student)
        return listofstudents

    def listofStudentsMarks(self, which_class):
        marks_class_test1 = []
        marks_class_test2 = []
        marks_class_test3 = []
        marks_class_predictedHy = []
        sub_class = self.profile.subject_set.filter(student__klass__name=which_class)
        if not sub_class:
            pass
        else:
            for i in sub_class:
                if i.test1:
                    marks_class_test1.append(i.test1)
                if i.test2:
                    marks_class_test2.append(i.test2)
                if i.test3:
                    marks_class_test3.append(i.test3)
                if i.predicted_hy:
                    marks_class_predictedHy.append(i.predicted_hy)
        return marks_class_test1, marks_class_test2, marks_class_test3, marks_class_predictedHy

    def teacher_get_testmarks_classwise(req, klass_dict):
        klass_test1_dict = {}  # dictionary to hold test1 marks of different classes
        klass_test2_dict = {}
        klass_test3_dict = {}

        # fill out the above dictionaries

        for i in klass_dict.values():
            kk = i
            klasstest1 = []
            klasstest2 = []
            klasstest3 = []

            for j in kk:
                klasstest1.append(j.test1)
                klasstest2.append(j.test2)
                klasstest3.append(j.test3)
                testm1 = {str(j.student.klass): klasstest1}
                testm2 = {str(j.student.klass): klasstest2}
                testm3 = {str(j.student.klass): klasstest3}
            klass_test1_dict.update(testm1)
            klass_test2_dict.update(testm2)
            klass_test3_dict.update(testm3)
        return klass_test1_dict, klass_test2_dict, klass_test2_dict

    def find_frequency_grades(self, test1, test2=None, test3=None):
        t1_fg_a = 0
        t1_fg_b = 0
        t1_fg_c = 0
        t1_fg_d = 0
        t1_fg_e = 0
        t1_fg_f = 0
        t1_fg_s = 0

        t2_fg_a = 0
        t2_fg_b = 0
        t2_fg_c = 0
        t2_fg_d = 0
        t2_fg_f = 0
        t2_fg_e = 0
        t2_fg_s = 0

        t3_fg_a = 0
        t3_fg_b = 0
        t3_fg_c = 0
        t3_fg_d = 0
        t3_fg_e = 0
        t3_fg_f = 0
        t3_fg_s = 0
        if test2 is None:

            for i in test1:
                if i == 'E':
                    t1_fg_e = t1_fg_e + 1
                elif i == 'F':
                    t1_fg_f = t1_fg_f + 1
                elif i == 'A':
                    t1_fg_a = t1_fg_a + 1
                elif i == 'B':
                    t1_fg_b = t1_fg_b + 1
                elif i == 'C':
                    t1_fg_c = t1_fg_c + 1
                elif i == 'D':
                    t1_fg_d = t1_fg_d + 1
                elif i == 'S':
                    t1_fg_s = t1_fg_s + 1
            return t1_fg_a, t1_fg_b, t1_fg_c, t1_fg_d, t1_fg_e, t1_fg_f, t1_fg_s

        elif test3 is None:
            for i in test1:
                if i == 'E':
                    t1_fg_e = t1_fg_e + 1
                elif i == 'F':
                    t1_fg_f = t1_fg_f + 1
                elif i == 'A':
                    t1_fg_a = t1_fg_a + 1
                elif i == 'B':
                    t1_fg_b = t1_fg_b + 1
                elif i == 'C':
                    t1_fg_c = t1_fg_c + 1
                elif i == 'D':
                    t1_fg_d = t1_fg_d + 1
                elif i == 'S':
                    t1_fg_s = t1_fg_s + 1

            for i in test2:
                if i == 'E':
                    t2_fg_e = t2_fg_e + 1
                elif i == 'F':
                    t2_fg_f = t2_fg_f + 1
                elif i == 'A':
                    t2_fg_a = t2_fg_a + 1
                elif i == 'B':
                    t2_fg_b = t2_fg_b + 1
                elif i == 'C':
                    t2_fg_c = t2_fg_c + 1
                elif i == 'D':
                    t2_fg_d = t2_fg_d + 1
                elif i == 'S':
                    t2_fg_s = t2_fg_s + 1

            return t1_fg_a, t1_fg_b, t1_fg_c, t1_fg_d, t1_fg_e, t1_fg_f, t1_fg_s, \
                   t2_fg_a, t2_fg_b, t2_fg_c, t2_fg_d, t2_fg_e, t2_fg_f, t2_fg_s
        else:
            for i in test1:
                if i == 'E':
                    t1_fg_e = t1_fg_e + 1
                elif i == 'F':
                    t1_fg_f = t1_fg_f + 1
                elif i == 'A':
                    t1_fg_a = t1_fg_a + 1
                elif i == 'B':
                    t1_fg_b = t1_fg_b + 1
                elif i == 'C':
                    t1_fg_c = t1_fg_c + 1
                elif i == 'D':
                    t1_fg_d = t1_fg_d + 1
                elif i == 'S':
                    t1_fg_s = t1_fg_s + 1

            for i in test2:
                if i == 'E':
                    t2_fg_e = t2_fg_e + 1
                elif i == 'F':
                    t2_fg_f = t2_fg_f + 1
                elif i == 'A':
                    t2_fg_a = t2_fg_a + 1
                elif i == 'B':
                    t2_fg_b = t2_fg_b + 1
                elif i == 'C':
                    t2_fg_c = t2_fg_c + 1
                elif i == 'D':
                    t2_fg_d = t2_fg_d + 1
                elif i == 'S':
                    t2_fg_s = t2_fg_s + 1
            for i in test3:
                if i == 'E':
                    t3_fg_e = t3_fg_e + 1
                elif i == 'F':
                    t3_fg_f = t3_fg_f + 1
                elif i == 'A':
                    t3_fg_a = t3_fg_a + 1
                elif i == 'B':
                    t3_fg_b = t3_fg_b + 1
                elif i == 'C':
                    t3_fg_c = t3_fg_c + 1
                elif i == 'D':
                    t3_fg_d = t3_fg_d + 1
                elif i == 'S':
                    t3_fg_s = t3_fg_s + 1
            return t1_fg_a, t1_fg_b, t1_fg_c, t1_fg_d, t1_fg_e, t1_fg_f, t1_fg_s, \
                   t2_fg_a, t2_fg_b, t2_fg_c, t2_fg_d, t2_fg_e, t2_fg_f, t2_fg_s, \
                   t3_fg_a, t3_fg_b, t3_fg_c, t3_fg_d, t3_fg_e, t3_fg_f, t3_fg_s

    def find_grade_from_marks(self, test1, test2=None, test3=None):
        test1_grade = []
        test2_grade = []
        test3_grade = []
        test1 = np.array(test1)
        if test2 is None:
            for i, n in enumerate(test1):
                if n < 4:
                    test1_grade.append('F')
                if 4 <= n < 5:
                    test1_grade.append('E')
                if 5 <= n < 6:
                    test1_grade.append('D')
                if 6 <= n < 7:
                    test1_grade.append('C')
                if 7 <= n < 8:
                    test1_grade.append('B')
                if 8 <= n < 9:
                    test1_grade.append('A')
                if 9 <= n <= 10:
                    test1_grade.append('S')
            return test1_grade
        elif test3 is None:

            test2 = np.array(test2)

            for i, n in enumerate(test1):
                if n < 4:
                    test1_grade.append('F')
                if 4 <= n < 5:
                    test1_grade.append('E')
                if 5 <= n < 6:
                    test1_grade.append('D')
                if 6 <= n < 7:
                    test1_grade.append('C')
                if 7 <= n < 8:
                    test1_grade.append('B')
                if 8 <= n < 9:
                    test1_grade.append('A')
                if 9 <= n <= 10:
                    test1_grade.append('S')

            for i, n in enumerate(test2):
                if n < 4:
                    test2_grade.append('F')
                if 4 <= n < 5:
                    test2_grade.append('E')
                if 5 <= n < 6:
                    test2_grade.append('D')
                if 6 <= n < 7:
                    test2_grade.append('C')
                if 7 <= n < 8:
                    test2_grade.append('B')
                if 8 <= n < 9:
                    test2_grade.append('A')
                if 9 <= n <= 10:
                    test2_grade.append('S')
            return test1_grade, test2_grade
        else:
            test2 = np.array(test2)
            test3 = np.array(test3)
            for i, n in enumerate(test1):
                if n < 4:
                    test1_grade.append('F')
                if 4 <= n < 5:
                    test1_grade.append('E')
                if 5 <= n < 6:
                    test1_grade.append('D')
                if 6 <= n < 7:
                    test1_grade.append('C')
                if 7 <= n < 8:
                    test1_grade.append('B')
                if 8 <= n < 9:
                    test1_grade.append('A')
                if 9 <= n <= 10: test1_grade.append('S')

            for i, n in enumerate(test2):
                if n < 4:
                    test2_grade.append('F')
                if 4 <= n < 5:
                    test2_grade.append('E')
                if 5 <= n < 6:
                    test2_grade.append('D')
                if 6 <= n < 7:
                    test2_grade.append('C')
                if 7 <= n < 8:
                    test2_grade.append('B')
                if 8 <= n < 9:
                    test2_grade.append('A')
                if 9 <= n < 11:
                    test2_grade.append('S')
            for i, n in enumerate(test3):
                if n < 4:
                    test3_grade.append('F')
                if 4 <= n < 5:
                    test3_grade.append('E')
                if 5 <= n < 6:
                    test3_grade.append('D')
                if 6 <= n < 7:
                    test3_grade.append('C')
                if 7 <= n < 8:
                    test3_grade.append('B')
                if 8 <= n < 9:
                    test3_grade.append('A')
                if 9 <= n <= 10:
                    test3_grade.append('S')
            return test1_grade, test2_grade, test3_grade

    def averageoftest(self, test, test2=None, test3=None):
        if test2 is None and test3 is None:
            testmarks = np.array(test)
            return np.mean(testmarks)
        elif test3 is None:
            testmarks = np.array(test)
            testmarks2 = np.array(test2)
            return np.mean(testmarks), np.mean(testmarks2)
        else:
            testmarks = np.array(test)
            testmarks2 = np.array(test2)
            testmarks3 = np.array(test3)
            return np.mean(testmarks), np.mean(testmarks2), np.mean(testmarks3)

    def school_test_analysis(self, test):
        average_test = self.averageoftest(test)
        g1 = self.find_grade_from_marks(test)
        t1_fg_a, t1_fg_b, t1_fg_c, t1_fg_d, t1_fg_e, t1_fg_f, t1_fg_s = \
            self.find_frequency_grades(g1)
        context = \
            {'testav': average_test, 't1_fg_a': t1_fg_a, 't1_fg_b': t1_fg_b,
             't1_fg_c': t1_fg_c, 't1_fg_d': t1_fg_d, 't1_fg_e': t1_fg_e, 't1_fg_f': t1_fg_f,
             't1_fg_s': t1_fg_s}
        return context
    def online_findAverageofTest(self, test_id, percent=None):
        if self.institution == 'School':
            if percent:
                test = OnlineMarks.objects.filter(test__id=test_id)
                all_marks = []
                all_marks_percent = []
                for te in test:
                    all_marks.append(int(te.marks))
                    all_marks_percent.append((te.marks / te.test.max_marks) * 100)
                average = np.mean(all_marks)
                percent_average = np.mean(all_marks_percent)
                return average, percent_average
            else:
                test = OnlineMarks.objects.filter(test__id=test_id)
                all_marks = []
                for te in test:
                    all_marks.append(int(te.marks))
                average = np.mean(all_marks)

                return average
        elif self.institution == 'SSC':
            if percent:
                test = SSCOnlineMarks.objects.filter(test__id=test_id)
                all_marks = []
                all_marks_percent = []
                for te in test:
                    all_marks.append(int(te.marks))
                    all_marks_percent.append((te.marks / te.test.max_marks) * 100)
                average = np.mean(all_marks)
                percent_average = np.mean(all_marks_percent)
                return average, percent_average
            else:
                test = SSCOnlineMarks.objects.filter(test__id=test_id)
                all_marks = []
                for te in test:
                    all_marks.append(int(te.marks))
                average = np.mean(all_marks)
                return average


    def offline_findAverageofTest(self, test_id, percent=None):
        if self.institution == 'School':
            if percent:
                test = OnlineMarks.objects.filter(test__id=test_id)
                all_marks = []
                all_marks_percent = []
                for te in test:
                    all_marks.append(int(te.marks))
                    all_marks_percent.append((te.marks / te.test.max_marks) * 100)
                average = np.mean(all_marks)
                percent_average = np.mean(all_marks_percent)
                return average, percent_average
            else:
                test = OnlineMarks.objects.filter(test__id=test_id)
                all_marks = []
                for te in test:
                    all_marks.append(int(te.marks))
                average = np.mean(all_marks)

                return average
        elif self.institution == 'SSC':
            if percent:
                test = SSCOfflineMarks.objects.filter(test__id=test_id)
                all_marks = []
                all_marks_percent = []
                for te in test:
                    all_marks.append(int(te.marks))
                    all_marks_percent.append((te.marks / te.test.max_marks) * 100)
                average = np.mean(all_marks)
                percent_average = np.mean(all_marks_percent)
                return average, percent_average
            else:
                test = SSCOfflineMarks.objects.filter(test__id=test_id)
                all_marks = []
                for te in test:
                    all_marks.append(int(te.marks))
                average = np.mean(all_marks)
                return average

    def online_freqeucyGrades(self,test_id,mode = None):
        if self.institution == 'School':
            test = OnlineMarks.objects.filter(test__id = test_id)
        elif self.institution == 'SSC':
            if mode =='offline':
                test = SSCOfflineMarks.objects.filter(test__id = test_id)
            else:
                test = SSCOnlineMarks.objects.filter(test__id = test_id)
        all_marks = []
        for i in test:
            all_marks.append((i.marks/i.test.max_marks)*100)
        grade_s = 0
        grade_a = 0
        grade_b = 0
        grade_c = 0
        grade_d = 0
        grade_e = 0
        grade_f = 0
        for marks in all_marks:
            if math.ceil(marks) < 33:
                grade_f +=1
            elif 33 <= math.ceil(marks) < 50:
                grade_e +=1
            elif 50 <= math.ceil(marks) < 60:
                grade_d +=1
            elif 60 <= math.ceil(marks) < 70:
                grade_c +=1
            elif 70 <= math.ceil(marks) < 80:
                grade_b +=1
            elif 80 <= math.ceil(marks) < 90:
                grade_a +=1
            elif 90 <= math.ceil(marks) <= 100:
                grade_s +=1
        return grade_s,grade_a,grade_b,grade_c,grade_d,grade_e,grade_f 

    def online_QuestionPercentage(self, test_id):
        if self.institution == 'School':
            online_marks = OnlineMarks.objects.filter(test__id=test_id)
        elif self.institution == 'SSC':
            online_marks = SSCOnlineMarks.objects.filter(test__id=test_id)
        all_answers = []
        for aa in online_marks:
            all_answers.extend(aa.allAnswers)
        unique, counts = np.unique(all_answers, return_counts=True)
        freq = np.asarray((unique, counts)).T
        return freq

    def offline_QuestionPercentage(self, test_id):
        if self.institution == 'School':
            offline_marks = OnlineMarks.objects.filter(test__id=test_id)
        elif self.institution == 'SSC':
            offline_marks = SSCOfflineMarks.objects.filter(test__id=test_id)
        all_answers = []
        for aa in offline_marks:
            all_answers.extend(aa.allAnswers)
        unique, counts = np.unique(all_answers, return_counts=True)
        freq = np.asarray((unique, counts)).T
        return freq

   



    def online_skippedQuestions(self,test_id,mode=None):
        if self.institution == 'School':
            online_marks = OnlineMarks.objects.filter(test__id=test_id)
        elif self.institution == 'SSC':
            if mode == 'offline':
                online_marks = SSCOnlineMarks.objects.filter(test__id=test_id)
            else:
                online_marks = SSCOfflineMarks.objects.filter(test__id=test_id)
        skipped_questions = []
        for om in online_marks:
            for sq in om.skippedAnswers:
                skipped_questions.append(sq)
        unique, counts = np.unique(skipped_questions, return_counts=True)
        sq = np.asarray((unique, counts)).T
        return sq
        
    def online_problematicAreasperTest(self,test_id):
        if self.institution == 'School':
            online_marks = OnlineMarks.objects.filter(test__id = test_id)
            wrong_answers = []
            for om in online_marks:
                for wa in om.wrongAnswers:
                    wrong_answers.append(wa)
            wq = []
            for i in wrong_answers:
                qu = Questions.objects.get(choices__id = i)
                quid = qu.id
                wq.append(quid)

            unique, counts = np.unique(wq, return_counts=True)
            waf = np.asarray((unique, counts)).T
            nw_ind = []
            kk = np.sort(waf,0)[::-1]
            for u in kk[:,1]:
                for z,w in waf:
                    if u == w:
                        if z in nw_ind:
                            continue
                        else:
                            nw_ind.append(z)
                            break
            final_freq = np.asarray((nw_ind,kk[:,1])).T
            return final_freq
        elif self.institution == 'SSC':
            online_marks = SSCOnlineMarks.objects.filter(test__id = test_id)
            wrong_answers = []
            for om in online_marks:
                for wa in om.wrongAnswers:
                    wrong_answers.append(wa)
            wq = []
            for i in wrong_answers:
                qu = SSCquestions.objects.get(choices__id = i)
                quid = qu.id
                wq.append(quid)

            unique, counts = np.unique(wq, return_counts=True)
            waf = np.asarray((unique, counts)).T
            nw_ind = []
            kk = np.sort(waf,0)[::-1]
            for u in kk[:,1]:
                for z,w in waf:
                    if u == w:
                        if z in nw_ind:
                            continue
                        else:
                            nw_ind.append(z)
                            break
            final_freq = np.asarray((nw_ind,kk[:,1])).T
            return final_freq
    def offline_problematicAreasperTest(self,test_id):
        if self.institution == 'School':
            online_marks = OnlineMarks.objects.filter(test__id = test_id)
            wrong_answers = []
            for om in online_marks:
                for wa in om.wrongAnswers:
                    wrong_answers.append(wa)
            wq = []
            for i in wrong_answers:
                qu = Questions.objects.get(choices__id = i)
                quid = qu.id
                wq.append(quid)

            unique, counts = np.unique(wq, return_counts=True)
            waf = np.asarray((unique, counts)).T
            nw_ind = []
            kk = np.sort(waf,0)[::-1]
            for u in kk[:,1]:
                for z,w in waf:
                    if u == w:
                        if z in nw_ind:
                            continue
                        else:
                            nw_ind.append(z)
                            break
            final_freq = np.asarray((nw_ind,kk[:,1])).T
            return final_freq
        elif self.institution == 'SSC':
            online_marks = SSCOfflineMarks.objects.filter(test__id = test_id)
            wrong_answers = []
            for om in online_marks:
                for wa in om.wrongAnswers:
                    wrong_answers.append(wa)
            wq = []
            for i in wrong_answers:
                qu = SSCquestions.objects.get(choices__id = i)
                quid = qu.id
                wq.append(quid)

            unique, counts = np.unique(wq, return_counts=True)
            waf = np.asarray((unique, counts)).T
            nw_ind = []
            kk = np.sort(waf,0)[::-1]
            for u in kk[:,1]:
                for z,w in waf:
                    if u == w:
                        if z in nw_ind:
                            continue
                        else:
                            nw_ind.append(z)
                            break
            final_freq = np.asarray((nw_ind,kk[:,1])).T
            return final_freq


    def online_problematicAreas(self,user,subject,klass):
        if self.institution == 'School':
            online_marks = OnlineMarks.objects.filter(test__creator= user,test__sub=
                                                  subject,test__klas__name = klass)
        elif self.institution == 'SSC':
            online_marks = SSCOnlineMarks.objects.filter(test__creator= user,test__sub=
                                                  subject,test__klas__name = klass)
            all_onlineMarks = SSCOnlineMarks.objects.filter(test__creator =
                                                            user,test__sub =
                                                            'SSCMultipleSections',test__klas__name=
                                                            klass)
            offline_marks = SSCOfflineMarks.objects.filter(test__creator =
                                                           user,test__sub =
                                                           subject,test__klas__name
                                                           = klass)
            all_offlinemarks = SSCOfflineMarks.objects.filter(test__creator =
                                                               user,test__sub =
                                                               'SSCMultipleSections',test__klas__name
                                                            = klass)
        wrong_answers = []
        skipped_answers = []
        if online_marks:
            for om in online_marks:
                for wa in om.wrongAnswers:
                    wrong_answers.append(wa)
                for sp in om.skippedAnswers:
                    skipped_answers.append(sp) 
            
            
        if all_onlineMarks:
            for om in all_onlineMarks:
                for wa in om.wrongAnswers:
                    wrong_answers.append(wa)
                for sp in om.skippedAnswers:
                    skipped_answers.append(sp)
        if offline_marks:
            for om in offline_marks:
                for wa in om.wrongAnswers:
                    wrong_answers.append(wa)
                for sp in om.skippedAnswers:
                    skipped_answers.append(sp) 
        if all_offlinemarks:
            for om in all_offlinemarks:
                for wa in om.wrongAnswers:
                    wrong_answers.append(wa)
                for sp in om.skippedAnswers:
                    skipped_answers.append(sp)


        wq = []
        for i in wrong_answers:
            if self.institution == 'School':
                qu = Questions.objects.get(choices__id = i)
            elif self.institution == 'SSC':
                try:
                    qu = SSCquestions.objects.get(choices__id = i)
                except Exception as e:
                    print(str(e))
                    continue
            if qu.section_category == subject:
                quid = qu.id
                wq.append(quid)
        for i in skipped_answers:
            if self.institution == 'School':
                try:
                    qu = Questions.objects.get(id = i)
                except Exception as e:
                    print(str(e))
                    continue
            elif self.institution == 'SSC':
                try:
                    qu = SSCquestions.objects.get(id = i)
                except Exception as e:
                    print(str(e))
                    continue
            if qu.section_category == subject:
                quid = qu.id
                wq.append(quid)

        unique, counts = np.unique(wq, return_counts=True)
        waf = np.asarray((unique, counts)).T
        nw_ind = []
        kk = np.sort(waf,0)[::-1]
        for u in kk[:,1]:
            for z,w in waf:
                if u == w:
                    if z in nw_ind:
                        continue
                    else:
                        nw_ind.append(z)
                        break
        final_freq = np.asarray((nw_ind,kk[:,1])).T
        return final_freq
        
    def online_problematicAreasNames(self,user,subject,klass):
        arr = self.online_problematicAreas(user,subject,klass)
        if self.institution == 'School':
            how_many = 0
            areas = []
            for u,k in arr:
                if how_many == 3:
                    break
                qu = Questions.objects.get(id = u)
                cat = qu.topic_category
                areas.append(cat)
                how_many += 1
            areas = list(unique_everseen(areas))
            area_names=  self.change_topicNumbersNames(arr,subject)
            return areas
        elif self.institution == 'SSC':
            how_many = 0
            areas = []
            for u,k in arr:
                if how_many == 3:
                    break
                qu = SSCquestions.objects.get(id = u)
                cat = qu.topic_category
                areas.append(cat)
                how_many += 1
            areas = list(unique_everseen(areas))
            area_names=  self.change_topicNumbersNames(areas,subject)
            area_names = np.array(area_names)
            return area_names[:,0]

    def online_problematicAreaswithIntensity(self,user,subject,klass):
        arr = self.online_problematicAreas(user,subject,klass)
        anal = []
        num = []
        for u,k in arr:
            if self.institution == 'School':
                qu = Questions.objects.get(id = u)
            elif self.institution == 'SSC':
                qu = SSCquestions.objects.get(id = u)
            category = qu.topic_category
            anal.append(category)
            num.append(k)
        analysis = list(zip(anal,num))
        final_analysis = []
        final_num = []
        for u,k in analysis:
            if u in final_analysis:
                ind = final_analysis.index(u)
                temp = final_num[ind]
                final_num[ind] = temp + k
            else:
                final_analysis.append(u)
                final_num.append(k)
        # weak areas frequency
        waf = list(zip(final_analysis,final_num))
        return waf
    def online_problematicAreaswithIntensityAverage(self,user,subject,klass):
        if self.institution  == 'School':
            pass
        elif self.institution == 'SSC':
            arr = self.online_problematicAreaswithIntensity(user,subject,klass)
            total_arr = SSCOnlineMarks.objects.filter(test__creator =
                                                      user,test__sub =
                                                      subject,test__klas__name
                                                     = klass) 
            all_total_arr = SSCOnlineMarks.objects.filter(test__creator =
                                                          user,test__sub=
                                                          'SSCMultipleSections',test__klas__name
                                                     = klass)
            offline_total_arr = SSCOfflineMarks.objects.filter(test__creator =
                                                               user,test__sub =
                                                               subject,test__klas__name
                                                               = klass)
            all_offline_total_arr =\
            SSCOfflineMarks.objects.filter(test__creator = user,test__sub =
                                           'SSCMultipleSections',test__klas__name
                                           = klass)
            quest_categories = []
            if total_arr:
                for ta in total_arr:
                    for al in ta.allAnswers:
                        try:
                            quest = SSCquestions.objects.get(choices__id = al)
                        except Exception as e:
                            print(str(e))
                            continue
                        quest_categories.append(quest.topic_category)
                    for sk in ta.skippedAnswers:
                        try:
                            quest = SSCquestions.objects.get(id = sk)
                        except Exception as e:
                            print(str(e))
                            continue
                        quest_categories.append(quest.topic_category)
            if all_total_arr:
                for ta in all_total_arr:
                    for al in ta.allAnswers:
                        try:
                            quest = SSCquestions.objects.get(choices__id = al)
                        except Exception   as e:
                            print(str(e))
                            continue
                        quest_categories.append(quest.topic_category)
                    for sk in ta.skippedAnswers:
                        try:
                            quest = SSCquestions.objects.get(id = sk)
                        except Exception   as e:
                            print(str(e))
                            continue
                        quest_categories.append(quest.topic_category)
            if offline_total_arr:
                 for ta in offline_total_arr:
                    for al in ta.allAnswers:
                        try:
                            quest = SSCquestions.objects.get(choices__id = al)
                        except Exception   as e:
                            print(str(e))
                            continue
                        quest_categories.append(quest.topic_category)
                    for sk in ta.skippedAnswers:
                        try:
                            quest = SSCquestions.objects.get(id = sk)
                        except Exception   as e:
                            print(str(e))
                            continue
                        quest_categories.append(quest.topic_category)
            if all_offline_total_arr:
                 for ta in all_offline_total_arr:
                    for al in ta.allAnswers:
                        try:
                            quest = SSCquestions.objects.get(choices__id = al)
                        except Exception   as e:
                            print(str(e))
                            continue
                        quest_categories.append(quest.topic_category)
                    for sk in ta.skippedAnswers:
                        try:
                            quest = SSCquestions.objects.get(id = sk)
                        except Exception   as e:
                            print(str(e))
                            continue
                        quest_categories.append(quest.topic_category)
              

            unique, counts = np.unique(quest_categories, return_counts=True)
            waf = np.asarray((unique, counts)).T
            arr = np.array(arr)
            average_cat = []
            average_percent = []
            for i,j in waf:
                if i in arr[:,0]:
                    ind = np.where(arr==i)
                    now_arr = arr[ind[0],1]
                    average =(int(now_arr[0])/int(j)*100)
                    average_cat.append(i)
                    average_percent.append(average)
            weak_average = list(zip(average_cat,average_percent))
            return weak_average

    def weakAreas_timing(self,user,subject,klass):
        all_questions = []
        all_timing = []
        if self.institution == 'School':
            marks = OnlineMarks.objects.filter(test__sub =
                                               subject,test__creator =
                                            user)
            for om in marks:
                for aq in om.sscansweredquestion_set.all():
                    all_questions.append(aq.quest.topic_category)
                    all_timing.append(aq.time)

        elif self.institution == 'SSC':
            marks = SSCOnlineMarks.objects.filter(test__sub = subject,
                                                  test__creator =
                                                  user)
            every_marks = SSCOnlineMarks.objects.filter(test__sub =
                                                        'SSCMultipleSections',test__creator
                                                        = user)
            for om in marks:
                for aq in om.sscansweredquestion_set.all():
                    all_questions.append(aq.quest.topic_category)
                    all_timing.append(aq.time)
            if every_marks:
                for om in every_marks:
                    for al in om.sscansweredquestion_set.all():
                        if al.quest.section_category == subject:
                            all_questions.append(al.quest.topic_category)
                            all_timing.append(al.time)

        areawise_timing = list(zip(all_questions,all_timing))
        dim1 = list(unique_everseen(all_questions))
        dim3 = []
        dim4 = []
        freq = []
        for j in dim1:
            k_val = 0
            n = 0
            for x,y in areawise_timing:
                if j == x and y != -1:
                    k_val += y
                    n += 1
            dim3.append(j)
            try:
                average_time = float(k_val/n)
                dim4.append(average_time)
                freq.append(n)
            except:
                pass
        timing = list(zip(dim3,dim4))
        freq_list = list(zip(dim3,freq))
        return timing,freq_list

    def find_classRank(self,li):
        array = np.array(li)
        temp = array.argsort()
        ranks = np.empty(len(array), int)
        ranks[temp] = np.arange(len(array))
        final_rank = []
        for j in ranks:
            final_rank.append(((len(li)-j)))
        return final_rank


    def generate_rankTable(self,test_id,mode=None):
        if mode:
            all_marks = SSCOfflineMarks.objects.filter(test__id = test_id)
        else:
            all_marks = SSCOnlineMarks.objects.filter(test__id = test_id)
        names = []
        totalMarks = []
        scores = []
        percentage = []
        numCorrect = []
        numIncorrect = []
        numSkipped = []
        # get total marks and put in a list
        for i in all_marks:
            names.append(i.student.name)
            totalMarks.append(i.test.max_marks)
            scores.append(i.marks)
            percentage.append((i.marks/i.test.max_marks)*100)
            numCorrect.append(len(i.rightAnswers))
            numIncorrect.append(len(i.wrongAnswers))
            numSkipped.append(len(i.skippedAnswers))
        rank = self.find_classRank(scores)
        result =\
        list(zip(names,totalMarks,scores,rank,percentage,numCorrect,numIncorrect,numSkipped))
        return np.array(result)
        

        





    def change_topicNumbersNames(self,arr,subject):
        names = []
        numbers = []
        if subject == 'English':
            for i in arr:
                if i == '1.1':
                    names.append('Word Meanings')
                    numbers.append(i)
                elif i == '1.2':
                    names.append('Idiom/Phrase Meaning')
                    numbers.append(i)
                elif i == '2.1':
                    names.append('Antonyms')
                    numbers.append(i)
                elif i == '3.1':
                    names.append('Alternate Phrases/Underlined')
                    numbers.append(i)
                elif i == '3.2':
                    names.append('Alternate words/Fill in the blanks')
                    numbers.append(i)
                elif i == '4.1':
                    names.append('Re-Arrangement')
                    numbers.append(i)
                elif i == '5.1':
                    names.append('Spelling')
                    numbers.append(i)
                elif i == '6.1':
                    names.append('Substitution')
                    numbers.append(i)
                elif i == '7.1':
                    names.append('Random')
                    numbers.append(i)
                elif i == '8.1':
                    names.append('Spot the Error')
                    numbers.append(i)
                elif i == '9.1':
                    names.append('Passage')
                    numbers.append(i)
            changed = list(zip(names,numbers))
            return changed
        if subject == 'General-Intelligence':
            for i in arr:
                if i == '1.1':
                    names.append('Paper cutting and Folding')
                    numbers.append(i)
                elif i == '1.2':
                    names.append('Mirror and Water Image')
                    numbers.append(i)
                elif i == '1.3':
                    names.append('Embedded Figures')
                    numbers.append(i)
                elif i == '1.4':
                    names.append('Figure Completion')
                    numbers.append(i)
                elif i == '1.5':
                    names.append('Counting of embedded figures')
                    numbers.append(i)
                elif i == '1.6':
                    names.append('Counting of figures')
                    numbers.append(i)
                elif i == '2.1':
                    names.append('Analogous pair')
                    numbers.append(i)
                elif i == '2.2':
                    names.append('Multiple Analogy')
                    numbers.append(i)
                elif i == '2.3':
                    names.append('Choosing the analogous pair')
                    numbers.append(i)
                elif i == '2.4':
                    names.append('Number analogy (series pattern)')
                    numbers.append(i)
                elif i =='2.5':
                    names.append('Number analogy (missing)')
                    numbers.append(i)
                elif i == '2.6':
                    names.append('Alphabet based analogy')
                    numbers.append(i)
                elif i == '2.7':
                    names.append('Mixed analogy')
                    numbers.append(i)
                elif i == '3.1':
                    names.append('Series Completion (Diagram)')
                    numbers.append(i)
                elif i == '3.2':
                    names.append('Analogy (Diagram)')
                    numbers.append(i)
                elif i == '3.3':
                    names.append('Classification (Diagram)')
                    numbers.append(i)
                elif i == '3.4':
                    names.append('Dice & Boxes')
                    numbers.append(i)
                elif i == '2.8':
                    names.append('Ruled based analogy')
                    numbers.append(i)
                elif i == '2.9':
                    names.append('Alphabet series (missing)')
                    numbers.append(i)
                elif i == '4.1':
                    names.append('Age')
                    numbers.append(i)
                elif i == '5.1':
                    names.append('Matrix')
                    numbers.append(i)
                elif i == '6.1':
                    names.append('Word Creation')
                    numbers.append(i)
                elif i == '7.1':
                    names.append('Odd one out')
                    numbers.append(i)
                elif i == '8.1':
                    names.append('Height')
                    numbers.append(i)
                elif i == '9.1':
                    names.append('Direction')
                    numbers.append(i)
                elif i =='10.1':
                    names.append('Statement & Conclusion')
                    numbers.append(i)
                elif i == '11.1':
                    names.append('Venn Diagram')
                    numbers.append(i)
                elif i == '12.1':
                    names.append('Missing number')
                    numbers.append(i)
                elif i == '13.1':
                    names.append('Logical Sequence of words')
                    numbers.append(i)
                elif i == '14.1':
                    names.append('Clock/Time')
                    numbers.append(i)
                elif i == '15.1':
                    names.append('Mathematical Operations')
                    numbers.append(i)
                elif i == '16.1':
                    names.append('Coding Decoding')
                    numbers.append(i)
                elif i == '17.1':
                    names.append('Series Test')
                    numbers.append(i)







            changed = list(zip(names,numbers))
            return changed
        if subject == 'Quantitative-Analysis':
            for i in arr:
                if i == '1.1':
                    names.append('Probability')
                    numbers.append(i)
                elif i == '2.1':
                    names.append('Percentage')
                    numbers.append(i)
                elif i == '3.1':
                    names.append('Pipes & Cisterns')
                    numbers.append(i)
                elif i == '4.1':
                    names.append('Simplification')
                    numbers.append(i)
                elif i == '5.1':
                    names.append('Permutations')
                    numbers.append(i)
                elif i == '6.1':
                    names.append('Simple Interest')
                    numbers.append(i)
                elif i == '7.1':
                    names.append('Partnership')
                    numbers.append(i)
                elif i == '8.1':
                    names.append('Averages')
                    numbers.append(i)
                elif i == '9.1':
                    names.append('Compound Interest')
                    numbers.append(i)
                elif i == '11.1':
                    names.append('Mixture and Alligations')
                    numbers.append(i)
                elif i == '12.1':
                    names.append('LCM & HCF')
                    numbers.append(i)
                elif i == '13.1':
                    names.append('Inequalities')
                    numbers.append(i)
                elif i == '14.1':
                    names.append('Ages')
                    numbers.append(i)
                elif i == '15.1':
                    names.append('Chain Rule')
                    numbers.append(i)
                elif i == '16.1':
                    names.append('Mensuration')
                    numbers.append(i)
                elif i == '17.1':
                    names.append('Ratio & Proportions')
                    numbers.append(i)
                elif i == '18.1':
                    names.append('Time & Distance')
                    numbers.append(i)
                elif i == '19.1':
                    names.append('Time & Work')
                    numbers.append(i)
                elif i == '20.1':
                    names.append('Number Series')
                    numbers.append(i)
                elif i == '21.1':
                    names.append('Number System')
                    numbers.append(i)
                elif i == '22.1':
                    names.append('Quadratic Equations')
                    numbers.append(i)
                elif i == '23.1':
                    names.append('Data Sufficiency')
                    numbers.append(i)
 
            changed = list(zip(names,numbers))
            return changed
        if subject == 'General-Knowledge':
            for i in arr:
                if i == '1.1':
                    names.append('Inventions & Innovators')
                if i == '2.1':
                    names.append('Bird Sanctuary')
                    numbers.append(i)
                if i == '3.1':
                    names.append('Books & Authors')
                    numbers.append(i)
                if i == '4.1':
                    names.append('Countries, Capitals & Currencies')
                    numbers.append(i)
                if i == '5.1':
                    names.append('Current Affairs')
                    numbers.append(i)
                if i == '6.1':
                    names.append('Economics')
                    numbers.append(i)
                if i == '7.1':
                    names.append('General Science')
                    numbers.append(i)
                if i == '8.1':
                    names.append('Biology')
                    numbers.append(i)
                if i == '9.1':
                    names.append('Chemistry')
                    numbers.append(i)
                if i == '10.1':
                    names.append('Science & Technology')
                    numbers.append(i)
                if i == '11.1':
                    names.append('Physics')
                    numbers.append(i)
                if i == '12.1':
                    names.append('Geography')
                    numbers.append(i)
                if i == '13.1':
                    names.append('National Organizations')
                    numbers.append(i)
                if i == '14.1':
                    names.append('History')
                    numbers.append(i)
                if i == '15.1':
                    names.append('Honors & Awards')
                    numbers.append(i)
                if i == '16.1':
                    names.append('Important Dates')
                    numbers.append(i)
                if i == '17.1':
                    names.append('Indian Agriculture')
                    numbers.append(i)
                if i == '18.1':
                    names.append('Indian Constitution')
                    numbers.append(i)
                if i == '19.1':
                    names.append('Indian Culture')
                    numbers.append(i)
                if i == '20.1':
                    names.append('Indian Museums')
                    numbers.append(i)
                if i == '21.1':
                    names.append('Polity (India)')
                    numbers.append(i)
                if i == '22.1':
                    names.append('Sports')
                    numbers.append(i)
                if i == '23.1':
                    names.append('Superlatives(India)')
                    numbers.append(i)
                if i == '24.1':
                    names.append('Symbols of States (India)')
                    numbers.append(i)
                if i == '25.1':
                    names.append('Tiger Reserve')
                    numbers.append(i)
                if i == '26.1':
                    names.append('UNESCO Word Heritage Sites(India)')
                    numbers.append(i)
                if i == '27.1':
                    names.append('World Organizations')
                    numbers.append(i)
                if i == '28.1':
                    names.append('Polity (World)')
                    numbers.append(i)
            changed = list(zip(names,numbers))
            return changed

    
    
    def change_topicNumbersNamesWeakAreas(self,arr,subject):
        names = []
        numbers = []
        if subject == 'English':
            for i,j in arr:
                if i == '1.1':
                    names.append('Word Meanings')
                    numbers.append(j)
                elif i == '1.2':
                    names.append('Idiom/Phrase Meaning')
                    numbers.append(j)
                elif i == '2.1':
                    names.append('Antonyms')
                    numbers.append(j)
                elif i == '3.1':
                    names.append('Alternate Phrases/Underlined')
                    numbers.append(j)
                elif i == '3.2':
                    names.append('Alternate words/Fill in the blanks')
                    numbers.append(j)
                elif i == '4.1':
                    names.append('Re-Arrangement')
                    numbers.append(j)
                elif i == '5.1':
                    names.append('Spelling')
                    numbers.append(j)
                elif i == '6.1':
                    names.append('Substitution')
                    numbers.append(j)
                elif i == '7.1':
                    names.append('Random')
                    numbers.append(j)
                elif i == '8.1':
                    names.append('Spot the Error')
                    numbers.append(j)
                elif i == '9.1':
                    names.append('Passage')
                    numbers.append(j)
            changed = list(zip(names,numbers))
            return changed
        if subject == 'General-Intelligence':
            for i,j in arr:
                if i == '1.1':
                    names.append('Paper cutting and Folding')
                    numbers.append(j)
                elif i == '1.2':
                    names.append('Mirror and Water Image')
                    numbers.append(j)
                elif i == '1.3':
                    names.append('Embedded Figures')
                    numbers.append(j)
                elif i == '1.4':
                    names.append('Figure Completion')
                    numbers.append(j)
                elif i == '1.5':
                    names.append('Counting of embedded figures')
                    numbers.append(j)
                elif i == '1.6':
                    names.append('Counting of figures')
                    numbers.append(j)
                elif i == '2.1':
                    names.append('Analogous pair')
                    numbers.append(j)
                elif i == '2.2':
                    names.append('Multiple Analogy')
                    numbers.append(j)
                elif i == '2.3':
                    names.append('Choosing the analogous pair')
                    numbers.append(j)
                elif i == '2.4':
                    names.append('Number analogy (series pattern)')
                    numbers.append(j)
                elif i =='2.5':
                    names.append('Number analogy (missing)')
                    numbers.append(j)
                elif i == '2.6':
                    names.append('Alphabet based analogy')
                    numbers.append(j)
                elif i == '2.7':
                    names.append('Mixed analogy')
                    numbers.append(j)
                elif i == '3.1':
                    names.append('Series Completion (Diagram)')
                    numbers.append(j)
                elif i == '3.2':
                    names.append('Analogy (Diagram)')
                    numbers.append(j)
                elif i == '3.3':
                    names.append('Classification (Diagram)')
                    numbers.append(j)
                elif i == '3.4':
                    names.append('Dice & Boxes')
                    numbers.append(j)
                elif i == '2.8':
                    names.append('Ruled based analogy')
                    numbers.append(j)
                elif i == '2.9':
                    names.append('Alphabet series (missing)')
                    numbers.append(j)
                elif i == '4.1':
                    names.append('Age')
                    numbers.append(j)
                elif i == '5.1':
                    names.append('Matrix')
                    numbers.append(j)
                elif i == '6.1':
                    names.append('Word Creation')
                    numbers.append(j)
                elif i == '7.1':
                    names.append('Odd one out')
                    numbers.append(j)
                elif i == '8.1':
                    names.append('Height')
                    numbers.append(j)
                elif i == '9.1':
                    names.append('Direction')
                    numbers.append(j)
                elif i =='10.1':
                    names.append('Statement & Conclusion')
                    numbers.append(j)
                elif i == '11.1':
                    names.append('Venn Diagram')
                    numbers.append(j)
                elif i == '12.1':
                    names.append('Missing number')
                    numbers.append(j)
                elif i == '13.1':
                    names.append('Logical Sequence of words')
                    numbers.append(j)
                elif i == '14.1':
                    names.append('Clock/Time')
                    numbers.append(j)
                elif i == '15.1':
                    names.append('Mathematical Operations')
                    numbers.append(j)
                elif i == '16.1':
                    names.append('Coding Decoding')
                    numbers.append(j)
                elif i == '17.1':
                    names.append('Series Test')
                    numbers.append(j)







            changed = list(zip(names,numbers))
            return changed
        if subject == 'Quantitative-Analysis':
            for i,j in arr:
                if i == '1.1':
                    names.append('Probability')
                    numbers.append(j)
                elif i == '2.1':
                    names.append('Percentage')
                    numbers.append(j)
                elif i == '3.1':
                    names.append('Pipes & Cisterns')
                    numbers.append(j)
                elif i == '4.1':
                    names.append('Simplification')
                    numbers.append(j)
                elif i == '5.1':
                    names.append('Permutations')
                    numbers.append(j)
                elif i == '6.1':
                    names.append('Simple Interest')
                    numbers.append(j)
                elif i == '7.1':
                    names.append('Partnership')
                    numbers.append(j)
                elif i == '8.1':
                    names.append('Averages')
                    numbers.append(j)
                elif i == '9.1':
                    names.append('Compound Interest')
                    numbers.append(j)
                elif i == '11.1':
                    names.append('Mixture and Alligations')
                    numbers.append(j)
                elif i == '12.1':
                    names.append('LCM & HCF')
                    numbers.append(j)
                elif i == '13.1':
                    names.append('Inequalities')
                    numbers.append(j)
                elif i == '14.1':
                    names.append('Ages')
                    numbers.append(j)
                elif i == '15.1':
                    names.append('Chain Rule')
                    numbers.append(j)
                elif i == '16.1':
                    names.append('Mensuration')
                    numbers.append(j)
                elif i == '17.1':
                    names.append('Ratio & Proportions')
                    numbers.append(j)
                elif i == '18.1':
                    names.append('Time & Distance')
                    numbers.append(j)
                elif i == '19.1':
                    names.append('Time & Work')
                    numbers.append(j)
                elif i == '20.1':
                    names.append('Number Series')
                    numbers.append(j)
                elif i == '21.1':
                    names.append('Number System')
                    numbers.append(i)
                elif i == '22.1':
                    names.append('Quadratic Equation')
                    numbers.append(i)
                elif i == '23.1':
                    names.append('Data Sufficiency')
                    numbers.append(i)
            changed = list(zip(names,numbers))
            return changed
        if subject == 'General-Knowledge':
            for i in arr:
                if i == '1.1':
                    names.append('Inventions & Innovators')
                if i == '2.1':
                    names.append('Bird Sanctuary')
                    numbers.append(i)
                if i == '3.1':
                    names.append('Books & Authors')
                    numbers.append(i)
                if i == '4.1':
                    names.append('Countries, Capitals & Currencies')
                    numbers.append(i)
                if i == '5.1':
                    names.append('Current Affairs')
                    numbers.append(i)
                if i == '6.1':
                    names.append('Economics')
                    numbers.append(i)
                if i == '7.1':
                    names.append('General Science')
                    numbers.append(i)
                if i == '8.1':
                    names.append('Biology')
                    numbers.append(i)
                if i == '9.1':
                    names.append('Chemistry')
                    numbers.append(i)
                if i == '10.1':
                    names.append('Science & Technology')
                    numbers.append(i)
                if i == '11.1':
                    names.append('Physics')
                    numbers.append(i)
                if i == '12.1':
                    names.append('Geography')
                    numbers.append(i)
                if i == '13.1':
                    names.append('National Organizations')
                    numbers.append(i)
                if i == '14.1':
                    names.append('History')
                    numbers.append(i)
                if i == '15.1':
                    names.append('Honors & Awards')
                    numbers.append(i)
                if i == '16.1':
                    names.append('Important Dates')
                    numbers.append(i)
                if i == '17.1':
                    names.append('Indian Agriculture')
                    numbers.append(i)
                if i == '18.1':
                    names.append('Indian Constitution')
                    numbers.append(i)
                if i == '19.1':
                    names.append('Indian Culture')
                    numbers.append(i)
                if i == '20.1':
                    names.append('Indian Museums')
                    numbers.append(i)
                if i == '21.1':
                    names.append('Polity (India)')
                    numbers.append(i)
                if i == '22.1':
                    names.append('Sports')
                    numbers.append(i)
                if i == '23.1':
                    names.append('Superlatives(India)')
                    numbers.append(i)
                if i == '24.1':
                    names.append('Symbols of States (India)')
                    numbers.append(i)
                if i == '25.1':
                    names.append('Tiger Reserve')
                    numbers.append(i)
                if i == '26.1':
                    names.append('UNESCO Word Heritage Sites(India)')
                    numbers.append(i)
                if i == '27.1':
                    names.append('World Organizations')
                    numbers.append(i)
                if i == '28.1':
                    names.append('Polity (World)')
                    numbers.append(i)
            changed = list(zip(names,numbers))

    def change_topicNamesNumber(self,arr,subject):
        numbers = []
        if subject == 'English':
            for i in arr:
                if i == 'Word Meanings':
                    numbers.append('1.1')
                elif i == 'Idiom/Phrase Meaning':
                    numbers.append('1.2')
                elif i == 'Antonyms':
                    numbers.append('2.1')
                elif i == 'Alternate Phrases/Underlined':
                    numbers.append('3.1')
                elif i == 'Alternate words/Fill in the blanks':
                    numbers.append('3.2')
                elif i == 'Re-Arrangement':
                    numbers.append('4.1')
                elif i == 'Spelling':
                    numbers.append('5.1')
                elif i == 'Substitution':
                    numbers.append('6.1')
                elif i == 'Random':
                    numbers.append('7.1')
                elif i == 'Spot the Error':
                    numbers.append('8.1')
                elif i == 'Passage':
                    numbers.append('9.1')
            return numbers
        if subject == 'General-Intelligence':
            for i in arr:
                if i == 'Paper cutting and Folding':
                    numbers.append('1.1')
                elif i == 'Mirror and Water Image':
                    numbers.append('1.2')
                elif i == 'Embedded Figures':
                    numbers.append('1.3')
                elif i == 'Figure Completion':
                    numbers.append('1.4')
                elif i == 'Counting of embedded figures':
                    numbers.append('1.5')
                elif i == 'Counting of figures':
                    numbers.append('1.6')
                elif i == 'Analogous pair':
                    numbers.append('2.1')
                elif i == 'Multiple Analogy':
                    numbers.append('2.2')
                elif i == 'Choosing the analogous pair':
                    numbers.append('2.3')
                elif i == 'Number analogy (series pattern)':
                    numbers.append('2.4')
                elif i =='Number analogy (missing)':
                    numbers.append('2.5')
                elif i == 'Alphabet based analogy':
                    numbers.append('2.6')
                elif i == 'Mixed analogy':
                    numbers.append('2.7')
                elif i == 'Series Completion (Diagram)':
                    numbers.append('3.1')
                elif i == 'Analogy (Diagram)':
                    numbers.append('3.2')
                elif i == 'Classification (Diagram)':
                    numbers.append('3.3')
                elif i == 'Dice & Boxes':
                    numbers.append('3.4')
                elif i == 'Ruled based analogy':
                    numbers.append('2.8')
                elif i == 'Alphabet series (missing)':
                    numbers.append('2.9')
                elif i == 'Age':
                    numbers.append('4.1')
                elif i == 'Matrix':
                    numbers.append('5.1')
                elif i == 'Word Creation':
                    numbers.append('6.1')
                elif i == 'Odd one out':
                    numbers.append('7.1')
                elif i == 'Height':
                    numbers.append('8.1')
                elif i == 'Direction':
                    numbers.append('9.1')
                elif i =='Statement & Conclusion':
                    numbers.append('10.1')
                elif i == 'Venn Diagram':
                    numbers.append('11.1')
                elif i == 'Missing number':
                    numbers.append('12.1')
                elif i == 'Logical Sequence of words':
                    numbers.append('13.1')
                elif i == 'Clock/Time':
                    numbers.append('14.1')
                elif i == 'Mathematical Operations':
                    numbers.append('15.1')
                elif i == 'Coding Decoding':
                    numbers.append('16.1')
                elif i == 'Series Test':
                    numbers.append('17.1')










            return numbers
        if subject == 'Quantitative-Analysis':
            for i in arr:
                if i == 'Probability':
                    numbers.append('1.1')
                elif i == 'Percentage':
                    numbers.append('2.1')
                elif i == 'Pipes & Cisterns':
                    numbers.append('3.1')
                elif i == 'Simplification':
                    numbers.append('4.1')
                elif i == 'Permutations':
                    numbers.append('5.1')
                elif i == 'Simple Interest':
                    numbers.append('6.1')
                elif i == 'Partnership':
                    numbers.append('7.1')
                elif i == 'Averages':
                    numbers.append('8.1')
                elif i == 'Compound Interest':
                    numbers.append('9.1')
                elif i == 'Mixture and Alligations':
                    numbers.append('11.1')
                elif i == 'LCM & HCF':
                    numbers.append('12.1')
                elif i == 'Inequalities':
                    numbers.append('13.1')
                elif i == 'Ages':
                    numbers.append('14.1')
                elif i == 'Chain Rule':
                    numbers.append('15.1')
                elif i == 'Mensuration':
                    numbers.append('16.1')
                elif i == 'Ratio & Proportions':
                    numbers.append('17.1')
                elif i == 'Time & Distance':
                    numbers.append('18.1')
                elif i == 'Time & Work':
                    numbers.append('19.1')
                elif i == 'Number Series':
                    numbers.append('20.1')
                elif i == 'Number System':
                    numbers.append('21.1')
                elif i == 'Quadratic Equations':
                    numbers.append('22.1')
                elif i == 'Data Sufficiency':
                    numbers.append('23.1')
            return numbers
        if subject == 'General-Knowledge':
            for i in arr:
                if i == 'Inventions & Innovators':
                    numbers.append('1.1')
                if i == 'Bird Sanctuary':
                    numbers.append('2.1')
                if i == 'Books & Authors':
                    numbers.append('3.1')
                if i == 'Countries, Capitals & Currencies':
                    numbers.append('4.1')
                if i == 'Current Affairs':
                    numbers.append('5.1')
                if i == 'Economics':
                    numbers.append('6.1')
                if i == 'General Science':
                    numbers.append('7.1')
                if i == 'Biology':
                    numbers.append('8.1')
                if i == 'Chemistry':
                    numbers.append('9.1')
                if i == 'Science & Technology':
                    numbers.append('10.1')
                if i == 'Physics':
                    numbers.append('11.1')
                if i == 'Geography':
                    numbers.append('12.1')
                if i == 'National Organizations':
                    numbers.append('13.1')
                if i == 'History':
                    numbers.append('14.1')
                if i == 'Honors & Awards':
                    numbers.append('15.1')
                if i == 'Important Dates':
                    numbers.append('16.1')
                if i == 'Indian Agriculture':
                    numbers.append('17.1')
                if i == 'Indian Constitution':
                    numbers.append('18.1')
                if i == 'Indian Culture':
                    numbers.append('19.1')
                if i == 'Indian Museums':
                    numbers.append('20.1')
                if i == 'Polity (India)':
                    numbers.append('21.1')
                if i == 'Sports':
                    numbers.append('22.1')
                if i == 'Superlatives(India)':
                    numbers.append('23.1')
                if i == 'Symbols of States (India)':
                    numbers.append('24.1')
                if i == 'Tiger Reserve':
                    numbers.append('25.1')
                if i == 'UNESCO Word Heritage Sites(India)':
                    numbers.append('26.1')
                if i == 'World Organizations':
                    numbers.append('27.1')
                if i == 'Polity (World)':
                    numbers.append('28.1')
            return numbers



def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    #pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")),result)
    pdf =\
    pisa.pisaDocument(BytesIO(html.encode("utf-8-sig")),result,encoding='utf-8')
    if not pdf.err:
        return  HttpResponse(result.getvalue(),content_type='application/pdf')
    return None



def visible_tests(test_id):
    test = SSCKlassTest.objects.get(id = test_id)
    test_date = test.due_date
    print(test_date)
    today_date = datetime.now().date()
    print(today_date)
    if test_date == today_date:
        return test

    else:
        return test














