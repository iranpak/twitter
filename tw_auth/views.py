from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from .forms import SignUpForm
from .models import Tweet
import traceback
from .models import Request
from django.utils.timezone import now
from django.contrib.sessions.models import Session
from django.utils import timezone
from django.contrib.auth.models import User


# Create your views here.


def homepage(request):
    user = request.user
    if user.is_authenticated:
        try:
            # print(request.META['REMOTE_ADDR'])
            user_tweets = Tweet.objects.filter(user=user).order_by('-created_at')
            logged_in_users = get_all_logged_in_users()

            # print(logged_in_users)

            # logout(request)
            return render(request, 'tw_section/homepage.html', {'tweets': user_tweets})
        except Exception as e:
            print(traceback.format_exc())
            return render(request, 'tw_section/homepage.html', {'tweets': []})

    else:
        return redirect('login')


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
        if user is not None:
            [s.delete() for s in Session.objects.all() if s.get_decoded().get('_auth_user_id') == user.id]
            login(request, user)
        else:
            ip_address = request.META['REMOTE_ADDR']
            browser = request.META['HTTP_USER_AGENT']
            current_time = now()

            Request.objects.create(ip_addr=ip_address, browser=browser, created_at=current_time, unauthorized=True)

        return redirect('home')


def logout_view(request):
    logout(request)
    return redirect('login')


def get_all_logged_in_users():
    # Query all non-expired sessions
    # use timezone.now() instead of datetime.now() in latest versions of Django
    sessions = Session.objects.filter(expire_date__gte=timezone.now())
    uid_list = []

    # Build a list of user ids from that query
    for session in sessions:
        data = session.get_decoded()
        uid_list.append(data.get('_auth_user_id', None))

    # Query all logged in users based on id list
    logged_in_users = User.objects.filter(id__in=uid_list)
    return logged_in_users
