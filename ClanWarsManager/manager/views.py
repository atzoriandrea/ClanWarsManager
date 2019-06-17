from django.shortcuts import render, get_object_or_404, reverse
from django.urls import reverse_lazy
from .models import War, Clan
from django.views.generic import (
    CreateView, 
    ListView,
    DeleteView
)


from .forms import CustomUserCreationForm

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

class WarsView(ListView):
    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.clan is not None:
            return War.objects.filter(clan=self.request.user.clan)
        else:
            return []
    paginate_by = 100  # if pagination is desired

    template_name = 'wars.html'

class ClanListView(ListView):
    queryset = Clan.objects.all()
    template_name = "clan/list.html"

class DeleteClanView(DeleteView):
    template_name = "clan/delete.html"
    def get_object(self):
        pk = self.kwargs.get("pk")
        return get_object_or_404(Clan, pk=pk)

    def get_success_url(self):
        return reverse("clan_list")

    