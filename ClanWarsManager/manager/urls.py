from django.urls import path, reverse, reverse_lazy
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
    WarCreateView,
    WarDetailView,
    WarDeleteView,
    RedirectView
)

urlpatterns = [
    path('', RedirectView.as_view(url=reverse_lazy("wars_list")), name='home'),
    # User
    path('signup/', SignUpView.as_view(), name='user_signup'),
    path('login/', auth_views.LoginView.as_view(), name='user_login'),
    path('logout/', auth_views.LogoutView.as_view(), name='user_logout'),
    # Wars
    path('wars/', WarListView.as_view(), name='wars_list'),
    path('wars/<int:pk>', WarDetailView.as_view(), name='wars_details'),
    path('wars/<int:pk>/delete', WarDeleteView.as_view(), name='wars_delete'),
    # Clans
    path('clans/', ClanListView.as_view(), name='clans_list'),
    path('clans/<int:pk>', ClanDetailView.as_view(), name='clans_details'),
    path('clans/<int:pk>/fight/', WarCreateView.as_view(), name='clans_fight'),
    path('clans/<int:pk>/join/', ClanJoinView.as_view(), name='clan_join'),
    path('clans/delete', ClanDeleteView.as_view(), name='clan_delete'),
    path('clans/update', ClanUpdateView.as_view(), name='clan_update'),
    path('clans/leave', ClanLeaveView.as_view(), name='clan_leave'),
    path('clans/kick/<str:username>', ClanRemoveView.as_view(), name='clan_kick'),
]
