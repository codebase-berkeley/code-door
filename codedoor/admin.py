from django.contrib import admin
from .models import Company, Profile, Application, Review, Question

admin.site.register(Company)
admin.site.register(Profile)
admin.site.register(Application)
admin.site.register(Review)
admin.site.register(Question)

