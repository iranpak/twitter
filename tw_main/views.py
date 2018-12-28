from django.shortcuts import render
from django.shortcuts import redirect
from tw_auth.models import Tweet
from api import models
import uuid
# Create your views here.


def store_tweet(request):
    if request.method == 'POST':
        user = request.user
        if user.is_authenticated():
            tweet_text = request.POST.get("tweet", "")
            Tweet.objects.create(user=user, body=tweet_text)

            return redirect('home')


def get_all_tweets(request):
    user = request.user
    if user.is_authenticated:
        tweets = Tweet.objects.all().order_by('-created_at')
        return render(request, 'tw_auth/all_tweets.html', {'tweets': tweets})
