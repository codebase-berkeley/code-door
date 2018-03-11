from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from .models import Company

def hello(request):
	return render(request, 'codedoor/hello.html', {'name': 'Brian'})

def create_company(request):
	if request.method == "POST":
		name = request.POST["name"]
		industry = request.POST["industry"]
		website = request.POST["website"]
		logo = request.POST["logo"]
		structure = request.POST["structure"]

		company = Company(name=name, industry=industry, website=website, logo=logo, structure=structure)
		company.save()

		return redirect('viewcompany/' + str(company.pk))
	else:
		return render(request, "codedoor/createcompany.html")


def view_company(request, pk):
	company = Company.objects.get(pk=pk)
	return render(request, "codedoor/viewcompany.html", {"company": company})


def edit_company(request, pk):
	return render(request, "codedoor/viewcompany.html", {"company": company})
