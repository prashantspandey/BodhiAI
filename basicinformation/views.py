from django.shortcuts import render, HttpResponseRedirect, reverse, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from .models import Student, Teacher, Subject, School, klass
from django.utils import timezone
from .marksprediction import hindi_3testhyprediction, english_3testhyprediction, science_3testhyprediction, \
    maths_3testhyprediction, predictionConvertion


def home(request):
    user = request.user

    if user.is_authenticated:

        if user.groups.filter(name='Students').exists():
            profile = user.student
            subjects = user.student.subject_set.all()

            # retrieve predicted marks from database
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

            context = {'profile': profile, 'subjects': subjects, 'hindihy_prediction': predicted_hindihy,
                       'mathshy_prediction': predicted_mathshy, 'englishhy_prediction': predicted_englishhy,
                       'sciencehy_prediction': predicted_sciencehy}
            return render(request, 'basicinformation/student.html', context)


        elif user.groups.filter(name='Teachers').exists():
            profile = user.teacher

            subject = profile.subject_set.all()
            allstudents = []
            for i in subject:
                allstudents.append(i)
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


# def readmarks(request):
#     user = request.user
#     profile = user.student
#     subjects = user.student.subject_set.all()
#     mathst1, mathst2, mathst3, mathshy, mathst4 = [], [], [], [], [],
#     hindit1, hindit2, hindit3, hindihy, hindit4 = [], [], [], [], [],
#     englisht1, englisht2, englisht3, englishhy, englisht4 = [], [], [], [], [],
#     sciencet1, sciencet2, sciencet3, sciencehy, sciencet4 = [], [], [], [], [],
#
#     for i in subjects:
#         if i.name == 'Maths':
#             mathst1.append(i.test1)
#             mathst2.append(i.test2)
#             mathst3.append(i.test3)
#             mathshy.append(i.hy)
#             mathst4.append(i.test4)
#         elif i.name == 'Hindi':
#             hindit1.append(i.test1)
#             hindit2.append(i.test2)
#             hindit3.append(i.test3)
#             hindihy.append(i.hy)
#             hindit4.append(i.test4)
#         elif i.name == 'English':
#             englisht1.append(i.test1)
#             englisht2.append(i.test2)
#             englisht3.append(i.test3)
#             englishhy.append(i.hy)
#             englisht4.append(i.test4)
#         elif i.name == 'Science':
#             sciencet1.append(i.test1)
#             sciencet2.append(i.test2)
#             sciencet3.append(i.test3)
#             sciencehy.append(i.hy)
#             sciencet4.append(i.test4)
#
#     return mathst1, mathst2, mathst3, mathshy, mathst4 \
#         , hindit1, hindit2, hindit3, hindihy, hindit4, \
#            englisht1, englisht2, englisht3, englishhy, englisht4, \
#            sciencet1, sciencet2, sciencet3, sciencehy, sciencet4
