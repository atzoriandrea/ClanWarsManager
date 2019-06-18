from django.urls import path, reverse
from django.contrib.auth import views as auth_views
from .views import (
    SignUpView, 
    WarsView,
    ClanListView,
    DeleteClanView,
    MyClan,
    ExitClan,
    RemoveUserFromClan,
    UpdateClanView
)

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('wars/', WarsView.as_view(), name='wars'),
    path('', WarsView.as_view(), name='home'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('clans/', ClanListView.as_view(), name='clan_list'),
    path('clans/<int:pk>', MyClan.as_view(), name='clan'),
    path('clans/delete', DeleteClanView.as_view(), name='clan_delete'),
    path('clans/update', UpdateClanView.as_view(), name='clan_update'),
    path('clans/exit', ExitClan.as_view(), name='exit'),
    path('clans/remove/<str:username>', RemoveUserFromClan.as_view(), name='RemoveUser'),
]
