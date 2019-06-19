from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm, ClanForm
from .models import War, Clan, User
from django.core.exceptions import PermissionDenied
from django.utils.http import urlencode
from django.views.generic import (
    View,
    CreateView,
    ListView,
    DeleteView,
    DetailView, 
    RedirectView,
    UpdateView,
    TemplateView
    )


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

class WarListView(ListView):
    template_name = 'wars.html'
    paginate_by = 100  # if pagination is desired
    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.clan is not None:
            return War.objects.filter(clan=self.request.user.clan)
        else:
            return []

class ClanListView(ListView):
    queryset = Clan.objects.all()
    template_name = "clan/list.html"


class ClanDeleteView(DeleteView):
    template_name = "clan/delete.html"
    
    def get_object(self):
        clan = get_object_or_404(Clan, pk=self.request.user.clan.pk)
        if self.request.user.is_authenticated and self.request.user == clan.clanMaster:
            return clan
        else:
            raise PermissionDenied()

    def get_success_url(self):
        return reverse("clan_list")

class ClanDetailView(DetailView):
    template_name = "clan/details.html"
    def get_object(self):
        pk = self.kwargs.get("pk")
        return get_object_or_404(Clan, pk=pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["members"] = User.objects.filter(clan=self.get_object())
        return context

    def dispatch(self, request, pk, *args, **kwargs):
        if request.user.is_authenticated and request.user == get_object_or_404(Clan, pk=pk).clanMaster:
            view=ClanUpdateView.as_view()
            return view(request, *args, **kwargs)
        return super().dispatch(request, pk, *args, **kwargs)

class ClanLeaveView(RedirectView):
    def post(self, request, *args, **kwargs):
        request.user.clan = None
        request.user.save()
        return super().post(self, request, *args,**kwargs)
        
    def get_redirect_url(self, *args, **kwargs):
        return reverse("wars")

class ClanRemoveView(RedirectView):
    def post(self, request, *args, **kwargs):
        member = get_object_or_404(User, username=self.kwargs.get("username"))
        member.clan = None
        member.save()
        return super().post(self, request, *args,**kwargs)

    def get_redirect_url(self, *args, **kwargs):
        query = urlencode({'removed': self.kwargs.get("username")})
        return self.request.user.clan.get_absolute_url() + "?" + query

class ClanUpdateView(UpdateView):
    template_name = "clan/update.html"
    form_class = ClanForm

    def get_object(self):
        clan = self.request.user.clan
        if self.request.user.is_authenticated and self.request.user == clan.clanMaster:
            return clan
        else:
            raise PermissionDenied()
        return clan

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

    





    