from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from codedoor.models import Review, Company, Profile

#class Review(models.Model):
#    company = models.ForeignKey(Company, on_delete=models.CASCADE)
#    reviewer = models.ForeignKey(Profile, on_delete=models.CASCADE)
#    rating = models.DecimalField(decimal_places=2, max_digits=10)
#    recommend = models.BooleanField()
#    review = models.TextField()
#    title = models.CharField(max_length=200, null=True, blank=True)

#    def __str__(self):
#        return "{}'s review of {}".format(self.reviewer.name,
#                                          self.company.name)

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


def view_review(request, pk):
    review = get_object_or_404(Review, pk=pk)
    return render(request, "codedoor/viewreview.html", {"review": review})


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
