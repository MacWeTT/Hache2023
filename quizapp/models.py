from django.db import models
from django.contrib.auth.models import User
from PIL import Image
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=300, blank=True)
    avatar = models.ImageField(null=True, default="avatar.png", upload_to='user_data')
    
    def __str__(self):
        return self.user.username
    
    def save(self,*args, **kwargs):
        super(Profile,self).save(*args,**kwargs)
        
        img = Image.open(self.avatar.path)
        if (img.height > 300 or img.width > 300):
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.avatar.path)
    
    
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    next_question = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    
    def get_next_question(self):
        return self.next_question
    
    def is_correct_answer(self, answer):
        return answer == self.correct_answer
