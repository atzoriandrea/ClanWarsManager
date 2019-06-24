from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from manager.models import War, User, Clan

class TestWarViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.userWithoutClan = User.objects.create_user(username="TestN", password="ViewsN")
        self.user = User.objects.create_user(username="Test", password="Views")
        self.user2 = User.objects.create_user(username="Test2", password="Views2")
        self.user3 = User.objects.create_user(username="Test3", password="Views3")
        clan = Clan.objects.create(name="ClanTest", maxMembers=10, clanMaster=self.user)
        clan2 = Clan.objects.create(name="ClanTest2", maxMembers=10, clanMaster=self.user2)
        clan3 = Clan.objects.create(name="ClanTest3", maxMembers=10, clanMaster=self.user3)
        self.user.clan = clan
        self.user.save()
        self.user2.clan = clan2
        self.user2.save()
        self.user3.clan = clan3
        self.user3.save()
        War.objects.create(allyClan=clan, enemyClanName=clan2.name, date=timezone.now())
        War.objects.create(allyClan=clan2, enemyClanName=clan3.name, date=timezone.now())

    #WarListView Tests
    def test_wars_list(self):
        warListUrl = reverse("wars_list")
        login = self.client.login(username="Test", password="Views") 
        self.assertTrue(login)
        response = self.client.get(warListUrl)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "wars/list.html")
        self.client.logout()

        login = self.client.login(username="TestN", password="ViewsN") 
        self.assertTrue(login)
        response = self.client.get(warListUrl)
        self.assertEqual(response.status_code, 403)
        self.client.logout()

        response = self.client.get(warListUrl)
        self.assertEqual(response.status_code, 302)
        response = self.client.post(warListUrl)
        self.assertEqual(response.status_code, 302)

    #WarCreateView Tests
    def test_wars_create_valid_data(self):
        warCreateUrl = reverse("clans_fight", args=[2])
        login = self.client.login(username="Test", password="Views") 
        self.assertTrue(login)
        response = self.client.post(warCreateUrl)
        self.assertEqual(response.status_code, 302)
        self.client.logout()
    
        response = self.client.get(warCreateUrl)
        self.assertEqual(response.status_code, 302)
        response = self.client.post(warCreateUrl)
        self.assertEqual(response.status_code, 302)

    def test_wars_create_own_data(self):
        warCreateUrl = reverse("clans_fight", args=[1])
        login = self.client.login(username="Test", password="Views") 
        self.assertTrue(login)
        response = self.client.post(warCreateUrl)
        self.assertEqual(response.status_code, 403)
        self.client.logout()

    def test_wars_create_invalid_data(self):
        warCreateUrl = reverse("clans_fight", args=[4])
        login = self.client.login(username="Test", password="Views") 
        self.assertTrue(login)
        response = self.client.post(warCreateUrl)
        self.assertEqual(response.status_code, 404)
        self.client.logout()


    #WarDetailView Tests
    def test_wars_details_valid_data(self):
        warDetailsUrl = reverse("wars_details", args=[1])
        login = self.client.login(username="Test", password="Views") 
        self.assertTrue(login)
        response = self.client.get(warDetailsUrl)
        self.assertEqual(response.status_code, 200)
        self.client.logout()
    
        response = self.client.get(warDetailsUrl)
        self.assertEqual(response.status_code, 302)
        response = self.client.post(warDetailsUrl)
        self.assertEqual(response.status_code, 302)

    def test_wars_details_invalid_data(self):
        warDetailsUrl = reverse("wars_details", args=[3])
        login = self.client.login(username="Test", password="Views") 
        self.assertTrue(login)
        response = self.client.get(warDetailsUrl)
        self.assertEqual(response.status_code, 404)
        self.client.logout()
        
        warDetailsUrl = reverse("wars_details", args=[2])
        login = self.client.login(username="Test", password="Views") 
        self.assertTrue(login)
        response = self.client.get(warDetailsUrl)
        self.assertEqual(response.status_code, 403)
        self.client.logout()
    
    #WarDeleteView Tests
    def test_wars_delete_valid_data(self):
        warDeleteUrl = reverse("wars_delete", args=[1])
        login = self.client.login(username="Test", password="Views") 
        self.assertTrue(login)
        response = self.client.post(warDeleteUrl)
        self.assertEqual(response.status_code, 302)
        self.client.logout()
        
        response = self.client.get(warDeleteUrl)
        self.assertEqual(response.status_code, 302)
        response = self.client.post(warDeleteUrl)
        self.assertEqual(response.status_code, 302)

    def test_wars_delete_invalid_data(self):
        warDeleteUrl = reverse("wars_delete", args=[2])
        login = self.client.login(username="Test", password="Views") 
        self.assertTrue(login)
        response = self.client.post(warDeleteUrl)
        self.assertEqual(response.status_code, 403)
        self.client.logout()

        warDeleteUrl = reverse("wars_delete", args=[3])
        login = self.client.login(username="Test", password="Views") 
        self.assertTrue(login)
        response = self.client.post(warDeleteUrl)
        self.assertEqual(response.status_code, 404)
        self.client.logout()
    