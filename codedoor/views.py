from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Profile, Company, Question, Application

def create_question(request):
    if request.method == 'POST':
        try:
            question = request.POST['question']
            comp_answer = request.POST['company answer']
            app_answer = request.POST['applicant answer']
        except Exception as e:
            return HttpResponse("You did not fill out the form correctly")

        q = Question(application=Application.objects.get(pk=1), question=question, applicant_answer=app_answer, actual_answer=comp_answer)
        q.save()
        return redirect("codedoor:view_question", pk=q.id)
    else:
        return render(request, 'codedoor/createQuestion.html')

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

def createprofile(request):
    if request.method == "GET":
        return render(request, 'codedoor/createprofile.html')
    else:
        try:
            input_name = request.POST['name']
            # input_profile_pic = request.POST['profile_pic']
            input_graduation_year = request.POST['graduation_year']
            input_current_job = request.POST['current_job']
            input_linkedin = request.POST['linkedin']
            if "http://" not in input_linkedin and "https://" not in input_linkedin:
                input_linkedin = "http://" + input_linkedin
        except Exception as e:
            return HttpResponse("You did not fill out the form correctly!") # TODO: message displayed on form

        # input_resume = request.POST['resume']
        profile = Profile(name=input_name,
                          graduation_year=input_graduation_year, current_job=input_current_job,
                          linkedin=input_linkedin)
        profile.save()
        return redirect("codedoor:viewprofile", pk=profile.id)


def viewprofile(request, pk):
    profile = get_object_or_404(Profile, id=pk)
    return render(request, 'codedoor/viewprofile.html', {"profile": profile})


def editprofile(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    if request.method == "GET":
        return render(request, 'codedoor/editprofile.html', {"profile": profile})
    else:
        try:
            profile.name = request.POST['name']
            # input_profile_pic = request.POST['profile_pic']
            profile.graduation_year = request.POST['graduation_year']
            profile.current_job = request.POST['current_job']
            print(profile.current_job)
            input_linkedin = request.POST['linkedin']
            if "http://" not in input_linkedin and "https://" not in input_linkedin:
                input_linkedin = "http://" + input_linkedin
            profile.linkedin = input_linkedin
        except Exception as e:
            return HttpResponse("You did not fill out the form correctly!")

        # input_resume = request.POST['resume']
        profile.save()
        return redirect("codedoor:viewprofile", pk=pk)

def create_company(request):
    if request.method == "POST":
        try:
            name = request.POST["name"]
            industry = request.POST["industry"]
            website = request.POST["website"]
            logo = request.FILES["logo"]
            structure = request.POST["structure"]
        except Exception as e:
            return HttpResponse("You did not fill out the form correctly!")

        company = Company(name=name, industry=industry, website=website, logo=logo, structure=structure)
        company.save()

        return redirect('viewcompany/' + str(company.pk))
    else:
        return render(request, "codedoor/createcompany.html")


def view_company(request, pk):
    company = get_object_or_404(Company, pk=pk)
    return render(request, "codedoor/viewcompany.html", {"company": company})


def edit_company(request, pk):
    company = get_object_or_404(Company, pk=pk)
    if request.method == "POST":
        try:
            company.name = request.POST["name"]
            company.industry = request.POST["industry"]
            company.website = request.POST["website"]
            company.structure = request.POST["structure"]
        except Exception as e:
            return HttpResponse("You did not fill out the form correctly!")

        company.save()

        return redirect('/codedoor/viewcompany/' + str(company.pk))

    return render(request, "codedoor/editcompany.html", {"company": company})
