from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .forms import SignUpForm
from .models import Tweet
import traceback
# Create your views here.


def homepage(request):
    user = request.user
    if user.is_authenticated:
        try:
            user_tweets = Tweet.objects.filter(user=user).order_by('-created_at')
            return render(request, 'tw_section/homepage.html', {'tweets': user_tweets})
        except Exception as e:
            print(traceback.format_exc())
            return render(request, 'tw_section/homepage.html', {'tweets': []})


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
