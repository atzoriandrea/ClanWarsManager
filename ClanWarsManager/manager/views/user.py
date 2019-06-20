from django.urls import reverse_lazy
from ..forms import CustomUserCreationForm
from django.views.generic import CreateView

# User


class SignupView(CreateView):

    form_class = CustomUserCreationForm
    success_url = reverse_lazy('user_login')
    template_name = 'user/signup.html'
