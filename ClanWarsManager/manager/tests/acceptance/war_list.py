from django.test import TestCase, Client
from manager.models import User, Clan, War, Battle
from django.urls import reverse
from django.utils import timezone

"""
L’utente autenticato nel sistema e membro di un clan, deve poter visualizzare la lista delle guerre
intraprese dal proprio clan. Le guerre aventi la somma delle percentuali di distruzione inflitte superiore
a quella delle subite, deve essere annotata come vinta.
"""

class TestAcceptanceWarList(TestCase):
    def setUp(self):
        #Client
        self.client = Client()
        #User with no clan
        self.uN = User.objects.create_user(username="TestN", password="TestAcceptanceN")
        #Users
        self.u1 = User.objects.create_user(username="Test1", password="TestAcceptance1")
        self.u2 = User.objects.create_user(username="Test2", password="TestAcceptance2")
        self.u3 = User.objects.create_user(username="Test3", password="TestAcceptance3")
        self.u4 = User.objects.create_user(username="Test4", password="TestAcceptance4")
        #Clans
        self.c1 = Clan.objects.create(name="TestClan", clanMaster=self.u1)
        self.c2 = Clan.objects.create(name="TestClan2", maxMembers=1, clanMaster=self.u2)
        self.c3 = Clan.objects.create(name="TestClan3", clanMaster=self.u3)
        self.u1.clan = self.c1
        self.u1.save()
        self.u2.clan = self.c2
        self.u2.save()
        self.u3.clan = self.c3
        self.u3.save()
        self.u4.clan = self.c1
        self.u4.save()
        #Wars
        War.objects.create(allyClan=self.c1, enemyClanName=self.c2.name, date=timezone.now())
        War.objects.create(allyClan=self.c2, enemyClanName=self.c3.name, date=timezone.now())
        #Urls
        self.warListUrl = reverse("wars_list")

    #Non logged user requests war list view
    def test_acceptance_war_list_unlogged_user(self):
        response = self.client.get(self.warListUrl)
        self.assertEqual(response.status_code, 302)
        response = self.client.post(self.warListUrl)
        self.assertEqual(response.status_code, 302)

    #User with clan requests war list view
    def test_acceptance_war_list_user_with_clan(self):
        login = self.client.login(username="Test1", password="TestAcceptance1")
        self.assertTrue(login)
        response = self.client.get(self.warListUrl)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("wars/list.html")
        self.client.logout()

    #User with no clan requests war list view
    def test_acceptance_war_list_user_no_clan(self):
        login = self.client.login(username="TestN", password="TestAcceptanceN")
        self.assertTrue(login)
        response = self.client.get(self.warListUrl)
        self.assertEqual(response.status_code, 403)
        self.client.logout()