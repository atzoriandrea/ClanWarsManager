from django.test import TestCase, Client
from manager.models import User, Clan
from django.urls import reverse

"""
Qualsiasi utente deve poter visualizzare, anche senza autenticarsi, la lista dei clan registrati e, per ogni
clan, la lista dei membri.
"""

class TestAcceptanceClanDetails(TestCase):
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
        self.clanDetailsUrl = reverse("clans_details", kwargs={"pk": 1})
    
    #Non logged user requests clan details view
    def test_acceptance_clan_details_unlogged_user(self):
        response = self.client.get(self.clanDetailsUrl)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("clans/details.html")
        
    #User with no clan requests clan details view
    def test_acceptance_clan_details_user_no_clan(self):
        login = self.client.login(username="TestN", password="TestAcceptanceN")
        response = self.client.get(self.clanDetailsUrl)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("clans/details.html")
        self.client.logout()

    #Clan member requests clan details view
    def test_acceptance_clan_details_member(self):
        login = self.client.login(username="Test4", password="TestAcceptance4")
        self.assertTrue(login)
        response = self.client.get(self.clanDetailsUrl)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("clans/details.html")
        self.client.logout()

    #Clan master requestss clan details view 
    def test_acceptance_clan_details_master(self):
        login = self.client.login(username="Test1", password="TestAcceptance1")
        self.assertTrue(login)
        response = self.client.get(self.clanDetailsUrl)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("clans/update.html")
        self.client.logout()