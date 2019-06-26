from django.test import TestCase, Client
from manager.models import User, Clan, War, Battle, UserSnapshot
from django.urls import reverse
from django.utils import timezone

"""
L’utente autenticato nel sistema e membro di un clan, deve poter modificare una battaglia in cui è
coinvolto.
"""

class TestAcceptanceBattleUpdate(TestCase):
    def setUp(self):
        #Client
        self.client = Client()
        #Users
        self.u1 = User.objects.create_user(username="Test1", password="TestAcceptance1")
        self.u2 = User.objects.create_user(username="Test2", password="TestAcceptance2")
        self.u3 = User.objects.create_user(username="Test3", password="TestAcceptance3")
        self.u4 = User.objects.create_user(username="Test4", password="TestAcceptance4")
        #Clans
        self.c1 = Clan.objects.create(name="TestClan", clanMaster=self.u1)
        self.c2 = Clan.objects.create(name="TestClan2", maxMembers=1, clanMaster=self.u2)
        self.u1.clan = self.c1
        self.u1.save()
        self.u2.clan = self.c2
        self.u2.save()
        self.u3.clan = self.c2
        self.u3.save()
        self.u4.clan = self.c1
        self.u4.save()
        #Wars
        war = War.objects.create(allyClan=self.c1, enemyClanName=self.c2.name, date=timezone.now())
        #UserSnapshots
        ally = UserSnapshot.objects.create(username=self.u1.username, isAlly=True, war=war)
        enemy = UserSnapshot.objects.create(username=self.u2.username, isAlly=False, war=war)
        enemy2 = UserSnapshot.objects.create(username=self.u3.username, isAlly=False, war=war)
        ally2 = UserSnapshot.objects.create(username=self.u4.username, isAlly=True, war=war)
        #Battles
        Battle.objects.create(ally=ally, enemy=enemy, allyDestruction=20, enemyDestruction=30, allyVictory=False, war=war)
        Battle.objects.create(ally=ally2, enemy=enemy, allyDestruction=50, enemyDestruction=60, allyVictory=False, war=war)
        #Urls
        self.battleUpdateUrl1 = reverse("battles_update", kwargs={'pk': 1})
        self.battleUpdateUrl2 = reverse("battles_update", kwargs={'pk': 2})
        

    #User master requests battle update view
    def test_acceptance_battle_update_as_master(self):
        login = self.client.login(username="Test1", password="TestAcceptance1") 
        self.assertTrue(login)
        battle = Battle.objects.first()
        data = {
            "ally": 1,
            "enemy": 2,
            "allyDestruction": 100,
            "enemyDestruction": 50,
            "allyVictory": True
        }
        response = self.client.post(self.battleUpdateUrl1, data=data)
        self.assertEqual(response.status_code, 302)
        battle.refresh_from_db()
        self.assertEqual(battle.ally.username, self.u1.username)
        self.assertEqual(battle.enemy.username, self.u2.username)
        self.assertEqual(battle.allyDestruction, 100)
        self.assertEqual(battle.enemyDestruction, 50)
        self.assertTrue(battle.allyVictory)
        self.client.logout()
    
    #Non logged user requests battle update view
    def test_acceptance_battle_update_unlogged_user(self):
        response = self.client.get(self.battleUpdateUrl1)
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed("registration/login.html")
        response = self.client.post(self.battleUpdateUrl1)
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed("registration/login.html")

    #User member requests battle update view for his battle
    def test_acceptance_battle_update_own_battle_as_member(self):
        login = self.client.login(username="Test4", password="TestAcceptance4") 
        self.assertTrue(login)
        battle = Battle.objects.last()
        data = {
            "enemy": 3,
            "allyDestruction": 80,
            "enemyDestruction": 60,
            "allyVictory": True
        }
        response = self.client.post(self.battleUpdateUrl2, data=data)
        self.assertEqual(response.status_code, 302)
        battle.refresh_from_db()
        self.assertEqual(battle.ally.username, self.u4.username)
        self.assertEqual(battle.enemy.username, self.u3.username)
        self.assertEqual(battle.allyDestruction, 80)
        self.assertEqual(battle.enemyDestruction, 60)
        self.assertTrue(battle.allyVictory)
        self.client.logout()
