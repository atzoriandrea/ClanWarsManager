from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from manager.models import War, User, Clan, UserSnapshot, Battle
class TestWarViews(TestCase):

    def setUp(self):
        self.client = Client()
        User.objects.create_user(username="TestN", password="ViewsN")
        user = User.objects.create_user(username="Test", password="Views")
        user2 = User.objects.create_user(username="Test2", password="Views2")
        user3 = User.objects.create_user(username="Test3", password="Views3")
        user4 = User.objects.create_user(username="Test4", password="Views4")
        clan = Clan.objects.create(name="ClanTest", maxMembers=10, clanMaster=user)
        clan2 = Clan.objects.create(name="ClanTest2", maxMembers=10, clanMaster=user2)
        clan3 = Clan.objects.create(name="ClanTest3", maxMembers=10, clanMaster=user3)
        user.clan = clan
        user.save()
        user2.clan = clan2
        user2.save()
        user3.clan = clan3
        user3.save()
        user4.clan = clan
        user4.save()
        war = War.objects.create(allyClan=clan, enemyClanName=clan2.name, date=timezone.now())
        war2 = War.objects.create(allyClan=clan2, enemyClanName=clan3.name, date=timezone.now())
        ally = UserSnapshot.objects.create(username="Test", isAlly=True, war=war)
        enemy = UserSnapshot.objects.create(username="Test2", isAlly=False, war=war)
        ally2 = UserSnapshot.objects.create(username="Test3", isAlly=True, war=war)
        Battle.objects.create(ally=ally, enemy=enemy, war=war)
        Battle.objects.create(ally=enemy, enemy=ally2, war=war2)

    #BattleCreateView Tests
    def test_battle_create_valid_data(self):
        battleCreateUrl = reverse("wars_addbattle", kwargs={"pk": 1})
        login = self.client.login(username="Test", password="Views") 
        self.assertTrue(login)
        response = self.client.post(battleCreateUrl)
        self.assertEqual(response.status_code, 302)
        newBattle = Battle.objects.last()
        war = War.objects.get(id=1)
        self.assertEqual(newBattle.war, war)
        ally = UserSnapshot.objects.get(username="Test")
        self.assertEqual(newBattle.ally, ally)
        enemy = UserSnapshot.objects.get(username="Test2")
        self.assertEqual(newBattle.enemy, enemy)
        self.client.logout()

        login = self.client.login(username="TestN", password="ViewsN") 
        self.assertTrue(login)
        response = self.client.post(battleCreateUrl)
        self.assertEqual(response.status_code, 403)
        self.client.logout()

        response = self.client.get(battleCreateUrl)
        self.assertEqual(response.status_code, 302)
        response = self.client.post(battleCreateUrl)
        self.assertEqual(response.status_code, 302)

    def test_battle_create_invalid_data(self):
        battleCreateUrl = reverse("wars_addbattle", kwargs={"pk": 100})
        login = self.client.login(username="Test", password="Views") 
        self.assertTrue(login)
        response = self.client.post(battleCreateUrl)
        self.assertEqual(response.status_code, 404)
        self.client.logout()

        battleCreateUrl = reverse("wars_addbattle", kwargs={"pk": 2})
        login = self.client.login(username="Test", password="Views") 
        self.assertTrue(login)
        response = self.client.post(battleCreateUrl)
        self.assertEqual(response.status_code, 403)
        self.client.logout()
        
        battleCreateUrl = reverse("wars_addbattle", kwargs={"pk": 1})
        login = self.client.login(username="Test4", password="Views4") 
        self.assertTrue(login)
        response = self.client.post(battleCreateUrl)
        self.assertEqual(response.status_code, 403)
        self.client.logout()

    #BattleUpdateView Tests
    def test_battle_update_valid_data(self):
        battleUpdateUrl = reverse("battles_update", kwargs={'pk': 1})
        login = self.client.login(username="Test", password="Views") 
        self.assertTrue(login)
        battle = Battle.objects.get(id=1)
        data = {
            "ally": 1,
            "enemy": 2,
            "allyDestruction": 100,
            "enemyDestruction": 50,
        }
        response = self.client.post(battleUpdateUrl, data=data)
        self.assertEqual(response.status_code, 302)
        battle.refresh_from_db()
        self.assertEqual(battle.allyDestruction, 100)
        self.assertEqual(battle.enemyDestruction, 50)
        self.client.logout()
    
        response = self.client.get(battleUpdateUrl)
        self.assertEqual(response.status_code, 302)
        response = self.client.post(battleUpdateUrl)
        self.assertEqual(response.status_code, 302)

    def test_battle_update_invalid_data(self):
        battleUpdateUrl = reverse("battles_update", kwargs={'pk': 100})
        login = self.client.login(username="Test", password="Views") 
        self.assertTrue(login)
        response = self.client.get(battleUpdateUrl)
        self.assertEqual(response.status_code, 404)
        self.client.logout()
        
        battleUpdateUrl = reverse("battles_update", kwargs={'pk': 2})
        login = self.client.login(username="Test", password="Views") 
        self.assertTrue(login)
        response = self.client.get(battleUpdateUrl)
        self.assertEqual(response.status_code, 403)
        self.client.logout()
    
    #BattleDeleteView Tests
    def test_battle_delete_valid_data(self):
        battleDeleteUrl = reverse("battles_delete", kwargs={"pk": 1})
        login = self.client.login(username="Test", password="Views") 
        self.assertTrue(login)
        response = self.client.post(battleDeleteUrl)
        self.assertEqual(response.status_code, 302)
        response = self.client.post(reverse("battles_update", kwargs={"pk": 1})
        self.assertEqual(response.status_code, 404)
        self.client.logout()
        
        response = self.client.get(battleDeleteUrl)
        self.assertEqual(response.status_code, 302)
        response = self.client.post(battleDeleteUrl)
        self.assertEqual(response.status_code, 302)

    def test_battle_delete_invalid_data(self):
        battleDeleteUrl = reverse("battles_delete", kwargs={"pk": 2})
        login = self.client.login(username="Test", password="Views") 
        self.assertTrue(login)
        response = self.client.post(battleDeleteUrl)
        self.assertEqual(response.status_code, 403)
        self.client.logout()

        battleDeleteUrl = reverse("battles_delete", kwargs={"pk": 1})
        login = self.client.login(username="Test4", password="Views4") 
        self.assertTrue(login)
        response = self.client.post(battleDeleteUrl)
        self.assertEqual(response.status_code, 403)
        self.client.logout()

        battleDeleteUrl = reverse("battles_delete", kwargs={"pk": 100})
        login = self.client.login(username="Test", password="Views") 
        self.assertTrue(login)
        response = self.client.post(battleDeleteUrl)
        self.assertEqual(response.status_code, 404)
        self.client.logout()