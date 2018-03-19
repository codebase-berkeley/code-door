from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from codedoor.models import Company

def create_review(request):
    if request.method == "POST":
        try:
            name = request.POST["name"]
            industry = request.POST["industry"]
            website = request.POST["website"]
            logo = request.FILES["logo"]
            structure = request.POST["structure"]
        except Exception as e:
            return HttpResponse("You did not fill out the form correctly!")

        review = Company(name=name, industry=industry, website=website, logo=logo, structure=structure)
        review.save()

        return redirect('viewreview/' + str(review.pk))
    else:
        return render(request, "codedoor/createreview.html")


def view_review(request, pk):
    review = get_object_or_404(Company, pk=pk)
    return render(request, "codedoor/viewreview.html", {"review": review})


def edit_review(request, pk):
    review = get_object_or_404(Company, pk=pk)
    if request.method == "POST":
        try:
            review.name = request.POST["name"]
            review.industry = request.POST["industry"]
            review.website = request.POST["website"]
            review.structure = request.POST["structure"]
        except Exception as e:
            return HttpResponse("You did not fill out the form correctly!")

        review.save()

        return redirect('/codedoor/viewreview/' + str(review.pk))

    return render(request, "codedoor/editreview.html", {"review": review})
