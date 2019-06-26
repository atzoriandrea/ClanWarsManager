from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.http import urlencode
from ..forms import BattleForm, BattleFormMaster
from ..models import War, UserSnapshot, Clan, Battle
from django.core.exceptions import PermissionDenied
from django.views.generic import (
    View,
    DeleteView,
    DetailView,
    ListView,
    UpdateView
)


class BattleCreateView(View):

    http_method_names = ['post']
    
    def post(self, request, **kwargs):
        war = get_object_or_404(War, pk=self.kwargs.get("pk"))
        ally = war.getAlly(request.user)
        if(ally is None):
            if (request.user == war.allyClan.clanMaster):
                ally = war.allies().first()
            else:
                raise PermissionDenied()
        firstEnemy = war.enemies().first()
        battle = Battle.objects.create(ally=ally, enemy=firstEnemy, war=war)
        battle.save()
        query = urlencode({'created': True})
        return redirect(battle.get_absolute_url() + f"?{query}")


class BattleDeleteView(DeleteView):

    http_method_names = ['post']
    model = Battle

    def get_success_url(self):
        query = urlencode({'deleted': True})
        return self.object.war.get_absolute_url() + f"?{query}"

    def get_object(self):
        battle = super().get_object()
        if self.request.user != battle.ally and self.request.user != battle.war.allyClan.clanMaster:
            raise PermissionDenied()
        return battle


class BattleUpdateView(UpdateView):

    template_name = "battles/update.html"
    context_object_name = "battle"
    model = Battle

    def get_form_class(self):
        if self.request.user == self.object.war.allyClan.clanMaster:
            return BattleFormMaster
        else:
            return BattleForm

    def get_object(self):
        battle = super().get_object()
        if self.request.user != battle.war.allyClan.clanMaster and battle.war.getAlly(self.request.user) is None:
            raise PermissionDenied()
        return battle
