from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.urls import reverse_lazy
from .models import War, Clan, User
from django.core.exceptions import ObjectDoesNotExist
from django.utils.http import urlencode
from django.views.generic import (
    View,
    CreateView,
    ListView,
    DeleteView,
    DetailView, RedirectView)


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

class MyClan(DetailView):
    template_name = "clan/details.html"
    def get_object(self):
        pk = self.kwargs.get("pk")
        return get_object_or_404(Clan, pk=pk)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['removedUser'] = None
        if "removed" in self.request.GET:
            try:
                context["removedUser"] = User.objects.get(username=self.request.GET.get("removed"))
            except:
                pass
        context["members"] = User.objects.filter(clan=self.get_object())
        return context

class ExitClan(View):
    template_name = "wars.html"
    def post(self, request, *args, **kwargs):
        request.user.clan = None
        request.user.save()
        return render(request, self.template_name, {})

class RemoveUserFromClan(RedirectView):
    def post(self, request, *args, **kwargs):
        member = get_object_or_404(User, username=self.kwargs.get("username"))
        member.clan = None
        member.save()
        return super().post(self, request, *args,**kwargs)
    def get_redirect_url(self, *args, **kwargs):
        query = urlencode({'removed': self.kwargs.get("username")})
        return reverse("clan", kwargs={'pk': self.request.user.clan.pk}) + "?" + query






    