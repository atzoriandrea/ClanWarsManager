from django.urls import path, include, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView
from .views.home import HomeDispatcherView
from .views.battles import BattleCreateView, BattleDeleteView, BattleUpdateView
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
    ClanCreateView,
)

urlpatterns = [
    path(r'', HomeDispatcherView.as_view(), name='home'),
    # User
    path(r'', include([
        path(r'signup/', SignupView.as_view(), name='user_signup'),
        path(r'login/', auth_views.LoginView.as_view(), name='user_login'),
        path(r'logout/', auth_views.LogoutView.as_view(), name='user_logout'),
    ])),
    # Wars
    path(r'wars/', include([
        path(r'', login_required(WarListView.as_view()), name='wars_list'),
        path(r'<int:pk>', login_required(WarDetailView.as_view()), name='wars_details'),
        path(r'<int:pk>/delete', login_required(WarDeleteView.as_view()), name='wars_delete'),
        path(r'<int:pk>/addbattle', login_required(BattleCreateView.as_view()), name='wars_addbattle'),
    ])),
    #Battles
    path(r'battles/',include([
        path(r'<int:pk>/delete', login_required(BattleDeleteView.as_view()), name='battles_delete'),
        path(r'<int:pk>', login_required(BattleUpdateView.as_view()), name='battles_update'),
    ])),
    # Clans
    path(r'clans/', include([
        path(r'', ClanListView.as_view(), name='clans_list'),
        path(r'<int:pk>', ClanDetailsDispatcherView.as_view(), name='clans_details'),
        path(r'<int:pk>/fight/', login_required(WarCreateView.as_view()), name='clans_fight'),
        path(r'<int:pk>/join/', login_required(ClanJoinView.as_view()), name='clans_join'),
        path(r'delete', login_required(ClanDeleteView.as_view()), name='clans_delete'),
        path(r'update', login_required(ClanUpdateView.as_view()), name='clans_update'),
        path(r'leave', login_required(ClanLeaveView.as_view()), name='clans_leave'),
        path(r'create', login_required(ClanCreateView.as_view()), name='clans_create'),
        path(r'kick/<str:username>', login_required(ClanKickView.as_view()), name='clans_kick'),
    ])),
]
