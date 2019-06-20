from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from .forms import CustomUserCreationForm, ClanForm
from .models import *
from django.core.exceptions import PermissionDenied
from django.utils.http import urlencode
from django.forms import modelformset_factory, inlineformset_factory
from django.views.generic import (
    View,
    CreateView,
    ListView,
    DeleteView,
    DetailView,
    RedirectView,
    UpdateView,
    TemplateView,
)


class SignUpView(CreateView):

    form_class = CustomUserCreationForm
    success_url = reverse_lazy('user_login')
    template_name = 'user/signup.html'


class WarListView(ListView):

    template_name = 'wars/list.html'
    paginate_by = 100  # if pagination is desired

    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.clan is not None:
            return War.objects.filter(allyClan=self.request.user.clan)
        else:
            # TODO Create a home page for anonymous users
            # raise PermissionDenied()
            return []


class ClanListView(ListView):

    template_name = "clans/list.html"

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query is not None:
            return Clan.objects.filter(name__icontains=query)
        return Clan.objects.all()



class ClanDeleteView(DeleteView):

    template_name = "clans/delete.html"

    def get_object(self):
        clan = get_object_or_404(Clan, pk=self.request.user.clan.pk)
        if self.request.user.is_authenticated and self.request.user == clan.clanMaster:
            return clan
        else:
            raise PermissionDenied()

    def get_success_url(self):
        return reverse("clans_list")


class ClanDetailView(DetailView):

    template_name = "clans/details.html"

    def get_object(self):
        pk = self.kwargs.get("pk")
        return get_object_or_404(Clan, pk=pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        clan = self.get_object()
        context['canjoin'] = self.request.user.is_authenticated and (self.request.user.clan is None and User.objects.filter(clan=clan).count() < clan.maxPlayers)
        context["members"] = User.objects.filter(clan=clan)
        return context

    def dispatch(self, request, pk, *args, **kwargs):
        if request.user.is_authenticated and request.user == get_object_or_404(Clan, pk=pk).clanMaster:
            view = ClanUpdateView.as_view()
            return view(request, *args, **kwargs)
        return super().dispatch(request, pk, *args, **kwargs)


class ClanLeaveView(RedirectView):

    def dispatch(self, request, *args, **kwargs):
        request.user.clan = None
        request.user.save()
        return super().dispatch(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        return reverse("wars_list")


class ClanRemoveView(RedirectView):
    
    def dispatch(self, *args, **kwargs):
        member = get_object_or_404(User, username=self.kwargs.get("username"))
        member.clan = None
        member.save()
        return super().dispatch(self.request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        query = urlencode({'removed': self.kwargs.get("username")})
        return self.request.user.clan.get_absolute_url() + "?" + query


class ClanUpdateView(UpdateView):

    template_name = "clans/update.html"
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


class ClanJoinView(RedirectView):

    def dispatch(self, *args, **kwargs):
        pk = self.kwargs.get("pk")
        clan = get_object_or_404(Clan, pk=pk)
        user = self.request.user
        user.clan = clan
        user.save()
        return super().dispatch(self.request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        query = urlencode({'joined': True})
        return self.request.user.clan.get_absolute_url() + "?" + query


class WarCreateView(View):

    def dispatch(self, request, *args, **kwargs):
        myClan = self.request.user.clan
        if self.request.user.is_authenticated:
            if myClan is not None and myClan.clanMaster == self.request.user:
                pk = self.kwargs.get("pk")
                enemyClan = get_object_or_404(Clan, pk=pk)
                if (myClan != enemyClan):
                    newWar = War.objects.create(allyClan=myClan, enemyClanName=enemyClan.name, date=timezone.now())
                    myMembersCount = User.objects.filter(clan=myClan).count()
                    enemyMembers = User.objects.filter(clan=enemyClan)
                    battleCount = min(myMembersCount, len(enemyMembers))
                    newWar.save()
                    # TODO: manca il controllo sul successo dell'operazione - transaction
                    for i in range(battleCount):
                        enemy = enemyMembers[i]
                        newEnemySnapshot = EnemyUserSnapshot.objects.create(username=enemy.username, war=newWar)
                        newEnemySnapshot.save()
                    return redirect(newWar.get_absolute_url())
        raise PermissionDenied()


class WarDeleteView(DeleteView):

    def get_object(self):
        war = get_object_or_404(War, pk=self.kwargs.get("pk"))
        if self.request.user.is_authenticated and self.request.user == war.allyClan.clanMaster:
            return war
        else:
            raise PermissionDenied()

    def get_success_url(self):
        return reverse("wars_list")


class WarDetailView(DetailView):

    template_name = "wars/details.html"

    def get_object(self):
        pk = self.kwargs.get("pk")
        return get_object_or_404(War, pk=pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["enemies"] = EnemyUserSnapshot.objects.filter(war=self.get_object())
        context["allies"] = User.objects.filter(clan=self.request.user.clan)
        battles = Battle.objects.filter(war=self.get_object())
        context["battles"] = battles
        BattleFormSet = inlineformset_factory(War, Battle, exclude=("war", ), extra=0)  
        context["formset"] = BattleFormSet(instance=self.get_object())
        return context

    def dispatch(self, *args, **kwargs):
        if not (self.request.user.is_authenticated and self.request.user.clan == self.get_object().allyClan):
            raise PermissionDenied()
        return super().dispatch(self.request, *args, **kwargs)
