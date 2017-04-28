from django.shortcuts import render, HttpResponseRedirect, reverse, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from .models import Student, Teacher, Subject, School, klass
from django.utils import timezone
from .marksprediction import hindi_3testhyprediction, english_3testhyprediction, science_3testhyprediction, \
    maths_3testhyprediction, predictionConvertion, get_predicted_marks


def home(request):
    user = request.user

    if user.is_authenticated:

        if user.groups.filter(name='Students').exists():
            profile = user.student
            subjects = user.student.subject_set.all()

            # retrieve all marks from database
            mathst1, mathst2, mathst3, mathshy, mathst4, mathspredhy, \
                hindit1, hindit2, hindit3, hindihy, hindit4, hindipredhy, \
                englisht1, englisht2, englisht3, englishhy, englisht4, englishpredhy, \
                sciencet1, sciencet2, sciencet3, sciencehy, sciencet4, sciencepredhy = readmarks(
                    user)
            hindipredhy = predictionConvertion(hindipredhy)
            mathspredhy = predictionConvertion(mathspredhy)
            englishpredhy = predictionConvertion(englishpredhy)
            sciencepredhy = predictionConvertion(sciencepredhy)

            context = {'profile': profile, 'subjects': subjects,
                       'hindihy_prediction': hindipredhy,
                       'mathshy_prediction': mathspredhy,
                       'englishhy_prediction': englishpredhy,
                       'sciencehy_prediction': sciencepredhy,
                       'maths1': mathst1, 'maths2': mathst2, 'maths3': mathst3,
                       'maths4': mathst4, 'hindi1': hindit1, 'hindi2': hindit2,
                       'hindi3': hindit3, 'hindi4': hindit4, 'english1': englisht1,
                       'english2': englisht2, 'english3': englisht3, 'english4': englisht4,
                       'science1': sciencet1, 'science2': sciencet2, 'science3': sciencet3, 'science4': sciencet4}
            return render(request, 'basicinformation/student.html', context)

        elif user.groups.filter(name='Teachers').exists():
            profile = user.teacher

            subject = profile.subject_set.all()
            allstudents = []
            for i in subject:
                allstudents.append(i)


            for stu in allstudents:
                print(stu.test1)
                print(stu.name)

            context = {'profile': profile, 'allstudents': allstudents}

            return render(request, 'basicinformation/teacher.html', context)
        else:

            return render(request, 'basicinformation/home.html')

    else:
        return HttpResponseRedirect(reverse('membership:login'))


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


def readmarks(user):
    profile = user.student
    subjects = user.student.subject_set.all()
    mathst1, mathst2, mathst3, mathshy, \
        mathst4, mathspredhy = [], [], [], [], [], []
    hindit1, hindit2, hindit3, hindihy, hindit4, \
        hindipredhy = [], [], [], [], [], []
    englisht1, englisht2, englisht3, englishhy, \
        englisht4, englishpredhy = [], [], [], [], [], []
    sciencet1, sciencet2, sciencet3, sciencehy, \
        sciencet4, sciencepredhy = [], [], [], [], [], []

    for i in subjects:
        if i.name == 'Maths':
            mathst1.append(i.test1)
            mathst2.append(i.test2)
            mathst3.append(i.test3)
            mathshy.append(i.hy)
            mathst4.append(i.test4)
            mathspredhy.append(i.predicted_hy)
        elif i.name == 'Hindi':
            hindit1.append(i.test1)
            hindit2.append(i.test2)
            hindit3.append(i.test3)
            hindihy.append(i.hy)
            hindit4.append(i.test4)
            hindipredhy.append(i.predicted_hy)
        elif i.name == 'English':
            englisht1.append(i.test1)
            englisht2.append(i.test2)
            englisht3.append(i.test3)
            englishhy.append(i.hy)
            englisht4.append(i.test4)
            englishpredhy.append(i.predicted_hy)
        elif i.name == 'Science':
            sciencet1.append(i.test1)
            sciencet2.append(i.test2)
            sciencet3.append(i.test3)
            sciencehy.append(i.hy)
            sciencet4.append(i.test4)
            sciencepredhy.append(i.predicted_hy)

    return mathst1, mathst2, mathst3, mathshy, mathst4, mathspredhy, \
        hindit1, hindit2, hindit3, hindihy, hindit4, hindipredhy, \
        englisht1, englisht2, englisht3, englishhy, englisht4, englishpredhy, \
        sciencet1, sciencet2, sciencet3, sciencehy, sciencet4, sciencepredhy
