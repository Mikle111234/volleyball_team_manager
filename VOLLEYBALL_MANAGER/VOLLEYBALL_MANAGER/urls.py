"""VOLLEYBALL_MANAGER URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from voll_manager.views import (main_page, club_page, groups_page, user_profile_page, user_club_page, develop_page, med_test_page,
                                user_statistics, user_settings_page, sport_test_page, psyho_test_page, login, create_user,
                                change_password)
from voll_manager.views_api import (distribute_players)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', main_page, name='home'),
    url(r'^club$', club_page, name='club'),
    url(r'^groups$', groups_page, name='groups'),
    url(r'^medical-test$', med_test_page, name='medical-test'),
    url(r'^sport-test$', sport_test_page, name='sport-test'),
    url(r'^psyho-test$', psyho_test_page, name='psyho-test'),
    url(r'^user$', user_profile_page, name='user-page'),
    url(r'^user-club$', user_club_page, name='user-club-page'),
    url(r'^user-statistics$', user_statistics, name='user-statistics-page'),
    url(r'^settings$', user_settings_page, name='user-settings-page'),
    url(r'^contacts$', develop_page, name='contacts'),
    url(r'^api/distribute', distribute_players, name='distribute'),
    url(r'^login$', login, name='login'),
    url(r'^create-user$', create_user, name='create_user'),
    url(r'^change-password', change_password, name='change_password'),
]
