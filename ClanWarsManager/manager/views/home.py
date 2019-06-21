from django.shortcuts import render
from .wars import WarListView
from django.views.generic import View


class HomeDispatcherView(View):

    def dispatch(self, request, **kwargs):
        if request.user.is_authenticated and request.user.clan is not None:
            return WarListView.as_view()(request, **kwargs)
        else:
            return render(request, 'home/homepage.html')
