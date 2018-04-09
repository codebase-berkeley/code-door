from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from codedoor.models import Question, Application

def create_question(request, pk):
    if request.method == 'POST':
        try:
            question = request.POST['question']
            comp_answer = request.POST['company answer']
            app_answer = request.POST['applicant answer']
        except Exception as e:
            return HttpResponse("You did not fill out the form correctly")

        q = Question(application=Application.objects.get(pk=pk), question=question, applicant_answer=app_answer, actual_answer=comp_answer)
        q.save()
        return redirect("codedoor:view_application", pk=pk)
    else:
        return render(request, 'codedoor/createQuestion.html', {"pk": pk})

def edit_question(request, pk):
    q = get_object_or_404(Question, pk=pk)
    if request.method == 'POST':
        try:
            q.question = request.POST['question']
            q.actual_answer = request.POST['company answer']
            q.applicant_answer = request.POST['applicant answer']
        except Exception as e:
            return HttpResponse("You did not fill out the form correctly")
        q.save()
        return redirect("codedoor:view_question", pk=q.id)
    else:
        return render(request, 'codedoor/editQuestion.html',
                      {
                          "question": q.question,
                          "applicant_answer": q.applicant_answer,
                          "comp_answer": q.actual_answer,
                          "pk": pk,
                          "link": "/codedoor/editingquestion/" + str(pk)
                      })

def view_question(request, pk):
    q = get_object_or_404(Question, pk=pk)
    return render(request, "codedoor/viewQuestion.html", {"q": q})

def list_questions(request):
    questions = Question.objects.order_by("-pk")
    return render(request, 'codedoor/viewQuestions.html', {"questions": questions})
