from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User, Clan, Battle


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = User
        fields = ['username']


class CustomUserChangeForm(UserChangeForm):

    class Meta(UserChangeForm):
        model = User
        fields = ['username', 'clan']


class ClanForm(forms.ModelForm):

    class Meta:
        model = Clan
        fields = ['name', 'maxMembers']


class BattleForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['enemy'].queryset = self.instance.war.enemies.all()
        self.fields['enemy'].empty_label = None

    class Meta:
        model = Battle
        exclude = ['ally', 'war']


class BattleFormMaster(BattleForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['ally'].queryset = self.instance.war.allyClan.members.all()
        self.fields['ally'].empty_label = None

    class Meta:
        model = Battle
        exclude = ['war']
