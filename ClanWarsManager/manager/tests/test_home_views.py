from django.test import TestCase, Client
from django.urls import reverse
from manager.models import User, Clan

class TestUserViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="Test", password="Views")
        self.user2 = User.objects.create_user(username="Test2", password="Views2")
        clan = Clan.objects.create(name="ClanTest", maxMembers=10, clanMaster=self.user)
        self.user.clan = clan
        self.user.save()

    #HomeDispatcherView Tests
    def test_home_dispatcher(self):
        homeUrl = reverse("home")
        login = self.client.login(username="Test", password="Views") 
        self.assertTrue(login)
        response = self.client.get(homeUrl)
        self.assertEqual(response.status_code, 200)
        self.client.logout()

        login = self.client.login(username="Test2", password="Views2") 
        self.assertTrue(login)
        response = self.client.get(homeUrl)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home/homepage.html")
        self.client.logout()

        response = self.client.get(homeUrl)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home/homepage.html")
        response = self.client.post(homeUrl)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home/homepage.html")