from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from ..models import War, EnemyUserSnapshot, Clan, Battle
from django.core.exceptions import PermissionDenied
from django.views.generic import (
    View,
    DeleteView,
    DetailView,
    ListView
)
class BattleListView(ListView):

    template_name = 'wars/list.html'
    paginate_by = 10
    context_object_name = "wars"

    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.clan is not None:
            war = get_object_or_404(War, pk=pk)
            return Battle.objects.filter(allyClan=self.request.user.clan)
        else:
            return []


class BattleCreateView(LoginRequiredMixin, View):
    def dispatch(self, request, pk, **kwargs):
        myClan = request.user.clan
        if myClan is not None and myClan.clanMaster == request.user:
            war = get_object_or_404(War, pk=pk)
            enemies = EnemyUserSnapshot.objects.get(war=war)
            newBattle = Battle.objects.create(allyClan=war.allyClan, enemyClanName=war.enemyClanName)
            newBattle.save()



    def dispatch(self, request, pk, **kwargs):
        myClan = request.user.clan
        if myClan is not None and myClan.clanMaster == request.user:
            enemyClan = get_object_or_404(Clan, pk=pk)
            if (myClan != enemyClan):

                for enemy in enemyClan.members.all():
                    newEnemySnapshot = EnemyUserSnapshot.objects.create(username=enemy.username, war=newWar)
                    newEnemySnapshot.save()
                return redirect(newBattle.get_absolute_url())
        raise PermissionDenied()


class BattleDeleteView(LoginRequiredMixin, DeleteView):

    success_url = reverse_lazy("wars_list")

    def get_object(self):
        war = get_object_or_404(War, pk=self.kwargs.get("pk"))
        if self.request.user == war.allyClan.clanMaster:
            return war
        else:
            raise PermissionDenied()


class BattleDetailView(LoginRequiredMixin, DetailView):

    template_name = "wars/details.html"
    context_object_name = "war"

    def get_object(self):
        war = get_object_or_404(War, pk=self.kwargs.get("pk"))
        if self.request.user.clan != war.allyClan:
            raise PermissionDenied()
        return war