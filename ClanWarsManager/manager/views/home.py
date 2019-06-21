from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from ..models import War, EnemyUserSnapshot, Clan, Battle
from django.core.exceptions import PermissionDenied
from .wars import WarListView
from django.views.generic import (
    View,
    DeleteView,
    DetailView,
    ListView,
    TemplateView
)
class HomeDispatcherView(View):

    def dispatch(self, request, **kwargs):
        if request.user.is_authenticated:
            view = WarListView.as_view()
        else:
            return render(request, 'home/homepage.html')

        return view(request, **kwargs)

