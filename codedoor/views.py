from django.shortcuts import render
from django.http import HttpResponse

from .models import Question
from .models import Application

def hello(request):
    return render(request, 'codedoor/hello.html', {'name': 'Brian'})

def createQPage(request):
    return render(request, 'codedoor/createQuestion.html')

def createQ(request):
    q = None
    if request.method == 'POST':
        question = request.POST['question']
        comp_answer = request.POST['company answer']
        app_answer = request.POST['applicant answer']
        q = Question(application=Application.objects.get(pk=1), question=question, applicant_answer=app_answer, actual_answer=comp_answer)
        q.save()
    return HttpResponse("Congrats! Here's your question: " + q.__str__())

def editQPage(request, pk):
    print("THE PK VALUE IS: " + str(pk))
    q = Question.objects.get(pk=pk)
    question = q.question
    aa = q.applicant_answer
    ca = q.actual_answer
    return render(request, 'codedoor/editQuestion.html', {"question": question, "applicant_answer": aa, "comp_answer": ca, "pk": pk, "link": "/codedoor/editingquestion/" + str(pk)})

def editQ(request, pk):
    # pk = int(pk)
    q = Question.objects.get(pk=pk)
    if request.method == 'POST':
        q.question = request.POST['question']
        q.actual_answer = request.POST['company answer']
        q.applicant_answer = request.POST['applicant answer']
        q.save()
    return HttpResponse("Congrats! Here's your edited question: " + q.__str__())

def viewQ(request, pk):
    q = Question.objects.get(pk=pk)
    return render(request, "codedoor/viewQuestion.html", {"q": q})

def listQ(request):
    questions = Question.objects.order_by("-pk")
    return render(request, 'codedoor/viewQuestions.html', {"questions": questions})