from django.urls import path, include, reverse_lazy
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView
from .views.wars import (
    WarCreateView,
    WarDetailView,
    WarDeleteView,
    WarListView,
)
from .views.user import SignupView
from .views.clans import (
    ClanListView,
    ClanDeleteView,
    ClanDetailsDispatcherView,
    ClanLeaveView,
    ClanKickView,
    ClanUpdateView,
    ClanJoinView,
)

urlpatterns = [
    path(r'', RedirectView.as_view(url=reverse_lazy("wars_list")), name='home'),
    # User
    path(r'', include([
        path(r'signup/', SignupView.as_view(), name='user_signup'),
        path(r'login/', auth_views.LoginView.as_view(), name='user_login'),
        path(r'logout/', auth_views.LogoutView.as_view(), name='user_logout'),
    ])),
    # Wars
    path(r'wars', include([
        path(r'', WarListView.as_view(), name='wars_list'),
        path(r'<int:pk>', WarDetailView.as_view(), name='wars_details'),
        path(r'<int:pk>/delete', WarDeleteView.as_view(), name='wars_delete'),
    ])),
    # Clans
    path(r'clans', include([
        path(r'', ClanListView.as_view(), name='clans_list'),
        path(r'<int:pk>', ClanDetailsDispatcherView.as_view(), name='clans_details'),
        path(r'<int:pk>/fight/', WarCreateView.as_view(), name='clans_fight'),
        path(r'<int:pk>/join/', ClanJoinView.as_view(), name='clan_join'),
        path(r'delete', ClanDeleteView.as_view(), name='clan_delete'),
        path(r'update', ClanUpdateView.as_view(), name='clan_update'),
        path(r'leave', ClanLeaveView.as_view(), name='clan_leave'),
        path(r'kick/<str:username>', ClanKickView.as_view(), name='clan_kick'),
    ])),
]
