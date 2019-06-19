from django.urls import path, reverse
from django.contrib.auth import views as auth_views
from .views import (
    SignUpView, 
    WarListView,
    ClanListView,
    ClanDeleteView,
    ClanDetailView,
    ClanLeaveView,
    ClanRemoveView,
    ClanUpdateView,
    ClanJoinView,
    CreateWar,
    WarDetailView,
    WarDeleteView,
)

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('wars/', WarListView.as_view(), name='wars'),
    path('wars/<int:pk>', WarDetailView.as_view(), name='war_details'),
    path('clans/fight/<int:pk>', CreateWar.as_view(), name='clan_fight'),
    path('wars/delete/<int:pk>', WarDeleteView.as_view(), name='war_delete'),
    path('', WarListView.as_view(), name='home'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('clans/', ClanListView.as_view(), name='clan_list'),
    path('clans/<int:pk>', ClanDetailView.as_view(), name='clan_details'),
    path('clans/delete', ClanDeleteView.as_view(), name='clan_delete'),
    path('clans/update', ClanUpdateView.as_view(), name='clan_update'),
    path('clans/exit', ClanLeaveView.as_view(), name='clan_leave'),
    path('clans/remove/<str:username>', ClanRemoveView.as_view(), name='clan_remove'),
    path('clans/join/<int:pk>', ClanJoinView.as_view(), name='clan_join'),
]
