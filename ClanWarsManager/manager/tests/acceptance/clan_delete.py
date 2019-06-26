from django.test import TestCase, Client
from manager.models import User, Clan
from django.urls import reverse

"""
L’utente autenticato nel sistema e capo del suo clan, deve poter eliminare il proprio clan.
"""

class TestAcceptanceClanDelete(TestCase):
    def setUp(self):
        #Client
        self.client = Client()
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
        self.clanDeleteUrl = reverse("clans_delete")

    #User master requests clan delete view
    def test_acceptance_clan_delete_as_master(self):
        login = self.client.login(username="Test1", password="TestAcceptance1")
        self.assertTrue(login)
        clan = self.u1.clan
        response = self.client.post(self.clanDeleteUrl)
        self.assertEqual(response.status_code, 302)
        self.u1.refresh_from_db()
        self.u4.refresh_from_db()
        self.assertIsNone(self.u1.clan)
        self.assertIsNone(self.u4.clan)
        self.assertFalse(Clan.objects.filter(id=clan.id).exists())
        self.client.logout()
    
    #User member requests clan delete view
    def test_acceptance_clan_delete_as_member(self):
        login = self.client.login(username="Test4", password="TestAcceptance4")
        self.assertTrue(login)
        clan = self.u4.clan
        response = self.client.post(self.clanDeleteUrl)
        self.assertEqual(response.status_code, 403)
        self.u4.refresh_from_db()
        clan.refresh_from_db()
        self.assertIsNotNone(self.u4.clan)
        self.assertIsNotNone(clan)
        self.client.logout()

    #Non logged user requests clan delete view
    def test_acceptance_clan_delete_unlogged_user(self):
        response = self.client.get(self.clanDeleteUrl)
        self.assertEqual(response.status_code, 302)
        response = self.client.post(self.clanDeleteUrl)
        self.assertEqual(response.status_code, 302)