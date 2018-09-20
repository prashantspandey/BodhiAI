from django.contrib import admin
from .models import *


class TeacherInline(admin.StackedInline):
    model = Teacher
    extra = 1
class StudentInline(admin.StackedInline):
    model = Student
    extra = 1

class SchoolAdmin(admin.ModelAdmin):
    inlines = [TeacherInline]
class KlassAdmin(admin.ModelAdmin):
    inlines = [StudentInline]


admin.site.register(School,SchoolAdmin)
admin.site.register(klass,KlassAdmin)
admin.site.register(Subject)
admin.site.register(Student)
admin.site.register(SchoolManagement)
admin.site.register(InterestedPeople)
admin.site.register(TeacherClasses)
admin.site.register(StudentCustomProfile)
admin.site.register(StudentProfile)
admin.site.register(StudentConfirmation)
admin.site.register(StudentDetails)
admin.site.register(StudentAverageTimingDetailCache)
