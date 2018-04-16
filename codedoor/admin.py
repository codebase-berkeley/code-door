from django.contrib import admin
from .models import Company, Profile, Application, Review, Question, ReviewComment, ApplicationComment

admin.site.register(Company)
admin.site.register(Profile)
admin.site.register(Application)
admin.site.register(Review)
admin.site.register(Question)
admin.site.register(ReviewComment)
admin.site.register(ApplicationComment)

