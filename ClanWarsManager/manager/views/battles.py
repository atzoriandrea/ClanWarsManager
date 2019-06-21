from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.http import urlencode
from ..forms import BattleForm, BattleFormMaster
from ..models import War, EnemyUserSnapshot, Clan, Battle
from django.core.exceptions import PermissionDenied
from django.views.generic import (
    View,
    DeleteView,
    DetailView,
    ListView,
    UpdateView
)

class BattleCreateView(LoginRequiredMixin, View):
    def dispatch(self, request, **kwargs):
        war = get_object_or_404(War, pk=self.kwargs.get("pk"))
        if(request.user.clan != war.allyClan):
            raise PermissionDenied()
        firstEnemy = war.enemies.first()
        battle = Battle.objects.create(ally=request.user, enemy=firstEnemy, war=war)
        battle.save()
        query = urlencode({'created': True})
        return redirect(battle.get_absolute_url() + f"?{query}")

class BattleDeleteView(LoginRequiredMixin, DeleteView):

    success_url = reverse_lazy("wars_list") #TODO: riporta a lista battaglie
    model = Battle

    def get_object(self):
        battle = super().get_object()
        if self.request.user != battle.ally and self.request.user != battle.war.allyClan.clanMaster:
            raise PermissionDenied()
        return battle

class BattleUpdateView(LoginRequiredMixin, UpdateView):

    template_name = "battles/update.html"

    context_object_name = "battle"
    model = Battle

    def get_form_class(self):
        if self.request.user != self.object.war.allyClan.clanMaster:
            return BattleForm
        else:
            return BattleFormMaster

    def get_object(self):
        battle = super().get_object()
        if self.request.user != battle.war.allyClan.clanMaster and self.request.user != battle.ally:
            raise PermissionDenied()
        return battle