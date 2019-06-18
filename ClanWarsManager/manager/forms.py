from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User, Clan

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
        fields = ['name', 'maxPlayers']
