from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
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
        return JsonResponse({"name": company.name, "industry": company.industry, "website": company.website, "structure": structure,  "success": True, "logo": company.logo})
    else:
        return HttpResponse("failed to create a company!")


@login_required
def view_company(request, pk, database):
    company = get_object_or_404(Company, pk=pk)
    profile = get_object_or_404(Profile, pk=request.user.profile.pk)

    if request.method == "GET":
        page = request.GET.get('page', 1)
        if database == "reviews":
            reviews = Review.objects.filter(company=company)
            rating = request.GET.get('rating')
            recommend = request.GET.get('recommend')
            if rating and rating != 'None':
                reviews = reviews.filter(rating=rating)
            if recommend and recommend !='None':
                reviews = reviews.filter(recommend=recommend)
            review_comments = []
            for review in reviews:
                review_comments += ReviewComment.objects.filter(review=review)
            review_comments = review_comments[:2]

            paginator1 = Paginator(reviews, 5)

            try:
                review_list = paginator1.page(page)
            except PageNotAnInteger:
                review_list = paginator1.page(1)
            except EmptyPage:
                review_list = paginator1.page(paginator1.num_pages)

            return render(request, "codedoor/viewcompany.html", {"company": company, "reviews": review_list, "profile": profile, "review_comments": review_comments})

        elif database == "applications":
            applications = Application.objects.filter(company=company)
            year = request.GET.get('year')
            season = request.GET.get('season')
            received_offer = request.GET.get('received_offer')

            if year and year != 'None':
                applications = applications.filter(year=year)
            if season and season != 'None':
                applications = applications.filter(season=season)
            if received_offer and received_offer != 'None':
                applications = applications.filter(received_offer=received_offer)
            app_comments = []
            for application in applications:
                app_comments += ApplicationComment.objects.filter(application=application)
            app_comments = app_comments[:2]

            paginator2 = Paginator(applications, 5)
            try:
                application_list = paginator2.page(page)
            except PageNotAnInteger:
                application_list = paginator2.page(1)
            except EmptyPage:
                application_list = paginator2.page(paginator2.num_pages)

            return render(request, "codedoor/viewcompany.html", {"company": company, "profile": profile, "applications": application_list, "app_comments": app_comments})

        else:
            HttpResponse("Invalid url")


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
