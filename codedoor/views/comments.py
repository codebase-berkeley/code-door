from __future__ import unicode_literals
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import render, get_object_or_404
from codedoor.models import ReviewComment, Review, Profile, Application, ApplicationComment
from django.urls import reverse




def addrc(request):
    print("Called")
    if request.method == "POST":
        review = Review.objects.get(pk=request.POST["review"])
        print(review)
        title = request.POST['title']
        content = request.POST['content']
        commenter = Profile.objects.get(user=request.user)
        rc = ReviewComment(review=review, title=title, content=content, commenter=commenter)
        rc.save()

        return JsonResponse({"title": rc.title, "content": rc.content, "profile_url": rc.commenter.profile_pic ,"name": rc.commenter.user.get_full_name(), "success": True})

    return HttpResponse("yeeha")


def addac(request):
    print("Called")
    if request.method == "POST":
        x = request.POST["application"]
        applicatio = Application.objects.get(pk=x)
        print(applicatio.pk)
        title = request.POST['title']
        content = request.POST['content']
        commenter = Profile.objects.get(user=request.user)

        ac = ApplicationComment(application = applicatio, title = title, content=content, commenter=commenter)
        print("did not bugg out yet")
        ac.save()
        print("did not bugg out yet")

        return JsonResponse({"title": ac.title, "content": ac.content, "profile_url": ac.commenter.profile_pic ,"name": ac.commenter.user.get_full_name(), "success": True})

    return HttpResponse("yeeha")
