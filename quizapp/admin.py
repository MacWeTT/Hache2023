from django.contrib import admin
from .models import Profile, Question, inputQuestions, VerifiedEmails

# Register your models here.

admin.site.register(Profile)
admin.site.register(Question)
admin.site.register(inputQuestions)
admin.site.register(VerifiedEmails)
