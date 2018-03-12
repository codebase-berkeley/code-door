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




