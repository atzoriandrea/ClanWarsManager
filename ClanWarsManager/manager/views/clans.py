from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from ..forms import ClanForm
from ..models import User, Clan
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.utils.http import urlencode
from django.views.generic import (
    View,
    DeleteView,
    DetailView,
    UpdateView,
    ListView
)


class ClanListView(ListView):

    template_name = "clans/list.html"
    paginate_by = 4
    context_object_name = "clans"

    def get_queryset(self):
        query = self.request.GET.get("q")
        if query is not None:
            return Clan.objects.filter(name__icontains=query)
        return Clan.objects.all()


class ClanDeleteView(DeleteView):

    http_method_names = ['post']

    def get_success_url(self):
        query = urlencode({'clanDeleted': True})
        return reverse("home") + f"?{query}"

    def get_object(self):
        clan = self.request.user.clan
        if self.request.user == clan.clanMaster:
            return clan
        else:
            raise PermissionDenied()


class ClanDetailsView(DetailView):

    template_name = "clans/details.html"
    context_object_name = "clan"
    model = Clan


class ClanDetailsDispatcherView(View):

    def dispatch(self, request, **kwargs):
        clan = get_object_or_404(Clan, pk=self.kwargs.get("pk"))
        if request.user.is_authenticated and clan.clanMaster == request.user:
            view = ClanUpdateView.as_view()
        else:
            view = ClanDetailsView.as_view()
        return view(request, **kwargs)


class ClanLeaveView(View):

    http_method_names = ['post']

    def dispatch(self, request, **kwargs):
        clan = request.user.clan
        if clan is None or clan.clanMaster == request.user:
            raise PermissionDenied()
        request.user.clan = None
        request.user.save()
        query = urlencode({'leaved': True})
        return redirect(clan.get_absolute_url() + f"?{query}")


class ClanKickView(View):

    http_method_names = ['post']

    def dispatch(self, request, **kwargs):
        username = self.kwargs.get("username")
        member = get_object_or_404(User, username=username)
        if member.clan.clanMaster != request.user or member == request.user:
            raise PermissionDenied()
        clan = member.clan
        member.clan = None
        member.save()
        query = urlencode({'kicked': True})
        return redirect(clan.get_absolute_url() + f"?{query}")


class ClanUpdateView(UpdateView):

    template_name = "clans/update.html"
    form_class = ClanForm
    context_object_name = "clan"

    def get_object(self):
        clan = self.request.user.clan
        if self.request.user != clan.clanMaster:
            raise PermissionDenied()
        return clan


class ClanCreateView(View):

    http_method_names = ['post']
    
    def dispatch(self, request, **kwargs):
        if request.user.clan is not None:
            raise PermissionDenied()
        clan = Clan.objects.create(name='', clanMaster=request.user)
        clan.save()
        request.user.clan = clan
        request.user.save()
        query = urlencode({'created': True})
        return redirect(clan.get_absolute_url() + f"?{query}")


class ClanJoinView(View):

    http_method_names = ['post']
    
    def dispatch(self, request, pk, **kwargs):
        clan = get_object_or_404(Clan, pk=pk)
        if request.user.clan is not None or clan.members.count() >= clan.maxMembers:
            raise PermissionDenied()
        request.user.clan = clan
        request.user.save()
        query = urlencode({'joined': True})
        return redirect(clan.get_absolute_url() + f"?{query}")
