from django.test import TestCase
from django.utils import timezone
from manager.models import War, UserSnapshot, User, Clan, Battle

class TestModels(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="Test", password="Models")
        self.user2 = User.objects.create_user(username="Test2", password="Models2")
        self.user3 = User.objects.create_user(username="Test3", password="Models3")
        clan = Clan.objects.create(name="TestClan", maxMembers=10, clanMaster=self.user)
        clan2 = Clan.objects.create(name="TestClan2", maxMembers=10, clanMaster=self.user2)
        self.user.clan = clan
        self.user.save()
        self.user2.clan = clan2
        self.user2.save()
        self.user3.clan = clan
        self.user3.save()
        self.war = War.objects.create(allyClan=clan, enemyClanName=clan2.name, date=timezone.now())
        self.us1 = UserSnapshot.objects.create(username="Test", isAlly=True, war=self.war)
        self.us2 = UserSnapshot.objects.create(username="Test2", isAlly=False, war=self.war)
        self.us3 = UserSnapshot.objects.create(username="Test3", isAlly=True, war=self.war)
        Battle.objects.create(ally=self.us1, enemy=self.us2, allyDestruction=60, enemyDestruction=30, allyVictory=True, war=self.war)
        Battle.objects.create(ally=self.us1, enemy=self.us2, allyDestruction=40, enemyDestruction=50, allyVictory=False, war=self.war)

    def test_war_is_won(self):
        self.assertTrue(self.war.won())
        Battle.objects.create(ally=self.us1, enemy=self.us2, allyDestruction=20, enemyDestruction=100, allyVictory=False, war=self.war)
        self.assertFalse(self.war.won())

    def test_war_get_ally(self):
        self.assertIsNotNone(self.war.getAlly(self.user))
        self.assertIsNone(self.war.getAlly(self.user2))
        self.assertIsNotNone(self.war.getAlly(self.user3))

    def test_war_can_add_battle(self):
        self.assertTrue(self.war.canAddBattle(self.user))
        self.assertFalse(self.war.canAddBattle(self.user2))
        self.assertTrue(self.war.canAddBattle(self.user3))
    
    def test_war_allies(self):
        allies = self.war.allies()
        self.assertEqual(allies.count(), 2)
        self.assertTrue(allies.filter(username=self.us1.username).exists())
        self.assertFalse(allies.filter(username=self.us2.username).exists())
        self.assertTrue(allies.filter(username=self.us3.username).exists())
    
    def test_war_enemies(self):
        enemies = self.war.enemies()
        self.assertEqual(enemies.count(), 1)
        self.assertFalse(enemies.filter(username=self.us1.username).exists())
        self.assertTrue(enemies.filter(username=self.us2.username).exists())
        self.assertFalse(enemies.filter(username=self.us3.username).exists())