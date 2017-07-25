from django.contrib import admin
from .models import Questions, Choices , KlassTest
# Register your models here.

class ChoiceInline(admin.TabularInline):
    model = Choices
    extra = 1

class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]

admin.site.register(Questions,QuestionAdmin)
admin.site.register(KlassTest)
