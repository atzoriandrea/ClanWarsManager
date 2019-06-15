from django.db import models

from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=30, primary_key=True)
    password = models.CharField(max_length=30)
    clan = models.ForeignKey("Clan", on_delete=models.SET_NULL, null=True, blank=True, default=None)

class Clan(models.Model):
    name = models.CharField(max_length=30)
    clanMaster = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+")
    maxPlayers = models.PositiveSmallIntegerField(default=20, validators=[MaxValueValidator(50)])

class War(models.Model):
    clan = models.ForeignKey(Clan, on_delete=models.CASCADE, related_name="+")
    date = models.DateField()

class Battle(models.Model):
    ally = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="+")
    enemy = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+")
    allyDestruction = models.SmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], default=0)
    enemyDestruction = models.SmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], default=0)
    allyVictory = models.BooleanField()
    war = models.ForeignKey(War, on_delete=models.CASCADE, related_name="+")

