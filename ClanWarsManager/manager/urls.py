from django.urls import path, reverse
from django.contrib.auth import views as auth_views
from .views import SignUpView, WarsView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('wars/', WarsView.as_view(), name='wars'),
    path('', WarsView.as_view(), name='home'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
