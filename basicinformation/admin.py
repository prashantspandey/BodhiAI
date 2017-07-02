from django.contrib import admin
from .models import School,klass,Student,Subject,Teacher

class SubjectInline(admin.StackedInline):
    model = Subject
    extra = 1


class StudentAdmin(admin.ModelAdmin):
    inlines = [SubjectInline]


admin.site.register(Student, StudentAdmin)
admin.site.register(School)
admin.site.register(klass)
admin.site.register(Teacher)
# admin.site.register(Student)
admin.site.register(Subject)
