from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from codedoor.models import Review, Company, Profile
from django.contrib.auth.decorators import login_required

#@login_required
def create_review(request):
    if request.method == "POST":
        try:
            company = Company.objects.get(pk=request.POST["company"])
            reviewer = Profile.objects.get(pk=request.POST["reviewer"])
            rating = request.POST["rating"]
            recommend = request.POST["recommend"]
            review = request.POST["review"]
            title = request.POST["title"]
        except Exception as e:
            return HttpResponse("You did not fill out the form correctly!")

        review = Review(company=company, reviewer=reviewer, rating=rating, recommend=recommend, review=review, title=title)
        review.save()

        return redirect('viewreview/' + str(review.pk))
    else:
        companies = Company.objects.all()
        reviewers = Profile.objects.all()
        return render(request, "codedoor/createreview.html", {"companies": companies, "reviewers": reviewers})

#@login_required
def view_review(request, pk):
    review = get_object_or_404(Review, pk=pk)
    return render(request, "codedoor/viewreview.html", {"review": review})

#@login_required
def edit_review(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if request.method == "POST":
        try:
            company = Company.objects.get(pk=request.POST["company"])
            reviewer = Profile.objects.get(pk=request.POST["reviewer"])
            review.company = company
            review.reviewer = reviewer
            review.rating = request.POST["rating"]
            review.recommend = request.POST["recommend"]
            review.review = request.POST["review"]
            review.title = request.POST["title"]
        except Exception as e:
            return HttpResponse("You did not fill out the form correctly!")

        review.save()

        return redirect('/codedoor/viewreview/' + str(review.pk))
    else:
        companies = Company.objects.all()
        reviewers = Profile.objects.all()
        return render(request, "codedoor/editreview.html", {"review": review, "companies": companies, "reviewers": reviewers})
