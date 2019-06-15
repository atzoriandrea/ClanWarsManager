from django.contrib import admin

from .models import User, Clan, War, Battle
# Register your models here.
admin.site.register(User)
admin.site.register(Clan)
admin.site.register(War)
admin.site.register(Battle)
