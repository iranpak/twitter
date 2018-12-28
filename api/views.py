import traceback

from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid
from .models import TokenV1
from tw_auth import models as tw_models


# Create your views here.

def get_user_by_key(request, token_text):
    try:
        cnv = uuid.UUID(token_text).hex
    except:
        return None
    token = TokenV1.objects.filter(authentication_key=cnv).get()
    user = token.user_authentication
    return user


def authenticate_v1(username, password, request):
    user = authenticate(username=username, password=password)
    if user is None:
        return render(request, 'tw_auth/error.html')
    else:
        login(request=request, user=user)
        return


def login_v1(request):
    if request.method == 'GET':
        return render(request, 'tw_auth/login.html')

    else:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        user = authenticate(username=username, password=password)
        if user is None:
            return render(request, 'tw_auth/error.html')
        else:
            token = uuid.uuid4()
            TokenV1.objects.create(user_authentication=user, authentication_key=token)
            # create_auth_token(request, user, True)
            login(request=request, user=user)
            return render(request, 'api/token.html', {'token': token, 'version': 1})


def logout_v1(request):
    TokenV1.objects.filter(user_authentication=request.user).delete()
    logout(request=request)
    return redirect('home')


def store_tweet_api_v1(request):
    token_text = request.POST.get("token_v1", "")
    user = get_user_by_key(request, token_text)
    if request.method == 'POST':
        if user is None:
            return render(request, 'api/404.html', {'version': 1})
        else:
            tweet_text = request.POST.get("tweet", "")
            tw_models.Tweet.objects.create(user=user, body=tweet_text)
            return redirect('tweet_api_v1')
    else:
        try:
            user_tweets = tw_models.Tweet.objects.filter(user=user).order_by('-created_at')
            return render(request, 'api/tweet_api_v1.html', {'tweets': user_tweets})
        except Exception as e:
            print(traceback.format_exc())
            return render(request, 'api/tweet_api_v1.html', {'tweets': []})


def store_tweet_api_v2(request):
    if request.method == 'POST':
        token_text = request.POST.get("token_v2", "")
        user = get_user_by_key(request, token_text)
        if user is None:
            return render(request, 'api/404.html', {'version': 2})
        else:
            tweet_text = request.POST.get("tweet", "")
            tw_models.Tweet.objects.create(user=user, body=tweet_text)
            return redirect('tweet_api_v2')
    else:
        user = request.user
        if user.is_authenticated:
            try:
                user_tweets = tw_models.Tweet.objects.filter(user=user).order_by('-created_at')
                return render(request, 'api/tweet_api_v2.html', {'tweets': user_tweets})
            except Exception as e:
                print(traceback.format_exc())
                return render(request, 'api/tweet_api_v2.html', {'tweets': []})
        else:
            return render(request, 'api/tweet_api_v2.html', {'tweets': []})


def tweet_api_v1(request):
    user = request.user
    if user.is_authenticated:
        try:
            user_tweets = tw_models.Tweet.objects.filter(user=user).order_by('-created_at')
            return render(request, 'api/tweet_api_v1.html', {'tweets': user_tweets})
        except Exception as e:
            print(traceback.format_exc())
            return render(request, 'api/tweet_api_v1.html', {'tweets': []})
    else:
        return render(request, 'api/tweet_api_v1.html', {'tweets': []})


def tweet_api_v2(request):
    user = request.user
    if user.is_authenticated:
        try:
            user_tweets = tw_models.Tweet.objects.filter(user=user).order_by('-created_at')
            return render(request, 'api/tweet_api_v2.html', {'tweets': user_tweets})
        except Exception as e:
            print(traceback.format_exc())
            return render(request, 'api/tweet_api_v2.html', {'tweets': []})
    else:
        return render(request, 'api/tweet_api_v2.html', {'tweets': []})


def get_token_v2(request):
    user = request.user
    if user is None:
        return render(request, 'tw_auth/error.html')
    else:
        token = uuid.uuid4()
        TokenV1.objects.filter(user_authentication=user).delete()
        TokenV1.objects.create(user_authentication=user, authentication_key=token)
        return render(request, 'api/token.html', {'token': token, 'version': 2})


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
    elif not created:
        Token.objects.update(user=instance)
