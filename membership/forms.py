from django.contrib.auth.models import User,Group
from django import forms
from django.contrib.auth.forms import UserCreationForm
from basicinformation.models import *

class LoginForm(forms.ModelForm):
    password = forms.CharField(max_length=50, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required= True)


    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'email',
            'password1',
            'password2'
        )
    def save(self,commit = True,*args,**kwargs):
        user = super(RegisterForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.email = self.cleaned_data['email']
        try:
            course = kwargs.get('course')
            print('found course')
        except:
            course = None
            print('couldnot  found course')
        if commit:
            user.save()
            gr = Group.objects.get(name='Students')
            gr.user_set.add(user)
            if course == None:
                print('Indeed i am none')
                school = School.objects.get(name='BodhiAI')
                print('%s-- school' %school)
                cl = klass.objects.get(school__name='BodhiAI')
                print('%s -- class' %cl)
                stu = Student(studentuser=user, klass=cl,
                                  name=user.first_name, school= school)
                stu.save()
                bodhi_teacher = Teacher.objects.get(name = 'BodhiAI')
                submaths = Subject(name='Quantitative-Analysis', student=stu,
                                   teacher = bodhi_teacher)
                subgi = Subject(name='General-Intelligence', student=stu,
                                teacher=bodhi_teacher)
                subenglish = Subject(name='English', student=stu, teacher=
                                     bodhi_teacher)
                subgk = Subject(name='General-Knowledge',
                                student=stu, teacher= bodhi_teacher)
                submaths.save()
                subgi.save()
                subenglish.save()
                subgk.save()
            elif str(course.lower()) == 'jito':
                print('Course is not none')
                print('%s course %s' %(course,type(course)))
                if str(course.lower()) == 'jito':
                    print('this is user save course %s' %course)
                    return user
                else:
                    print('Course is  none')
            elif str(course).lower() == 'siel':
                return user
            else:
                print('Indeed i am none')
                school = School.objects.get(name='BodhiAI')
                print('%s-- school' %school)
                cl = klass.objects.get(school__name='BodhiAI')
                print('%s -- class' %cl)
                stu = Student(studentuser=user, klass=cl,
                                  name=user.first_name, school= school)
                stu.save()
                bodhi_teacher = Teacher.objects.get(name = 'BodhiAI')
                submaths = Subject(name='Quantitative-Analysis', student=stu,
                                   teacher = bodhi_teacher)
                subgi = Subject(name='General-Intelligence', student=stu,
                                teacher=bodhi_teacher)
                subenglish = Subject(name='English', student=stu, teacher=
                                     bodhi_teacher)
                subgk = Subject(name='General-Knowledge',
                                student=stu, teacher= bodhi_teacher)
                submaths.save()
                subgi.save()
                subenglish.save()
                subgk.save()






        return user

class StudentInformationForm(forms.ModelForm):
    #kl = forms.ChoiceField(label='Class',widget=forms.Select())
    class Meta:
        model = StudentCustomProfile
        fields = ['address', 'phone','kl','fatherName','fullName']
        labels = {
                'address':'Address',
                'phone':'Phone',
                'kl': 'Class',
                'fatherName':'Father\'s Name',
                'fullName':'Full Name',
        }

class StudentForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ['phone','code']
        labels = {
                'phone':'Phone',
                'code':'Code',
        }




