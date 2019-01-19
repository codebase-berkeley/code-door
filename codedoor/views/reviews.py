from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from codedoor.models import Review, Company, Profile, ReviewComment

@login_required
def view_review(request, pk):
    review = get_object_or_404(Review, pk=pk)
    comments = ReviewComment.objects.filter(review=review)
    return render(request, "codedoor/view_review.html", {"review": review, "comments":comments})

@login_required
def view_company_reviews(request):
    """
    View a list of all recent reviews.
    Slow af atm. FIXME.
    :param request: Django request Object.
    :return: Template response.
    """
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

    return render(request, "codedoor/view_all_reviews.html",
        {"companies": companies, "reviews": review_list})

@login_required
def edit_review(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if request.method == "POST":
        try:
            company = Company.objects.get(pk=request.POST["company"])
            old_rating = review.rating
            new_rating = float(request.POST["rating"])
            # modify company rating
            company.avg_rating = (company.avg_rating*company.num_reviews - old_rating + new_rating)/company.num_reviews
            review.company = company
            review.rating = new_rating
            review.recommend = request.POST["recommend"]
            review.review = request.POST["review"]
            review.title = request.POST["title"]
        except Exception as e:
            return JsonResponse({
                "reviewername": review.reviewer.user.get_full_name(),
                "companypk": review.company.pk,
                "companyname": review.company.name,
                "companylogo": review.company.logo,
                "rating": review.rating,
                "recommend": review.recommend,
                "review": review.review,
                "title": review.title,
                "success": False
            })
        company.save()
        review.save()

        return JsonResponse({
            "reviewername": review.reviewer.user.get_full_name(),
            "companypk": review.company.pk,
            "companyname": review.company.name,
            "companylogo": review.company.logo,
            "rating": review.rating,
            "recommend": review.recommend,
            "review": review.review,
            "title": review.title,
            "success": True
        })
    return HttpResponse("Bad request")


@login_required
def created_review(request):
    if request.method == "POST":
        company = Company.objects.get(pk=request.POST['company'])
        reviewer = Profile.objects.get(user=request.user)
        rating = request.POST["rating"]
        recommend = request.POST["recommend"]
        review = request.POST["review"]
        title = request.POST["title"]
        recommend = recommend in ("True")
        # update company rating
        company.avg_rating = (company.avg_rating * company.num_reviews + float(rating))/(company.num_reviews+1)
        company.num_reviews = company.num_reviews + 1
        company.save()
        review = Review(company=company, reviewer=reviewer, rating=rating, recommend=recommend, review=review, title=title)
        review.save()

        return JsonResponse({
            "reviewername": review.reviewer.user.get_full_name(),
            "companypk": review.company.pk,
            "companyname": review.company.name,
            "companylogo": review.company.logo,
            "rating": review.rating,
            "recommend": review.recommend,
            "review": review.review,
            "title": review.title,
            "success": True
        })
    return HttpResponse("Bad request")

def company_search_suggestion(request, searchstring):
    def companytodict(company):
        return {
            "id": company.id,
            "name": company.name,
        }
    companies = list(Company.objects.filter(name__istartswith=searchstring))[:5]
    response = JsonResponse({"companies": [companytodict(company) for company in companies]})
    print(response)
    return response
