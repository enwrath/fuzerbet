from django.urls import path
from django.conf.urls import url, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    url(r'^accounts/', include('allauth.urls')),
    path('winnerBet', views.winnerBet, name='winnerBet'),
    path('userUpdate', views.userUpdate, name='userUpdate'),
    path('stream', views.streamView, name='streamView'),
    path('stream2', views.streamView2, name='streamView2'),
    path('streamUpdate', views.streamUpdate, name='streamUpdate'),
    path('ranking', views.ranking, name='ranking'),
    path('rankingUpdate', views.rankingUpdate, name='rankingUpdate'),
    path('resetUser', views.resetUser, name='resetUser'),
]
