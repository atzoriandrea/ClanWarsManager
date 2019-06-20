from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from ..models import War, EnemyUserSnapshot, Clan
from django.core.exceptions import PermissionDenied
from django.views.generic import (
    View,
    DeleteView,
    DetailView,
    ListView
)

# Wars

# TODO Create a home page for anonymous users
# class WarListView(LoginRequiredMixin, ListView):


class WarListView(ListView):

    template_name = 'wars/list.html'
    paginate_by = 10

    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.clan is not None:
            return War.objects.filter(allyClan=self.request.user.clan)
        else:
            return []


class WarCreateView(LoginRequiredMixin, View):

    def dispatch(self, request, pk, **kwargs):
        myClan = request.user.clan
        if myClan is not None and myClan.clanMaster == request.user:
            enemyClan = get_object_or_404(Clan, pk=pk)
            if (myClan != enemyClan):
                newWar = War.objects.create(allyClan=myClan, enemyClanName=enemyClan.name, date=timezone.now())
                newWar.save()
                for enemy in enemyClan.members.all():
                    newEnemySnapshot = EnemyUserSnapshot.objects.create(username=enemy.username, war=newWar)
                    newEnemySnapshot.save()
                return redirect(newWar.get_absolute_url())
        raise PermissionDenied()


class WarDeleteView(LoginRequiredMixin, DeleteView):

    success_url = reverse_lazy("wars_list")

    def get_object(self):
        war = get_object_or_404(War, pk=self.kwargs.get("pk"))
        if self.request.user == war.allyClan.clanMaster:
            return war
        else:
            raise PermissionDenied()


class WarDetailView(LoginRequiredMixin, DetailView):

    template_name = "wars/details.html"

    def get_object(self):
        war = get_object_or_404(War, pk=self.kwargs.get("pk"))
        if self.request.user.clan != war.allyClan:
            raise PermissionDenied()
        return war