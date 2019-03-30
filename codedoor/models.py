from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Company(models.Model):
    STRUCTURES = (("Startup", "Startup"),
                  ("Boutique", "Boutique"),
                  ("Small", "Small"),
                  ("Medium", "Medium"),
                  ("Large", "Large"))

    name = models.CharField(max_length=100)
    industry = models.CharField(max_length=100)
    website = models.URLField(null=True, blank=True)
    logo = models.URLField(null=True, blank=True)
    structure = models.CharField(max_length=100, choices=STRUCTURES)
    num_reviews = models.IntegerField(default = 0)
    avg_rating = models.FloatField(default = 0.0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.URLField(null=True, blank=True)
    graduation_year = models.IntegerField()
    current_job = models.CharField(null=True, blank=True, max_length=1000)
    linkedin = models.URLField(null=True, blank=True)
    resume = models.FileField(null=True, blank=True)
    codebucks = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.get_full_name()


class Application(models.Model):
    SEASONS = (('Fall', 'Fall'),
               ('Spring', 'Spring'),
               ('Summer', 'Summer'),
               ('Winter', 'Winter'))

    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    description = models.TextField()
    year = models.IntegerField()
    season = models.CharField(max_length=100, choices=SEASONS)
    position = models.CharField(max_length=500)
    received_offer = models.BooleanField()
    offer_details = models.TextField(null=True, blank=True)
    difficult = models.FloatField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}'s application to {}".format(self.profile.user.get_full_name(),
                                               self.company.name)


class Review(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    reviewer = models.ForeignKey(Profile, on_delete=models.CASCADE)
    rating = models.FloatField()
    recommend = models.BooleanField()
    review = models.TextField()
    title = models.CharField(max_length=200, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}'s review of {}".format(self.reviewer.user,
                                          self.company.name)


class Question(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    question = models.TextField()
    applicant_answer = models.TextField(null=True, blank=True)
    actual_answer = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}: {}".format(self.application.company.name,
                               self.question[0:40])


class ReviewComment(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, null=True, blank=True)
    content = models.TextField()
    commenter = models.ForeignKey(Profile, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} comment on {}".format(self.commenter.user, self.review.title)


class ApplicationComment(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, null=True, blank=True)
    content = models.TextField()
    commenter = models.ForeignKey(Profile, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} comment on {}".format(self.commenter.user, self.application.company.name)
