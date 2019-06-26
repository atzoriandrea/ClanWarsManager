from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from manager.models import War, User, Clan

class TestWarViews(TestCase):

    def setUp(self):
        self.client = Client()
        User.objects.create_user(username="TestN", password="ViewsN")
        self.user = User.objects.create_user(username="Test", password="Views")
        user2 = User.objects.create_user(username="Test2", password="Views2")
        user3 = User.objects.create_user(username="Test3", password="Views3")
        clan = Clan.objects.create(name="ClanTest", maxMembers=10, clanMaster=self.user)
        clan2 = Clan.objects.create(name="ClanTest2", maxMembers=10, clanMaster=user2)
        clan3 = Clan.objects.create(name="ClanTest3", maxMembers=10, clanMaster=user3)
        self.user.clan = clan
        self.user.save()
        user2.clan = clan2
        user2.save()
        user3.clan = clan3
        user3.save()
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
        warCreateUrl = reverse("clans_fight", kwargs={"pk": 2})
        login = self.client.login(username="Test", password="Views") 
        self.assertTrue(login)
        response = self.client.post(warCreateUrl)
        newWar = War.objects.last()
        enemyClan = Clan.objects.get(id=2)
        self.assertEqual(newWar.allyClan, self.user.clan)
        self.assertEqual(newWar.enemyClanName, enemyClan.name)
        self.assertLessEqual(newWar.date, timezone.now().date())
        self.assertEqual(response.status_code, 302)
        self.client.logout()
    
        response = self.client.get(warCreateUrl)
        self.assertEqual(response.status_code, 302)
        response = self.client.post(warCreateUrl)
        self.assertEqual(response.status_code, 302)

    def test_wars_create_own_data(self):
        warCreateUrl = reverse("clans_fight", kwargs={"pk": 1})
        login = self.client.login(username="Test", password="Views") 
        self.assertTrue(login)
        response = self.client.post(warCreateUrl)
        self.assertEqual(response.status_code, 403)
        self.client.logout()

    def test_wars_create_invalid_data(self):
        warCreateUrl = reverse("clans_fight", kwargs={"pk": 100})
        login = self.client.login(username="Test", password="Views") 
        self.assertTrue(login)
        response = self.client.post(warCreateUrl)
        self.assertEqual(response.status_code, 404)
        self.client.logout()


    #WarDetailView Tests
    def test_wars_details_valid_data(self):
        warDetailsUrl = reverse("wars_details", kwargs={"pk": 1})
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
        warDetailsUrl = reverse("wars_details", kwargs={"pk": 100})
        login = self.client.login(username="Test", password="Views") 
        self.assertTrue(login)
        response = self.client.get(warDetailsUrl)
        self.assertEqual(response.status_code, 404)
        self.client.logout()
        
        warDetailsUrl = reverse("wars_details", kwargs={"pk": 2})
        login = self.client.login(username="Test", password="Views") 
        self.assertTrue(login)
        response = self.client.get(warDetailsUrl)
        self.assertEqual(response.status_code, 403)
        self.client.logout()
    
    #WarDeleteView Tests
    def test_wars_delete_valid_data(self):
        warDeleteUrl = reverse("wars_delete", kwargs={"pk": 1})
        login = self.client.login(username="Test", password="Views") 
        self.assertTrue(login)
        response = self.client.post(warDeleteUrl)
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse("wars_details", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, 404)
        self.client.logout()
        
        response = self.client.get(warDeleteUrl)
        self.assertEqual(response.status_code, 302)
        response = self.client.post(warDeleteUrl)
        self.assertEqual(response.status_code, 302)

    def test_wars_delete_invalid_data(self):
        warDeleteUrl = reverse("wars_delete", kwargs={"pk": 2})
        login = self.client.login(username="Test", password="Views") 
        self.assertTrue(login)
        response = self.client.post(warDeleteUrl)
        self.assertEqual(response.status_code, 403)
        self.client.logout()

        warDeleteUrl = reverse("wars_delete", kwargs={"pk": 3})
        login = self.client.login(username="Test", password="Views") 
        self.assertTrue(login)
        response = self.client.post(warDeleteUrl)
        self.assertEqual(response.status_code, 404)
        self.client.logout()
    