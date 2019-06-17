from django.urls import path, reverse
from django.contrib.auth import views as auth_views
from .views import (
    SignUpView, 
    WarsView,
    ClanListView,
    DeleteClanView
)

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('wars/', WarsView.as_view(), name='wars'),
    path('', WarsView.as_view(), name='home'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('clans/', ClanListView.as_view(), name='clan_list'),
    path('clans/<int:pk>/delete', DeleteClanView.as_view(), name='clan_delete'),
]
