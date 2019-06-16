from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import ListView
from .models import War


from .forms import CustomUserCreationForm

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

class WarsView(ListView):
    def get_queryset(self):
        return War.objects.all() #filter(clan=self.request.user.clan)
    paginate_by = 100  # if pagination is desired

    template_name = 'home.html'