from django.test import TestCase, Client
from manager.models import User, Clan
from django.urls import reverse

"""
L’utente autenticato nel sistema e membro di un clan, deve poter abbandonare il proprio clan.
"""

class TestAcceptanceClanLeave(TestCase):
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
        self.clanLeaveUrl = reverse("clans_leave")

    
    #User member requests clan leave view
    def test_acceptance_clan_leave_as_member(self):
        login = self.client.login(username="Test4", password="TestAcceptance4")
        self.assertTrue(login)
        clanMembers = User.objects.filter(clan=self.u4.clan).count()
        response = self.client.post(self.clanLeaveUrl)
        self.assertEqual(response.status_code, 302)
        updateClanMembers = User.objects.filter(clan=self.u4.clan).count()
        self.u4.refresh_from_db()
        self.assertIsNone(self.u4.clan)
        self.assertEqual(updateClanMembers, clanMembers - 1)
        self.client.logout()
        
    #Non logged user requests clan leave view
    def test_acceptance_clan_leave_unlogged_user(self):
        response = self.client.get(self.clanLeaveUrl)
        self.assertEqual(response.status_code, 302)
        response = self.client.post(self.clanLeaveUrl)
        self.assertEqual(response.status_code, 302)
    
    #User master requests clan leave view
    def test_acceptance_clan_leave_as_master(self):
        login = self.client.login(username="Test1", password="TestAcceptance1")
        self.assertTrue(login)
        response = self.client.post(self.clanLeaveUrl)
        self.assertEqual(response.status_code, 403)
        self.assertIsNotNone(self.u1.clan)
        self.client.logout()