
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Clan, War, Battle
# Register your models here.





class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ['username']

admin.site.register(User, CustomUserAdmin)
# admin.site.register(User)
admin.site.register(Clan)
admin.site.register(War)
admin.site.register(Battle)