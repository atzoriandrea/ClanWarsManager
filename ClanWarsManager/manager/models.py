from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=30, primary_key=True)
    password = models.CharField(max_length=30)
    clan = models.ForeignKey("Clan",on_delete=models.SET_NULL, null=True, blank=True, default=None)

class Clan(models.Model):
    name = models.CharField(max_length=30)
    clanMaster = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+")
    maxPlayers = models.PositiveSmallIntegerField(default=20,validators=[MaxValueValidator(50)])


