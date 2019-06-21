from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User, Clan, Battle


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = User
        fields = ('username', )


class CustomUserChangeForm(UserChangeForm):

    class Meta(UserChangeForm):
        model = User
        fields = ('username', 'clan')


class ClanForm(forms.ModelForm):
    class Meta:
        model = Clan
        fields = ['name', 'maxMembers']

# TODO: limita selezione enemy e ally a membri del clan corretto
class BattleForm(forms.ModelForm):
    class Meta:
        model = Battle
        fields = ['enemy', 'allyDestruction', 'enemyDestruction', 'allyVictory']

class BattleFormMaster(forms.ModelForm):
    class Meta:
        model = Battle
        fields = ['ally', 'enemy', 'allyDestruction', 'enemyDestruction', 'allyVictory']


