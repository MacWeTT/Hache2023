from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Profile, inputQuestions, Question
from django.contrib.auth import authenticate, login, logout
from .forms import MyUserCreationForm, UserProfileForm, UserUpdateForm, AnswerForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import HttpResponse
from django.urls import reverse_lazy
from datetime import datetime, timedelta

import random
import time
import pytz


IST = pytz.timezone('Asia/Kolkata')


def Landing(request):
    return render(request, 'landing.html')


def Rules(request):
    return render(request, 'rules.html')


def Hackerboard(request):
    context = {}
    return render(request, 'hackerboard.html', context)


# def is_ajax(request):
#     return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def LoginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User doesn't exist.")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Username or password doesn't exist.")

    context = {'page': page}
    return render(request, 'login.html', context)


def LogoutUser(request):
    logout(request)
    return redirect('home')


def SignUpPage(request):

    if request.method == "POST":
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            login(request, user)
            messages.success(request, "Sign Up completed successfully.")
            return redirect('home')
        else:
            messages.error(
                request, 'An error occured. Check if passwords match.')

    else:
        form = MyUserCreationForm()

    context = {"form": form}
    return render(request, 'signup.html', context)


@login_required(login_url='login')
def HomePage(request):
    return render(request, 'home.html')


def ViewProfile(request, username):
    user = User.objects.get(username=username)
    profile = Profile.objects.get(user=user)
    context = {'profile': profile}
    return render(request, 'profile.html', context)


@login_required(login_url='login')
def EditProfile(request):
    user = request.user
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = UserProfileForm(
            request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('profile', username=user.username)
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = UserProfileForm(instance=request.user.profile)

    context = {'u_form': u_form, 'p_form': p_form}
    return render(request, 'editprofile.html', context)


# Request Messages
requestMessages = [
    'helpme',
    'nhihora',
]

randomMessages = [
    'Think Harder!',
    'Aaj aaj mei hojaega?',
    'Thoda koshish toh karlo bhai',
]


@login_required
def checkForWin(profile):
    if profile.correct == profile.total_questions:
        profile.winner = True
        profile.save()
        return True
    else:
        return False


@login_required
def WinnerView(request):
    winner = request.user.profile.winner
    if winner:
        return render(request, 'winner.html')
    else:
        return redirect('/')


@login_required
def getObj(profile):
    questionObj = Question.objects.get(questionNumber=profile.question_id)
    return questionObj


@login_required(login_url='login')
def QuizView(request):
    profile = request.user.profile
    old_id = profile.question_id

    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            userAnswer = form.cleaned_data.get('answer')
            if userAnswer != None:
                try:
                    inputQuestions.objects.create(
                        user=profile.user,
                        textQuestion=profile.question_id,
                        textAnswer=userAnswer,
                        textIP=request.META.get("REMOTE_ADDR")
                    )
                finally:
                    pass
                if userAnswer.lower() in requestMessages:
                    print("hello")
                    team = [
                        'contact @MacWeTT with screenshot.'
                        'contact @Aman with screenshot.'
                        'contact @Amritansh with screenshot.'
                        'contact @Suvrt with screenshot.'
                    ]
                    data = {'correct': False,
                            'errorM': random.choice(team)}
                    return JsonResponse(data)
                if userAnswer.lower().startswith("flag{") != True:
                    data = {'correct': False,
                            'errorM': "Submit in format Flag{Your_Answer}"}
                    return JsonResponse(data)
                else:
                    correctAnswer = getObj(profile).answer
                    if userAnswer.lower() == correctAnswer.lower():
                        profile.question_id += 1
                        profile.score += 10
                        profile.correct += 1
                        profile.lastQuestionTime = datetime.now(tz=IST)
                        profile.save()
                    winner = checkForWin(profile)
                    if winner:
                        data = {"winner": winner}
                    else:
                        profileObj = getObj(profile)
                        question = {'text': profileObj.question}
                        if (profile.lastQuestionTime != None):
                            print(datetime.now(tz=IST) -
                                  profile.lastQuestionTime)
                        if (profile.question_id == old_id):
                            message = random.choice(randomMessages)
                            data = {'question': question, 'winner': winner,
                                    'correct': False, 'errorM': message}
                        else:
                            data = {'question': question,
                                    'winner': winner, 'correct': True}
                    return JsonResponse(data)
            else:
                data = {'None': 'Galti'}
                return JsonResponse(data)
        else:
            data = {'None': 'Yes'}
            return JsonResponse(data)
    else:
        if checkForWin(profile):
            return redirect(reverse_lazy('winner'))
        form = AnswerForm()
        profileObj = getObj(profile)
        question = {'text': profileObj.question, 'asset': profileObj.asset,
                    'questionNum': profileObj.questionNumber}
        hint = profileObj.hint
        if hint:
            context = {'question': question, 'form': form, 'hint': hint}
            return render(request, 'quiz.html', context)
        else:
            context = {'question': question, 'form': form}
            return render(request, 'quiz.html', context)
