from django import forms
from .models import Exam, Question, Answer

class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['name', 'description', 'collaborators']

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['name', 'possible_answers', 'type', 'correct_answer', 'explanation', 'exam']

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['name', 'question', 'content']
