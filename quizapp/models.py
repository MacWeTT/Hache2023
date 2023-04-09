from django.db import models
from django.contrib.auth.models import User
from PIL import Image
# Create your models here.


class Profile(models.Model):
    # Personal Details
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=300, blank=True)
    avatar = models.ImageField(
        null=True, default="avatar.png", upload_to='user_data')

    def question_count():
        return Question.objects.all().count()

    # Question Information
    question_id = models.IntegerField(verbose_name="Question At", default=1)
    score = models.IntegerField(default=0)
    total_questions = models.IntegerField(
        verbose_name="Total Questions", default=question_count)
    data = models.TextField(default="March 6, 2023 10:00:00")
    correct = models.IntegerField(default=0)
    winner = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)
    lastQuestionTime = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-score']

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.avatar.path)
        if (img.height > 100 or img.width > 100):
            output_size = (100, 100)
            img.thumbnail(output_size)
            img.save(self.avatar.path)


class Question(models.Model):
    question = models.TextField()
    answer = models.CharField(max_length=200, null=True)
    hint = models.CharField(max_length=200, null=True, blank=True)
    asset = models.URLField(
        max_length=500, verbose_name='assets', null=True, blank=True)

    questionNumber = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f'{self.question[:50]}...'


class inputQuestions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    textQuestion = models.CharField(max_length=200)
    textAnswer = models.CharField(max_length=200)
    textTime = models.TimeField(auto_now=True)
    textIP = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f'{self.user} on {self.textTime} answered = {self.textAnswer}'


class VeriedEmails((models.Model)):
    email = models.EmailField(max_length=200)
    is_player = models.BooleanField(default=False)

    def __str__(self):
        return self.email
