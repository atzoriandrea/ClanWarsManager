from django.test import TestCase, Client
from manager.models import User, Clan
from django.urls import reverse

"""
Qualsiasi utente deve poter visualizzare, anche senza autenticarsi, la lista dei clan registrati e, per ogni
clan, la lista dei membri.
"""

class TestAcceptanceClanList(TestCase):
    def setUp(self):
        #Client
        self.client = Client()
        #User with no clan
        self.uN = User.objects.create_user(username="TestN", password="TestAcceptanceN")
        #Users
        self.u1 = User.objects.create_user(username="Test1", password="TestAcceptance1")
        #Clans
        self.c1 = Clan.objects.create(name="TestClan", clanMaster=self.u1)
        self.u1.clan = self.c1
        self.u1.save()
        #Urls
        self.clanListUrl = reverse("clans_list")


    #Non logged user requests clan list view
    def test_acceptance_clan_list_unlogged_user(self):
        response = self.client.get(self.clanListUrl)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("clans/list.html")

    #User with no clan requests clan list view
    def test_acceptance_clan_list_user_no_clan(self):
        login = self.client.login(username="TestN", password="TestAcceptanceN")
        self.assertTrue(login)
        response = self.client.get(self.clanListUrl)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("clans/list.html")
        self.client.logout()

    #User with clan requests clan list view
    def test_acceptance_clan_list_user_with_clan(self):
        login = self.client.login(username="Test1", password="TestAcceptance1")
        self.assertTrue(login)
        response = self.client.get(self.clanListUrl)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("clans/list.html")
        self.client.logout()