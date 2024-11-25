from django.db import models
from django.contrib.auth.models import User

class Exam(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_exams')
    created_on = models.DateTimeField(auto_now_add=True)
    collaborators = models.ManyToManyField(User, through='ExamPermits', related_name='collaborated_exams')

    def __str__(self):
        return self.name

class ExamPermits(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('exam', 'user')

    def __str__(self):
        return f"{self.user.username} - {self.exam.name}"

class Question(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    possible_answers = models.CharField(max_length=50)  
    type = models.CharField(max_length=50)
    correct_answer = models.CharField(max_length=50)  
    added_on = models.DateTimeField(auto_now_add=True)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    explanation = models.TextField(blank=True, null=True)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='questions')

    def __str__(self):
        return self.name

class Answer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    content = models.TextField()

    def __str__(self):
        return self.name
