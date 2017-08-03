def create_student(num, request):
    user = request.user

    for i in range(1, num):
        try:
            us = User.objects.create_user(username='student' + str(i),
                                          email='studentss' + str(i) + '@gmail.com',
                                          password='dnpandey')
            us.save()
            gr = Group.objects.get(name='Students')
            gr.user_set.add(us)
            cl = klass.objects.filter(school__name='First School')
            classes = []
            for cc in cl:
                classes.append(cc)
            for k in classes:
                stu = Student(studentuser=us, klass=np.random.choice(classes), rollNumber=int(str(i) + '00'),
                              name='stud' + str(i),
                              dob=timezone.now(), pincode=int(str(405060)))
                stu.save()
                sub = Subject(name='Maths', student=stu, teacher=user.teacher, test1
                =randint(3, 10), test2=randint(3, 9), test3=
                              randint(3, 9))
                sub.save()
        except Exception as e:
            print(str(e))


def create_teacher(num):
    school1 = School.objects.filter(name='Dummy School')
    school2 = School.objects.filter(name='Not Dummy School')
    schools = [school1,school2]
    for i in range(num):
        us = User.objects.create_user(username='teacher' + str(i),
                                      email='teacher' + str(i) + '@gmail.com',
                                      password='dnpandey')
        us.save()
        gr = Group.objects.get(name='Teachers')
        gr.user_set.add(us)

        teache = Teacher(teacheruser=us,
                         experience=randint(1, 20), name=us.username,
                         school=np.random.choice(schools))
        teache.save()
