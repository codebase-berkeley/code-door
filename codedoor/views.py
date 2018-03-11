from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from .models import Company
from django.core.files.storage import FileSystemStorage


def create_company(request):
    if request.method == "POST" and request.FILES["logo"]:
        name = request.POST["name"]
        industry = request.POST["industry"]
        website = request.POST["website"]
        myfile = request.FILES["logo"]
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        structure = request.POST["structure"]

        company = Company(name=name, industry=industry, website=website, logo=myfile, structure=structure)
        company.save()

        return redirect('viewcompany/' + str(company.pk))
    else:
        return render(request, "codedoor/createcompany.html")


def view_company(request, pk):
    company = Company.objects.get(pk=pk)
    return render(request, "codedoor/viewcompany.html", {"company": company})


def edit_company(request, pk):
    company = Company.objects.get(pk=pk)
    if request.method == "POST":
        company.name = request.POST["name"]
        company.industry = request.POST["industry"]
        company.website = request.POST["website"]
        myfile = request.FILES["logo"]
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        company.logo = myfile
        # company.logo = request.POST["logo"]
        company.structure = request.POST["structure"]

        company.save()

        return redirect('/codedoor/viewcompany/' + str(company.pk))

    return render(request, "codedoor/editcompany.html", {"company": company})