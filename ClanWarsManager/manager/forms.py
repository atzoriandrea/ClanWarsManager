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

    _USER_LABEL_FROM_INSTANCE = lambda u : u.username

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['enemy'].queryset = self.instance.war.enemies().all()
        self.fields['enemy'].empty_label = None
        self.fields['enemy'].label_from_instance = BattleForm._USER_LABEL_FROM_INSTANCE

    class Meta:
        model = Battle
        exclude = ['ally', 'war']


class BattleFormMaster(BattleForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['ally'].queryset = self.instance.war.allies().all()
        self.fields['ally'].empty_label = None
        self.fields['ally'].label_from_instance = BattleFormMaster._USER_LABEL_FROM_INSTANCE

    class Meta:
        model = Battle
        exclude = ['war']
