from django.contrib import admin
from .models import Profile, Question, inputQuestions

# Register your models here.

admin.site.register(Profile)
admin.site.register(Question)
admin.site.register(inputQuestions)
