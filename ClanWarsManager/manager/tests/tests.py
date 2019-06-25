from django.test import TestCase
from ..models import *
from django.utils import timezone
# Create your tests here.

class ClanTestCase(TestCase):
    def setUp(self):
        User.objects.create(username="ClanMaster",password="password")
        Clan.objects.create(name="TestClan", maxMembers=10, clanMaster=User.objects.get(username="ClanMaster"))
        cm = User.objects.get(username="ClanMaster")
        cm.clan = Clan.objects.get(name="TestClan")
        cm.save()
        User.objects.create(username="Andrea", password="password",clan=Clan.objects.get(name="TestClan"))
        User.objects.create(username="Nicola", password="password",clan=Clan.objects.get(name="TestClan"))

    def test_clans_attr(self):
        clan = Clan.objects.get(name="TestClan")
        self.assertEqual(clan.maxMembers, 10)
        cm = User.objects.get(username="ClanMaster")
        andrea = User.objects.get(username="Andrea")
        nicola = User.objects.get(username="Nicola")
        self.assertNotEqual(andrea, nicola)
        self.assertEqual(andrea.password, nicola.password)
        self.assertEqual(clan.clanMaster, cm)
        self.assertEqual(cm.clan, clan)

class WarTestCase(TestCase):
    def setUp(self):
        User.objects.create(username="ClanMaster", password="password")
        Clan.objects.create(name="TestClan", maxMembers=10, clanMaster=User.objects.get(username="ClanMaster"))
        cm = User.objects.get(username="ClanMaster")
        cm.clan = Clan.objects.get(name="TestClan")
        cm.save()
        User.objects.create(username="Andrea", password="password", clan=Clan.objects.get(name="TestClan"))
        User.objects.create(username="Nicola", password="password", clan=Clan.objects.get(name="TestClan"))
        User.objects.create(username="ClanMaster2", password="password")
        Clan.objects.create(name="TestClan2", maxMembers=10, clanMaster=User.objects.get(username="ClanMaster2"))
        cm2 = User.objects.get(username="ClanMaster2")
        cm2.clan = Clan.objects.get(name="TestClan2")
        cm2.save()
        User.objects.create(username="Davide", password="password", clan=Clan.objects.get(name="TestClan2"))
        User.objects.create(username="Francesco", password="password", clan=Clan.objects.get(name="TestClan2"))
        War.objects.create(allyClan=Clan.objects.get(name="TestClan"), enemyClanName="TestClan2", date=timezone.now())

    def test_war(self):
        guerra = War.objects.get(allyClan=Clan.objects.get(name="TestClan"), enemyClanName="TestClan2")
        self.assertIsNotNone(guerra)
        #self.assertEqual(len(guerra.allyClan.))


class SnapshotTestCase(TestCase):

    def setUp(self):
        User.objects.create(username="ClanMaster", password="password")
        Clan.objects.create(name="TestClan", maxMembers=10, clanMaster=User.objects.get(username="ClanMaster"))
        cm = User.objects.get(username="ClanMaster")
        cm.clan = Clan.objects.get(name="TestClan")
        cm.save()
        User.objects.create(username="Andrea", password="password", clan=Clan.objects.get(name="TestClan"))
        User.objects.create(username="Nicola", password="password", clan=Clan.objects.get(name="TestClan"))

        User.objects.create(username="ClanMaster2", password="password")
        Clan.objects.create(name="TestClan2", maxMembers=10, clanMaster=User.objects.get(username="ClanMaster2"))
        cm2 = User.objects.get(username="ClanMaster2")
        cm2.clan = Clan.objects.get(name="TestClan2")
        cm2.save()
        User.objects.create(username="Davide", password="password", clan=Clan.objects.get(name="TestClan2"))
        User.objects.create(username="Francesco", password="password", clan=Clan.objects.get(name="TestClan2"))
        War.objects.create(allyClan=Clan.objects.get(name="TestClan"), enemyClanName="TestClan2", date=timezone.now())

        for user in User.objects.filter(clan=Clan.objects.get("TestClan")):
            UserSnapshot.objects.create(username=user.username,isAlly=True, war=War.objects.get(allyClan=Clan.objects.get(name="TestClan"), enemyClanName="TestClan2"))

        for user in User.objects.filter(clan=Clan.objects.get("TestClan2")):
            UserSnapshot.objects.create(username=user.username,isAlly=False, war=War.objects.get(allyClan=Clan.objects.get(name="TestClan"), enemyClanName="TestClan2"))

    def snap_test(self):
        self.assertEqual(len(User.objects.filter(clan=Clan.objects.get("TestClan"))), len(UserSnapshot.objects.filter(isAlly=True)))
        self.assertEqual(len(User.objects.filter(clan=Clan.objects.get("TestClan2"))), len(UserSnapshot.objects.filter(isAlly=False)))



class BattleTestCase(TestCase):
    def setUp(self):

        # creating first user with his clan
        User.objects.create(username="ClanMaster", password="password")
        Clan.objects.create(name="TestClan", maxMembers=10, clanMaster=User.objects.get(username="ClanMaster"))
        cm = User.objects.get(username="ClanMaster")
        cm.clan = Clan.objects.get(name="TestClan")
        cm.save()
        # creating second user with his clan
        User.objects.create(username="ClanMaster2", password="password")
        Clan.objects.create(name="TestClan2", maxMembers=10, clanMaster=User.objects.get(username="ClanMaster2"))
        cm2 = User.objects.get(username="ClanMaster2")
        cm2.clan = Clan.objects.get(name="TestClan2")
        cm2.save()
        # Creating a war
        war = War.objects.create(allyClan=Clan.objects.get(name="TestClan"), enemyClanName="TestClan2", date=timezone.now())

    def test_battle(self):
        # Creating snapshots and battle.
        cm = User.objects.get(username="ClanMaster")
        cm2 = User.objects.get(username="ClanMaster2")
        war = War.objects.get(allyClan=Clan.objects.get(name="TestClan"), enemyClanName="TestClan2")
        allysnap = UserSnapshot.objects.create(username=cm.username, war=war, isAlly=False)
        self.assertIsNotNone(allysnap)
        enemysnap = UserSnapshot.objects.create(username=cm2.username, war=war, isAlly=False)
        self.assertIsNotNone(enemysnap)
        battle = Battle.objects.create(ally=allysnap, enemy=enemysnap, war=war)
        self.assertIsNotNone(battle)
        battle.allyDestruction = 50
        battle.enemyDestruction = 50
        battle.save()
        self.assertGreater(battle.allyDestruction, 49, "Giusto")
        self.assertLess(battle.enemyDestruction, 59, "Giusto")

