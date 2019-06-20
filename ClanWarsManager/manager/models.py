from django.contrib.auth.models import AbstractUser
from django.db import models
from django.shortcuts import reverse

from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class User(AbstractUser):
    clan = models.ForeignKey("Clan", on_delete=models.SET_NULL, null=True, blank=True, default=None)
    
    def __str__(self):
        return self.username

class Clan(models.Model):
    name = models.CharField(max_length=30)
    clanMaster = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+")
    maxPlayers = models.PositiveSmallIntegerField(default=20, validators=[MinValueValidator(1), MaxValueValidator(50)])

    def get_absolute_url(self):
        return reverse("clans_details", kwargs={'pk': self.pk})

    def __str__(self):
        return self.name

class War(models.Model):
    allyClan = models.ForeignKey(Clan, on_delete=models.CASCADE, related_name="+")
    enemyClanName = models.TextField(max_length=30)
    date = models.DateField()

    def get_absolute_url(self):
        return reverse("wars_details", kwargs={'pk': self.pk})

    def __str__(self):
        return f"{self.allyClan.name} vs {self.enemyClanName} @{self.date}"

class EnemyUserSnapshot(models.Model):
    username = models.TextField(max_length=30)
    war = models.ForeignKey(War, on_delete=models.CASCADE, related_name="+")

    def __str__(self):
        return f"{self.username} @ {str(self.war)}"

class Battle(models.Model):
    ally = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+")
    enemy = models.ForeignKey(EnemyUserSnapshot, on_delete=models.CASCADE, related_name="+")
    allyDestruction = models.SmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], default=0)
    enemyDestruction = models.SmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], default=0)
    allyVictory = models.BooleanField()
    war = models.ForeignKey(War, on_delete=models.CASCADE, related_name="+")

    def __str__(self):
        return f"{self.ally.username} vs {self.enemy.username}"

