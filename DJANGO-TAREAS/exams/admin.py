from django.contrib import admin
from .models import Exam, ExamPermits, Question, Answer

class ExamsAdmin(admin.ModelAdmin):
    readonly_fields = ("created_on",)

class ExamPermitsAdmin(admin.ModelAdmin):
    readonly_fields = ("date_added",)

class QuestionAdmin(admin.ModelAdmin):
    readonly_fields = ("added_on",)

class AnswerAdmin(admin.ModelAdmin):
    # No readonly fields specified for Answer model
    pass

admin.site.register(Exam, ExamsAdmin)
admin.site.register(ExamPermits, ExamPermitsAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)