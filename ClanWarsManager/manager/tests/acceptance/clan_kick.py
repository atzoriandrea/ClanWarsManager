from django.test import TestCase, Client
from manager.models import User, Clan
from django.urls import reverse

"""
L’utente autenticato nel sistema e capo del suo clan, deve poter espellere i membri del suo clan.
"""

class TestAcceptanceClanKick(TestCase):
    def setUp(self):
        #Client
        self.client = Client()
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
        self.clanKickUrl1 = reverse("clans_kick", kwargs={"username": "Test1"})
        self.clanKickUrl2 = reverse("clans_kick", kwargs={"username": "Test2"})
        self.clanKickUrl3 = reverse("clans_kick", kwargs={"username": "Test4"})

    #User master requests clan kick (member) view 
    def test_acceptance_clan_kick_member_in_clan_as_cm(self):
        login = self.client.login(username="Test1", password="TestAcceptance1")
        self.assertTrue(login)
        clanMembers = User.objects.filter(clan=self.u4.clan).count()
        response = self.client.post(self.clanKickUrl3)
        self.assertEqual(response.status_code, 302)
        updatedClanMembers = User.objects.filter(clan=self.u4.clan).count()
        self.u4.refresh_from_db()
        self.assertIsNone(self.u4.clan)
        self.assertEqual(updatedClanMembers, clanMembers - 1)
        self.client.logout()


    #User member requests clan kick (member) view
    def test_acceptance_clan_kick_member_as_member(self):
        login = self.client.login(username="Test4", password="TestAcceptance4")
        self.assertTrue(login)
        clanMembers = User.objects.filter(clan=self.u1.clan).count()
        response = self.client.post(self.clanKickUrl1)
        self.assertEqual(response.status_code, 403)
        updatedClanMembers = User.objects.filter(clan=self.u1.clan).count()
        self.u1.refresh_from_db()
        self.assertIsNotNone(self.u1.clan)
        self.assertEqual(updatedClanMembers, clanMembers)
        self.client.logout()
    
    #User master requests clan kick (other clan master) view
    def test_acceptance_clan_kick_other_master_as_master(self):
        login = self.client.login(username="Test1", password="TestAcceptance1")
        self.assertTrue(login)
        response = self.client.post(self.clanKickUrl2)
        self.assertEqual(response.status_code, 403)
        self.u2.refresh_from_db()
        self.assertIsNotNone(self.u2.clan)
        self.client.logout()

    #Non logged user requests clan kick view
    def test_acceptance_clan_kick_unlogged_user(self):
        response = self.client.get(self.clanKickUrl1)
        self.assertEqual(response.status_code, 302)
        response = self.client.post(self.clanKickUrl1)
        self.assertEqual(response.status_code, 302)