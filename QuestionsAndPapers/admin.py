from django.contrib import admin
from .models import *
# Register your models here.

class ChoiceInline(admin.TabularInline):
    model = Choices
    extra = 1

class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]

class SscQuestInline(admin.TabularInline):
    model = SSCansweredQuestion
    extra = 1

class SSCOnlineMarksAdmin(admin.ModelAdmin):
    inlines = [SscQuestInline]

class SSCQuestionAdmin(admin.ModelAdmin):
    list_display= ["text","section_category","topic_category"]
    list_filter = ["section_category","topic_category"]
    readonly_fields = ('dateInserted',)
    inlines = [ChoiceInline]

class SSCcomprehensionQuestions(admin.StackedInline):
    model = SSCquestions

class SSCComprehensionAdmin(admin.ModelAdmin):
    inlines = [SSCcomprehensionQuestions]

admin.site.register(Questions,QuestionAdmin)
admin.site.register(SSCquestions,SSCQuestionAdmin)
#admin.site.register(SSCOnlineMarks,SSCOnlineMarksAdmin)
admin.site.register(SSCOnlineMarks)
admin.site.register(Comprehension,SSCComprehensionAdmin)
admin.site.register(KlassTest)
admin.site.register(SSCKlassTest)
admin.site.register(OnlineMarks)
#admin.site.register(Comprehension)
admin.site.register(TemporaryAnswerHolder)
admin.site.register(TemporaryOneClickTestHolder)
admin.site.register(SSCansweredQuestion)
admin.site.register(SSCOfflineMarks)
admin.site.register(TimesUsed)
admin.site.register(TimesReported)
admin.site.register(SscTeacherTestResultLoader)
