from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from codedoor.models import Company, Review, Profile, Application, ReviewComment, ApplicationComment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
import boto3
from api_keys import s3_access_keys

company_logos_bucket = 'codedoor-companies-logos'


@login_required
def create_company(request):
    if request.method == "POST":
        try:
            name = request.POST["name"]
            industry = request.POST["industry"]
            website = request.POST["website"]
            logo = request.FILES["logo"].read()
            structure = request.POST["structure"]
        except Exception as e:
            print(e)
            return HttpResponse("You did not fill out the form correctly!")

        company = Company(name=name, industry=industry, website=website, structure=structure)
        company.save()
        s3 = boto3.resource('s3', aws_access_key_id=s3_access_keys["id"],
                            aws_secret_access_key=s3_access_keys["secret"])
        s3.Bucket(company_logos_bucket).put_object(Key=str(company.id), Body=logo, ACL='public-read')
        url = "https://s3-us-west-1.amazonaws.com/" + company_logos_bucket + "/" + str(company.id)
        company.logo = url
        company.save()
        return JsonResponse({"name": company.name, "industry": company.industry, "website": company.website, "structure": structure,  "success": True, "logo": company.logo, "pk": company.pk})
    else:
        return HttpResponse("failed to create a company!")


@login_required
def view_company(request, pk, database):
    company = get_object_or_404(Company, pk=pk)
    profile = get_object_or_404(Profile, pk=request.user.profile.pk)

    if request.method == "GET":
        reviews = Review.objects.filter(company=company)
        applications = Application.objects.filter(company=company)
        if database == "reviews":
            rating = request.GET.get('rating')
            recommend = request.GET.get('recommend')
            if rating and rating != 'None':
                reviews = reviews.filter(rating=rating)
            if recommend and recommend !='None':
                reviews = reviews.filter(recommend=recommend)
        elif database == "applications":
            year = request.GET.get('year')
            season = request.GET.get('season')
            received_offer = request.GET.get('received_offer')

            if year and year != 'None':
                applications = applications.filter(year=year)
            if season and season != 'None':
                applications = applications.filter(season=season)
            if received_offer and received_offer != 'None':
                applications = applications.filter(received_offer=received_offer)
        else:
            HttpResponse("Invalid url")



    else:
        if database == "reviews":
            if 'rating' in request.POST and 'recommend' in request.POST:
                input_rating = request.POST['rating']
                input_recommend = request.POST['recommend']
                reviews = Review.objects.filter(company=company, rating=input_rating, recommend=input_recommend)
            elif 'rating' in request.POST:
                input_rating = request.POST['rating']
                reviews = Review.objects.filter(company=company, rating=input_rating)
            elif 'recommend' in request.POST:
                input_recommend = request.POST['recommend']
                reviews = Review.objects.filter(company=company, recommend=input_recommend)
            else:
                reviews = Review.objects.filter(company=company)
            applications = Application.objects.filter(company=company)
        elif database == "applications":
            if 'year' in request.POST and 'season' in request.POST and 'received_offer' in request.POST:
                input_year = request.POST['year']
                input_season = request.POST['season']
                input_received_offer = request.POST['received_offer']
                applications = Application.objects.filter(company=company, year=input_year, season=input_season,
                                                          received_offer=input_received_offer)
            elif 'year' in request.POST:
                if 'season' in request.POST:
                    input_year = request.POST['year']
                    input_season = request.POST['season']
                    applications = Application.objects.filter(company=company, year=input_year, season=input_season)
                elif 'received_offer' in request.POST:
                    input_year = request.POST['year']
                    input_received_offer = request.POST['received_offer']
                    applications = Application.objects.filter(company=company, year=input_year,
                                                              received_offer=input_received_offer)
                else:
                    input_year = request.POST['year']
                    applications = Application.objects.filter(company=company, year=input_year)
            elif 'season' in request.POST:
                if 'received_offer' in request.POST:
                    input_season = request.POST['season']
                    input_received_offer = request.POST['received_offer']
                    applications = Application.objects.filter(company=company, season=input_season,
                                                              received_offer=input_received_offer)
                else:
                    input_season = request.POST['season']
                    applications = Application.objects.filter(company=company, season=input_season)
            elif 'received_offer' in request.POST:
                input_received_offer = request.POST['received_offer']
                applications = Application.objects.filter(company=company, received_offer=input_received_offer)
            else:
                applications = Application.objects.filter(company=company)
            reviews = Review.objects.filter(company=company)
        else:
            HttpResponse("Invalid url")

    # Reviews
    reviews = Review.objects.filter(company=company)
    review_comments = []
    for review in reviews:
        review_comments += ReviewComment.objects.filter(review=review)
    review_comments = review_comments[:2]
    # Applications
    applications = Application.objects.filter(company=company)
    app_comments = []
    for application in applications:
        app_comments += ApplicationComment.objects.filter(application=application)
    app_comments = app_comments[:2]

    
    paginator1 = Paginator(reviews, 5)
    paginator2 = Paginator(applications, 5)
    page = request.GET.get('page', 1)
    try:
        review_list = paginator1.page(page)
    except PageNotAnInteger:
        review_list = paginator1.page(1)
    except EmptyPage:
        review_list = paginator1.page(paginator1.num_pages)
    try:
        application_list = paginator2.page(page)
    except PageNotAnInteger:
        application_list = paginator2.page(1)
    except EmptyPage:
        application_list = paginator2.page(paginator2.num_pages)

    return render(request, "codedoor/viewcompany.html", {"company": company, 
        "reviews": review_list, "profile": profile, 
        "applications":application_list, "review_comments": review_comments, 
        "app_comments": app_comments})


@login_required
def edit_company(request, pk):
    company = get_object_or_404(Company, pk=pk)
    type =  ["Startup","Boutique","Small","Medium","Large"]
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

    return render(request, "codedoor/editcompany.html", {"company": company, "type": type })
