from django.test import TestCase
from ..models import *
from django.utils import timezone
# Create your tests here.

class ClanTestCase(TestCase):
    def setUp(self):
        User.objects.create(username="ClanMaster",password="password")
        Clan.objects.create(name="TestClan",maxMembers=10,clanMaster=User.objects.get(username="ClanMaster"))
        cm = User.objects.get(username="ClanMaster")
        cm.clan = Clan.objects.get(name = "TestClan")
        cm.save()
        User.objects.create(username="Andrea", password="password",clan=Clan.objects.get(name = "TestClan"))
        User.objects.create(username="Nicola", password="password",clan=Clan.objects.get(name = "TestClan"))

    def test_clans_attr(self):
        clan = Clan.objects.get(name = "TestClan")
        self.assertEqual(clan.maxMembers, 10)
        cm = User.objects.get(username="ClanMaster")
        andrea = User.objects.get(username="Andrea")
        nicola = User.objects.get(username="Nicola")
        self.assertNotEqual(andrea,nicola)
        self.assertEqual(andrea.password, nicola.password)
        self.assertEqual(clan.clanMaster, cm)
        self.assertEqual(cm.clan , clan)

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
        cm = User.objects.get(username="ClanMaster2")
        cm.clan = Clan.objects.get(name="TestClan2")
        cm.save()
        User.objects.create(username="Davide", password="password", clan=Clan.objects.get(name="TestClan2"))
        User.objects.create(username="Francesco", password="password", clan=Clan.objects.get(name="TestClan2"))
        War.objects.create(allyClan=Clan.objects.get(name="TestClan"), enemyClanName="TestClan2", date=timezone.now())

    def test_war(self):
        guerra = War.objects.get(allyClan=Clan.objects.get(name="TestClan"), enemyClanName="TestClan2")
        self.assertIsNotNone(guerra)
        #self.assertEqual(len(guerra.allyClan.))

