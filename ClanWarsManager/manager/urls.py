from django.urls import path
from .views import SignUpView,WarsView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('wars/', WarsView.as_view(), name='wars'),
]