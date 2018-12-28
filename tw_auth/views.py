from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .forms import SignUpForm
from .models import Tweet
from tw_main.models import Avatar
import traceback


# Create your views here.


def homepage(request):
    user = request.user
    user_pics = Avatar.objects.filter(user=user)
    user_pic = None
    if user_pics.count() > 0:
        user_pic = user_pics[0].document
    if user.is_authenticated:
        try:
            user_tweets = Tweet.objects.filter(user=user).order_by('-created_at')
            return render(request, 'tw_section/homepage.html',
                          {'tweets': user_tweets, 'pic': user_pic})
        except Exception as e:
            print(traceback.format_exc())
            return render(request, 'tw_section/homepage.html',
                          {'tweets': [], 'pic': user_pic})
    else:
        return render(request, 'tw_section/homepage.html',
                      {'tweets': [], 'pic': user_pic})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'tw_auth/signup.html', {'form': form})


def login_view(request):
    if request.method == 'GET':
        return render(request, 'tw_auth/login.html')

    elif request.method == 'POST':
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('home')
