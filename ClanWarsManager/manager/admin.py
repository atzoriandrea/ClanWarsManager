
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, Group

from .models import User, Clan, War, Battle, EnemyUserSnapshot

class CustomUserAdmin(UserAdmin):
    
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ['username', 'clan']
    fieldsets = (
        (('User'), {'fields': ('username', 'clan')}),
    )

admin.site.register(User, CustomUserAdmin)
admin.site.unregister(Group)
admin.site.register(Clan)
admin.site.register(War)
admin.site.register(Battle)
admin.site.register(EnemyUserSnapshot)