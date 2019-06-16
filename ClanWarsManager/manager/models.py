from django.contrib.auth.models import AbstractUser
from django.db import models

from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class User(AbstractUser):
    clan = models.ForeignKey("Clan", on_delete=models.SET_NULL, null=True, blank=True, default=None)
    def __str__(self):
        return self.username

class Clan(models.Model):
    name = models.CharField(max_length=30)
    clanMaster = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+")
    maxPlayers = models.PositiveSmallIntegerField(default=20, validators=[MaxValueValidator(50)])

    def __str__(self):
        return self.name

class War(models.Model):
    clan = models.ForeignKey(Clan, on_delete=models.CASCADE, related_name="+")
    date = models.DateField()

    def __str__(self):
        return self.clan.name

class Battle(models.Model):
    ally = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="+")
    enemy = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+")
    allyDestruction = models.SmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], default=0)
    enemyDestruction = models.SmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], default=0)
    allyVictory = models.BooleanField()
    war = models.ForeignKey(War, on_delete=models.CASCADE, related_name="+")

    def __str__(self):
        return self.ally.username + ' VS ' + self.enemy.username


