from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # image = models.ImageField()
    # bio = models
    
    
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    next_question = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    
    def get_next_question(self):
        return self.next_question
    
    def is_correct_answer(self, answer):
        return answer == self.correct_answer
