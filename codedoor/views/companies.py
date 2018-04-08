from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from codedoor.models import Company, Review, Profile
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required

@login_required
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

@login_required
def view_company(request, pk):
    company = get_object_or_404(Company, pk=pk)
    profile = get_object_or_404(Profile, pk=request.user.profile.pk)
    reviews = Review.objects.filter(company=company)
    paginator = Paginator(reviews, 5)
    page = request.GET.get('page', 1)
    try:
        review_list = paginator.page(page)
    except PageNotAnInteger:
        review_list = paginator.page(1)
    except EmptyPage:
        review_list = paginator.page(paginator.num_pages)

    return render(request, "codedoor/viewcompany.html", {"company": company, "reviews": review_list, "profile": profile}) 

@login_required
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
