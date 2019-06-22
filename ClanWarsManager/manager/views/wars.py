from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone
from django.utils.http import urlencode
from ..models import War, EnemyUserSnapshot, Clan
from django.core.exceptions import PermissionDenied
from django.views.generic import (
    View,
    DeleteView,
    DetailView,
    ListView
)
from django.db import transaction


class WarListView(ListView):

    template_name = 'wars/list.html'
    paginate_by = 10
    context_object_name = "wars"

    def get_queryset(self):
        if self.request.user.clan is None:
            raise PermissionDenied()
        return self.request.user.clan.wars.all()


class WarCreateView(View):

    http_method_names = ['post']

    def dispatch(self, request, pk, **kwargs):
        allyClan = request.user.clan
        if allyClan is not None and allyClan.clanMaster == request.user:
            enemyClan = get_object_or_404(Clan, pk=pk)
            if (allyClan != enemyClan):
                with transaction.atomic():
                    war = War.objects.create(allyClan=allyClan, enemyClanName=enemyClan.name, date=timezone.now())
                    war.save()
                    for enemy in enemyClan.members.all():
                        newEnemySnapshot = EnemyUserSnapshot.objects.create(username=enemy.username, war=war)
                        newEnemySnapshot.save()
                    query = urlencode({'created': True})
                    return redirect(war.get_absolute_url() + f"?{query}")
        raise PermissionDenied()


class WarDeleteView(DeleteView):

    http_method_names = ['post']
    model = War

    def get_success_url(self):
        query = urlencode({'deleted': True})
        return reverse("wars_list") + f"?{query}"

    def get_object(self):
        war = super().get_object()
        if self.request.user != war.allyClan.clanMaster:
            raise PermissionDenied()
        return war


class WarDetailView(DetailView):

    template_name = "wars/details.html"
    context_object_name = "war"
    model = War

    def get_object(self):
        war = super().get_object()
        if self.request.user.clan != war.allyClan:
            raise PermissionDenied()
        return war
