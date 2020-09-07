from django.urls import path
from django.conf.urls import url, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    url(r'^accounts/', include('allauth.urls')),
    path('winnerBet', views.winnerBet, name='winnerBet'),
    path('userUpdate', views.userUpdate, name='userUpdate'),
]
