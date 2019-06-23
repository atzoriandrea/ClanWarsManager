from django.contrib.auth.models import AbstractUser
from django.db import models
from django.shortcuts import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import MaxValueValidator, MinValueValidator


class User(AbstractUser):

    clan = models.ForeignKey("Clan", on_delete=models.SET_NULL, null=True, blank=True, related_name="members")

    def __str__(self):
        return self.username


class Clan(models.Model):

    name = models.CharField(max_length=30)
    clanMaster = models.OneToOneField(User, on_delete=models.CASCADE, related_name="+", null=False, blank=False)
    maxMembers = models.PositiveSmallIntegerField(default=20, validators=[MinValueValidator(1), MaxValueValidator(50)])

    def get_absolute_url(self):
        return reverse("clans_details", kwargs={'pk': self.pk})

    def __str__(self):
        return self.name


class War(models.Model):

    allyClan = models.ForeignKey(Clan, on_delete=models.CASCADE, related_name="wars", null=False, blank=False)
    enemyClanName = models.TextField(max_length=30)
    date = models.DateField()

    def get_absolute_url(self):
        return reverse("wars_details", kwargs={'pk': self.pk})

    def won(self):
        battles = self.battles.all()
        #TODO: Fix
        #return battles.aggregate(sum=models.Sum('allyDestruction'))["sum"] > battles.aggregate(sum=models.Sum('enemyDestruction'))["sum"]
        return True

    def getAlly(self, user):
        try:
            return self.allies().get(username=user.username)
        except ObjectDoesNotExist:
            return None

    def canAddBattle(self, user):
        return  self.allyClan.clanMaster==user or self.getAlly(user) is not None


    def enemies(self):
        return self.warriors.filter(isAlly=False)

    def allies(self):
        return self.warriors.filter(isAlly=True)

    def __str__(self):
        return f"{self.allyClan.name} vs {self.enemyClanName} @{self.date}"


class UserSnapshot(models.Model):

    username = models.TextField(max_length=30)
    isAlly = models.BooleanField()
    war = models.ForeignKey(War, on_delete=models.CASCADE, related_name="warriors", null=False, blank=False)


    def __str__(self):
        return f"{self.username} @ {str(self.war)}"


class Battle(models.Model):

    ally = models.ForeignKey(UserSnapshot, on_delete=models.CASCADE, related_name="+", null=False, blank=False)
    enemy = models.ForeignKey(UserSnapshot, on_delete=models.CASCADE, related_name="+", null=False, blank=False)
    allyDestruction = models.SmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], default=0)
    enemyDestruction = models.SmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], default=0)
    allyVictory = models.BooleanField(default=False)
    war = models.ForeignKey(War, on_delete=models.CASCADE, related_name="battles", null=False, blank=False)

    def get_absolute_url(self):
        return reverse("battles_update", kwargs={'pk': self.pk})

    def __str__(self):
        return f"{self.ally.username} vs {self.enemy.username}"
