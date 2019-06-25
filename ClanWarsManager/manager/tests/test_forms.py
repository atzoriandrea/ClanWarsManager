from django.test import TestCase
from manager.forms import BattleForm, BattleFormMaster, ClanForm, CustomUserCreationForm, CustomUserChangeForm
from manager.models import User, Clan, War, UserSnapshot, Battle
from django.utils import timezone

class TestsForms(TestCase):
    def setUp(self):
        user = User.objects.create(username="Test", password="Forms")
        user2 = User.objects.create(username="Test2", password="Forms2")
        clan = Clan.objects.create(name="TestClan", maxMembers=10, clanMaster=user)
        clan2 = Clan.objects.create(name="TestClan2", maxMembers=10, clanMaster=user2)
        user.clan = clan
        user.save()
        user2.clan = clan2
        user2.save()
        war = War.objects.create(allyClan=clan, enemyClanName=clan2.name, date=timezone.now())
        aus = UserSnapshot.objects.create(username="Test", isAlly=True, war=war)
        eus = UserSnapshot.objects.create(username="Test2", isAlly=False, war=war)
        self.battle = Battle.objects.create(ally=aus, enemy=eus, war=war)

    def test_custom_user_creation_valid_form(self):
        form = CustomUserCreationForm(data={
            "username": "TestT",
            "password1": "FormsTests",
            "password2": "FormsTests"
        })
        self.assertTrue(form.is_valid())

    def test_custom_user_creation_no_data_form(self):
        form = CustomUserCreationForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 3)
    
    def test_custom_user_change_valid_form(self):
        form = CustomUserChangeForm(data={
            "username": "TestT",
            "clan": 1
        })
        self.assertTrue(form.is_valid())

        form = CustomUserChangeForm(data={
            "username": "TestT",
        })
        self.assertTrue(form.is_valid())

    def test_custom_user_change_no_data_form(self):
        form = CustomUserChangeForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)


    def test_clan_valid_form(self):
        form = ClanForm(data={
            "name": "TestClanT",
            "maxMembers": 30
        })
        self.assertTrue(form.is_valid())
    
    def test_clan_invalid_form(self):
        form = ClanForm(data={
            "name": "TestClanT",
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)
        
        form = ClanForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)

    def test_battle_valid_form(self):
        data = {
            "enemy": 2,
            "allyDestruction": 100,
            "enemyDestruction": 20,
            "allyVictory": True
        }
        form = BattleForm(data=data, instance=self.battle)
        self.assertTrue(form.is_valid())
    
    def test_battle_invalid_form(self):
        data = {
            "enemy": 5,
            "allyDestruction": 100,
            "enemyDestruction": 20,
            "allyVictory": True
        }
        form = BattleForm(data=data, instance=self.battle)
        self.assertFalse(form.is_valid())
        
        data = {
            "enemy": 2,
            "allyVictory": True
        }
        form = BattleForm(data=data, instance=self.battle)
        self.assertFalse(form.is_valid())

        form = BattleForm(data={}, instance=self.battle)
        self.assertFalse(form.is_valid())


    def test_battle_valid_form_master(self):
        data = {
            "ally": 1,
            "enemy": 2,
            "allyDestruction": 100,
            "enemyDestruction": 20,
            "allyVictory": True
        }
        form = BattleFormMaster(data=data, instance=self.battle)
        self.assertTrue(form.is_valid())

    def test_battle_invalid_form_master(self):
        data = {
            "enemy": 2,
            "allyDestruction": 100,
            "enemyDestruction": 20,
            "allyVictory": True
        }
        form = BattleFormMaster(data=data, instance=self.battle)
        self.assertFalse(form.is_valid())
        
        data = {
            "ally": 1,
            "enemy": 100,
            "allyDestruction": 100,
            "enemyDestruction": 20,
        }
        form = BattleFormMaster(data=data, instance=self.battle)
        self.assertFalse(form.is_valid())
        
        data = {
            "ally": 100,
            "enemy": 2,
            "allyDestruction": 100,
            "enemyDestruction": 20,
        }
        form = BattleFormMaster(data=data, instance=self.battle)
        self.assertFalse(form.is_valid())

        form = BattleFormMaster(data={}, instance=self.battle)
        self.assertFalse(form.is_valid())