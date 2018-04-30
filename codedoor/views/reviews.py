from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from codedoor.models import Review, Company, Profile, ReviewComment
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

@login_required
def create_review(request):
    if request.method == "POST":
        try:
            company = Company.objects.get(pk=request.POST["company"])
            reviewer = Profile.objects.get(user=request.user)
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
        reviewer = request.user
        return render(request, "codedoor/createreview.html", {"companies": companies, "reviewer": reviewer})

@login_required
def create_review_wc(request, pk):
    currentcompany = get_object_or_404(Company, pk=pk)
    if request.method == "POST":
        try:
            print(request.user)
            company = Company.objects.get(pk=request.POST["company"])
            reviewer = Profile.objects.get(user=request.user)
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
        reviewer = request.user
        return render(request, "codedoor/createreviewwc.html", {"companies": companies, "reviewer": reviewer, "currentcompany": currentcompany})

@login_required
def view_review(request, pk):
    review = get_object_or_404(Review, pk=pk)
    comments = ReviewComment.objects.filter(review=review)
    return render(request, "codedoor/viewreview.html", {"review": review, "comments":comments})

@login_required
def view_company_reviews(request):
    reviews = Review.objects.all().order_by('-id')
    companies = Company.objects.all()
    paginator1 = Paginator(reviews, 6)
    page = request.GET.get('page', 1)
    try:
        review_list = paginator1.page(page)
    except PageNotAnInteger:
        review_list = paginator1.page(1)
    except EmptyPage:
        review_list = paginator1.page(paginator1.num_pages)

    return render(request, "codedoor/viewcompanyreviews.html",
        {"companies": companies, "reviews": review_list})

@login_required
def edit_review(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if request.method == "POST":
        try:
            company = Company.objects.get(pk=request.POST["company"])
            review.company = company
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
        return render(request, "codedoor/editreview.html", {"review": review, "companies": companies})


@login_required
def created_review(request):
    if request.method == "POST":
        pk = request.POST['pk']
        company = Company.objects.get(pk=pk)
        reviewer = Profile.objects.get(user=request.user)
        rating = request.POST["rating"]
        recommend = request.POST["recommend"]
        review = request.POST["review"]
        title = request.POST["reviewtitle"]
        recommend = recommend in ("True")
        print(recommend)

        review = Review(company=company, reviewer=reviewer, rating=rating, recommend=recommend, review=review, title=title)
        review.save()
        print("saved a revieww")

        return JsonResponse({"reviewername": review.reviewer.user.get_full_name(), "companypk": review.company.pk, "companyname": review.company.name, "companylogo": review.company.logo, "rating": review.rating, "recommend": review.recommend, "review": review.review, "title": review.title, "success": True})
    return HttpResponse("created a question!")
