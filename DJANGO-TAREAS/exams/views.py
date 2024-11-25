from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Exam, Question, Answer
from django.db.models import Q
from .forms import *
import json
from django.http import Http404, HttpResponse, HttpResponseBadRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from django.core import signing
import qrcode # type: ignore
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import base64

@login_required
def exams(request):

    if request.method == 'GET':
        
        exams = Exam.objects.filter(Q(creator=request.user) | Q(collaborators=request.user)).order_by('created_on').distinct()
        return render(request, 'exams.html',{
            'exams': exams
        })

@login_required
def exam_details(request, exam_id):
    exam = get_object_or_404(Exam, pk=exam_id)
    questions = exam.questions.all()

    if request.user == exam.creator or request.user in exam.collaborators.all():
        return render(request, 'exam_details.html',{
            'exam': exam,
            'questions': questions
        })
    else:
        raise Http404("You don't have permission to view this exam")

@login_required
def question_details(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    answers = question.answers.all()

    return render(request, 'question_details.html',{
        'question': question,
        'answers': answers
    })

def share_exam(request):
    return render(request, 'share_exam.html')

def manage_permits(request):
    return render(request, 'manage_permits.html')

def add_question(request, exam_id):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.exam = Exam.objects.get(pk=exam_id)
            question.added_by = request.user
            question.save()
            return redirect(reverse('exam_details', args=[exam_id]))
    else:
        form = QuestionForm()
    return render(request, 'add_question.html', {'form': form})

def create_exam(request):
    return render(request, 'create_exam.html')
