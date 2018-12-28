from django.shortcuts import render
from django.shortcuts import redirect
from tw_auth.models import Tweet
from django.core.files.storage import FileSystemStorage
from tw_main.forms import AvatarForm
from .models import Avatar
from api import models
import uuid
# Create your views here.


def store_tweet(request):
    if request.method == 'POST':
        user = request.user
        if user.is_authenticated:
            tweet_text = request.POST.get("tweet", "")
            Tweet.objects.create(user=user, body=tweet_text)

            return redirect('home')
        else:
            return render(request, 'api/404.html', {'version': 1})


def get_all_tweets(request):
    user = request.user
    if user.is_authenticated:
        tweets = Tweet.objects.all().order_by('-created_at')
        return render(request, 'tw_auth/all_tweets.html', {'tweets': tweets})


def upload_avatar(request):
    user = request.user
    if user.is_authenticated:
        if request.method == 'POST':
            avatar_file = request.FILES['avatar_file']
            fs = FileSystemStorage()
            Avatar.objects.create(user=user, document=avatar_file)
            filename = fs.save(avatar_file.name, avatar_file)
            uploaded_file_url = fs.url(filename)
            return redirect('home')
