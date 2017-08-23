from django.contrib import admin
from .models import *
# Register your models here.

class ChoiceInline(admin.TabularInline):
    model = Choices
    extra = 1

class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]

class SSCQuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
admin.site.register(Questions,QuestionAdmin)
admin.site.register(SSCquestions,SSCQuestionAdmin)
admin.site.register(KlassTest)
admin.site.register(SSCKlassTest)
admin.site.register(OnlineMarks)
admin.site.register(SSCOnlineMarks)
admin.site.register(TemporaryAnswerHolder)
