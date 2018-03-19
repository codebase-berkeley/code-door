from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from codedoor.models import Company, Review

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
    reviews = Review.objects.filter(company=company)
    return render(request, "codedoor/viewcompany.html", {"company": company, "reviews": reviews})


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
