from django.shortcuts import render, HttpResponseRedirect, reverse, redirect
from django.http import Http404, HttpResponse
from django.contrib.auth.models import User, Group
from django.contrib import messages 
from basicinformation.models import Subject,Teacher,Student
from .models import *
from basicinformation.marksprediction import *
from django.utils import timezone
def inbox(request):
    user = request.user
    if user.is_authenticated:
        messages = PrivateMessage.objects.filter(receiver = user)
        context = {'inbox' : messages}
        return render(request,'Private_Messages/all_messages.html',context)
    else:
        raise Http404('Not allowed')
def every_messages(request):
    user = request.user
    if user.is_authenticated:
        if user.groups.filter(name='Students').exists():
            profile = user.student
            sub = profile.subject_set.all()
            my_teachers = []
            for su in sub:
                my_teachers.append(su.teacher)
            my_messages = PrivateMessage.objects.filter(receiver= user)
            count = 0
            for i in my_messages:
                count = count + 1
            context = {'teachers':my_teachers,'count':count,'isTeacher':False}
            return render(request,'Private_Messages/messages.html',context) 
        if user.groups.filter(name='Teachers').exists():
            profile = user.teacher
            sub = profile.subject_set.all()
            my_students = []
            for su in sub:
                my_students.append(su.student)
            my_messages = PrivateMessage.objects.filter(receiver= user)
            count = 0
            for i in my_messages:
                count = count + 1
            context = {'teachers':my_students,'count':count,'isTeacher':True}
            return render(request,'Private_Messages/messages.html',context) 


def send_messages(request):
    user = request.user
    if user.is_authenticated:
        if user.groups.filter(name='Students').exists():
            if 'teacher_name' in request.GET:
                teacher_name = request.GET['teacher_name']
                teacher_id = int(teacher_name)
                s_id = teacher_id
                teacher = Teacher.objects.get(id = teacher_id)
                new_Message = PrivateMessage()
                new_Message.sender = user
                new_Message.receiver = teacher.teacheruser
                context = {'message_info':new_Message,'who':'student','sid':s_id}
                return render(request,'Private_Messages/send_message.html',context)
            if 'receiver' in request.POST and 'subject' in request.POST and 'body'  in  request.POST:
                profile = user.student
                sub = profile.subject_set.all()
                my_teachers = []
                for su in sub:
                    my_teachers.append(su.teacher)
                my_messages = PrivateMessage.objects.filter(receiver= user)
                count = 0
                for i in my_messages:
                    count = count + 1
                subject = request.POST['subject']
                receiver = request.POST['receiver']
                print(receiver)
                body = request.POST['body']
                teacher = Teacher.objects.get(id = int(receiver))
                post_message = PrivateMessage()
                post_message.sender = user
                post_message.receiver = teacher.teacheruser
                post_message.subject = subject
                if body == '':
                    messages.error(request, 'Please fill the Message. ')
                    context ={'messagain':teacher,'teachers':my_teachers,
                              'count':count}
                    return render(request,'Private_Messages/messages.html',context)
                else:
                    post_message.body = body
                    post_message.save()
                    context = {'mess':post_message,'created':True}
                    return render(request,'Private_Messages/send_message.html',context)
        if user.groups.filter(name='Teachers').exists():
            if 'teacher_name' in request.GET:
                student_id = request.GET['teacher_name']
                s_id = int(student_id)
                student = Student.objects.get(id = int(student_id))
                new_Message = PrivateMessage()
                new_Message.sender = user
                new_Message.receiver = student.studentuser
                
                context = {'message_info':new_Message,'sid':s_id,
                           }
                return render(request,'Private_Messages/send_message.html',context)
            if 'receiver' in request.POST and 'subject' in request.POST and 'body'  in  request.POST:
                profile = user.teacher
                sub = profile.subject_set.all()
                my_students = []
                for su in sub:
                    my_students.append(su.student)
                my_messages = PrivateMessage.objects.filter(receiver= user)
                count = 0
                for i in my_messages:
                    count = count + 1
                subject = request.POST['subject']
                receiver = request.POST['receiver']
                body = request.POST['body']
                student = Student.objects.get(id = receiver)
                post_message = PrivateMessage()
                post_message.sender = user
                post_message.receiver = student.studentuser
                post_message.subject = subject
                if body == '':
                    messages.error(request, "Message Body can't be empty")
                    context = {'messagain':student,'teachers':my_students,'count':count}
                    return render(request,'Private_Messages/messages.html',context)
                else:
                    post_message.body = body
                    post_message.save()
                    context = {'mess':post_message,'created':True}
                    return render(request,'Private_Messages/send_message.html',context)

def view_sent_messages(request):
    user = request.user
    if user.is_authenticated:
        sent_messages = PrivateMessage.objects.filter(sender = user)
        context = {'sent_messages':sent_messages}
        return render(request,'Private_Messages/sent_messages.html',context)
    else:
        raise Http404('Please login to see messages')


# functions for Announcement

def home_announcement(request):
    user = request.user
    if user.is_authenticated:
        if user.groups.filter(name='Teachers').exists():
            me = Teach(user)
            klasses = me.my_classes_names()
            annoucements = Announcement.objects.filter(announcer =
                                                       user.teacher)
            context = {'klasses':klasses,'announcements':annoucements}
            return \
        render(request,'Private_Messages/create_announcement.html',context)
        else:
            raise Http404('Wrong page kid')

def create_annoucement(request):
    user = request.user
    if user.is_authenticated:
        if request.POST:
            kla = request.POST['which_class']
            text = request.POST['announcement']
            print(klass)
            print(text)
            print(user.teacher)
            newAnnouncement = Announcement()
            newAnnouncement.announcer = user.teacher
            newAnnouncement.text = text
            newAnnouncement.date = timezone.now()
            newAnnouncement.save()
            kl = klass.objects.get(name = kla, school =
                                   user.teacher.school)
            students = Student.objects.filter(klass = kl)
            for st in students:
                newAnnouncement.listener.add(st)
            context = {'announcement':newAnnouncement}
            return render(request,'Private_Messages/success_announced.html',context)


















