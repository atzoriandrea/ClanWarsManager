from django.test import TestCase, Client
from manager.models import User, Clan, War, Battle, UserSnapshot
from django.urls import reverse
from django.utils import timezone

"""
L’utente autenticato nel sistema e capo del suo clan, deve poter creare una guerra con un altro clan già
esistente. Deve, quindi, poter registrare battaglie, decidendo per ognuna il membro alleato e quello
nemico da far sfidare, le loro percentuali di distruzione e l’esito della singola battaglia.
"""

class TestAcceptanceWarCreate(TestCase):
    def setUp(self):
        #Client
        self.client = Client()
        #User with no clan
        self.uN = User.objects.create_user(username="TestN", password="TestAcceptanceN")
        #Users
        self.u1 = User.objects.create_user(username="Test1", password="TestAcceptance1")
        self.u2 = User.objects.create_user(username="Test2", password="TestAcceptance2")
        self.u4 = User.objects.create_user(username="Test4", password="TestAcceptance4")
        #Clans
        self.c1 = Clan.objects.create(name="TestClan", clanMaster=self.u1)
        self.c2 = Clan.objects.create(name="TestClan2", maxMembers=1, clanMaster=self.u2)
        self.u1.clan = self.c1
        self.u1.save()
        self.u2.clan = self.c2
        self.u2.save()
        self.u4.clan = self.c1
        self.u4.save()
        #Urls
        self.warCreateUrl = reverse('clans_fight', kwargs={'pk': 2})


    #User master requests war create view and battle create view
    def test_acceptance_war_create_as_master(self):
        login = self.client.login(username="Test1", password="TestAcceptance1")
        self.assertTrue(login)
        response = self.client.post(self.warCreateUrl)
        self.assertEqual(response.status_code, 302)
        newWar = War.objects.last()
        self.assertEqual(newWar.allyClan, self.u1.clan)
        self.assertLessEqual(newWar.date, timezone.now().date())
        
        #Create new battle
        battleCreateUrl = reverse('wars_addbattle', kwargs={'pk': newWar.pk})
        response = self.client.post(battleCreateUrl)
        self.assertEqual(response.status_code, 302)
        warBattles = Battle.objects.filter(war=newWar)
        self.assertTrue(warBattles.exists())
        self.assertEqual(warBattles.last().war, newWar)
        self.client.logout()

    #Non logged user requests ear create view
    def test_acceptance_war_create_unlogged_user(self):
        response = self.client.get(self.warCreateUrl)
        self.assertEqual(response.status_code, 302)
        response = self.client.post(self.warCreateUrl)
        self.assertEqual(response.status_code, 302)

    #User with no clan requests war create view
    def test_acceptance_war_create_user_no_clan(self):
        login = self.client.login(username="TestN", password="TestAcceptanceN")
        self.assertTrue(login)
        response = self.client.post(self.warCreateUrl)
        self.assertEqual(response.status_code, 403)
        self.assertFalse(War.objects.filter(allyClan=self.uN.clan).exists())
        
    #User member requests war create view
    def test_acceptance_war_create_as_member(self):
        login = self.client.login(username="Test4", password="TestAcceptance4")
        self.assertTrue(login)
        response = self.client.post(self.warCreateUrl)
        self.assertEqual(response.status_code, 403)
        self.assertFalse(War.objects.filter(allyClan=self.u4.clan).exists())