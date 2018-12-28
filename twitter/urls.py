"""twitter URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from tw_auth import views as auth_views
from django.contrib.auth import login
from tw_main import views as main_views
from api import views as api_views
from django.urls import include

# from tw_auth import views as auth_views

urlpatterns = [
    path('', auth_views.homepage, name='home'),
    path('admin/', admin.site.urls),
    path('signup/', auth_views.signup, name='signup'),
    path('login/', auth_views.login_view, name='login'),
    path('tweet/', main_views.store_tweet, name='tweet'),
    path('api/v1/tweet/tweet/', api_views.store_tweet_api_v1, name='store_tweet_api_v1'),
    path('api/v1/tweet/', api_views.tweet_api_v1, name='tweet_api_v1'),
    path('all_tweets/', main_views.get_all_tweets, name='all_tweets'),
    path('api/v1/login/', api_views.login_v1, name='login_v1'),
    path('logout', api_views.logout_v1, name='logout_v1')
]
