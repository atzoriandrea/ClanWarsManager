from django.test import TestCase, Client
from manager.models import User, Clan
from django.urls import reverse

"""
L’utente autenticato nel sistema deve potersi unire ad un clan esistente, se non fa già parte di un altro
clan e se il clan a cui desidera unirsi non ha ancora raggiunto il numero massimo di membri.
"""

class TestAcceptanceClanJoin(TestCase):
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
        self.clan1JoinUrl = reverse("clans_join", kwargs={"pk": 1})
        self.clan2JoinUrl = reverse("clans_join", kwargs={"pk": 2})


    #User with no clan requests clan join view
    def test_acceptance_clan_join_user_no_clan(self):
        login = self.client.login(username="TestN", password="TestAcceptanceN")
        self.assertTrue(login)
        clanMembers = User.objects.filter(clan=self.c1).count()
        response = self.client.post(self.clan1JoinUrl)
        self.assertEqual(response.status_code, 302)
        updateClanMembers = User.objects.filter(clan=self.c1).count()
        self.uN.refresh_from_db()
        self.assertEqual(self.uN.clan, self.c1)
        self.assertEqual(updateClanMembers, clanMembers+1)
        self.client.logout()
        
    #User with clan requests clan join view
    def test_acceptance_clan_join_user_with_clan(self):
        login = self.client.login(username="Test2", password="TestAcceptance2")
        self.assertTrue(login)
        clanMembers = User.objects.filter(clan=self.c1).count()
        response = self.client.post(self.clan1JoinUrl)
        self.assertEqual(response.status_code, 403)
        updateClanMembers = User.objects.filter(clan=self.c1).count()
        self.assertNotEqual(self.u2.clan, self.c1)
        self.assertEqual(updateClanMembers, clanMembers)
        self.client.logout()

    #Non logged user requests clan join view
    def test_acceptance_clan_join_unlogged_user(self):
        response = self.client.get(self.clan1JoinUrl)
        self.assertEqual(response.status_code, 302)
        response = self.client.post(self.clan1JoinUrl)
        self.assertEqual(response.status_code, 302)
    
    #Join a clan with max members as user with no clan
    def test_acceptance_clan_join_max_members(self):
        login = self.client.login(username="TestN", password="TestAcceptanceN")
        self.assertTrue(login)
        clanMembers = User.objects.filter(clan=self.c2).count()
        response = self.client.post(self.clan2JoinUrl)
        self.assertEqual(response.status_code, 403)
        updateClanMembers = User.objects.filter(clan=self.c2).count()
        self.assertIsNone(self.uN.clan)
        self.assertEqual(updateClanMembers, clanMembers)
        self.client.logout()