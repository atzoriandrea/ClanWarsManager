from django.test import TestCase, Client
from manager.models import User, Clan
from django.urls import reverse

"""
L’utente autenticato nel sistema deve poter creare un clan, se non fa già parte di un altro clan,
decidendone il nome e il numero massimo di membri e diventandone automaticamente il capo.
"""

class TestAcceptanceClanCreate(TestCase):
    def setUp(self):
        #Client
        self.client = Client()
        #User with no clan
        self.uN = User.objects.create_user(username="TestN", password="TestAcceptanceN")
        #Users
        self.u1 = User.objects.create_user(username="Test1", password="TestAcceptance1")
        self.u4 = User.objects.create_user(username="Test4", password="TestAcceptance4")
        #Clans
        self.c1 = Clan.objects.create(name="TestClan", clanMaster=self.u1)
        self.u1.clan = self.c1
        self.u1.save()
        self.u4.clan = self.c1
        self.u4.save()
        #Urls
        self.clanCreateUrl = reverse("clans_create")
        

    #User with no clan requests clan create view
    def test_acceptance_clan_create_user_no_clan(self):
        login = self.client.login(username="TestN", password="TestAcceptanceN") 
        self.assertTrue(login)
        response = self.client.post(self.clanCreateUrl)
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed("clans/update.html")
        response = self.client.get(self.clanCreateUrl)
        self.assertEqual(response.status_code, 405)

        self.uN.refresh_from_db()
        newClan = Clan.objects.get(id=2)
        self.assertIsNotNone(self.uN.clan)
        self.assertEqual(self.uN.clan, newClan)
        self.assertEqual(newClan.clanMaster, self.uN)
        self.client.logout()

    #Non logged user requests clan create view
    def test_acceptance_clan_create_unlogged_user(self):
        response = self.client.get(self.clanCreateUrl)
        self.assertEqual(response.status_code, 302)
        response = self.client.post(self.clanCreateUrl)
        self.assertEqual(response.status_code, 302)

    #User with clan requests clan create view 
    def test_acceptance_clan_create_user_with_clan(self):
        login = self.client.login(username="Test1", password="TestAcceptance1") 
        self.assertTrue(login)
        clan = self.u1.clan
        response = self.client.post(self.clanCreateUrl)
        self.assertEqual(response.status_code, 403)
        self.u1.refresh_from_db()
        self.assertEqual(self.u1.clan, clan)
        self.assertEqual(clan.clanMaster, self.u1)
        self.client.logout()
