from __future__ import unicode_literals
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .models import Post


def addrc(request):
    if request.method == "POST":
        review = Review.objects.get(pk=request.POST["review"])
        title = request.POST['title']
        content = request.POST['content']
        commenter = Profile.objects.get(user=request.user)
        rc = ReviewComment(review=review, title=title, content=content, commenter=commenter)
        rc.save()

        return JsonResponse({"title": post.title, "body": post.body, "success": True})

    return HttpResponse("yeeha")
