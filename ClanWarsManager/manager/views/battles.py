from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.http import urlencode

from ..models import War, EnemyUserSnapshot, Clan, Battle
from django.core.exceptions import PermissionDenied
from django.views.generic import (
    View,
    DeleteView,
    DetailView,
    ListView
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