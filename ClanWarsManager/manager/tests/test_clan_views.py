from django.test import TestCase, Client
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from ..views.clans import ClanJoinView
from manager.models import War, User, Clan, UserSnapshot, Battle
from django.utils.http import urlencode
from django.core.exceptions import PermissionDenied

class TestClanViews(TestCase):
    def setUp(self):
        self.client = Client()
        User.objects.create_user(username="TestN", password="ViewsN")
        self.user = User.objects.create_user(username="Test", password="Views")
        user2 = User.objects.create_user(username="Test2", password="Views2")
        user3 = User.objects.create_user(username="Test3", password="Views3")
        user4 = User.objects.create_user(username="Test4", password="Views4")
        clan = Clan.objects.create(name="ClanTest", maxMembers=10, clanMaster=self.user)
        clan2 = Clan.objects.create(name="ClanTest2", maxMembers=10, clanMaster=user2)
        clan3 = Clan.objects.create(name="ClanTest3", maxMembers=10, clanMaster=user3)
        self.user.clan = clan
        self.user.save()
        user2.clan = clan2
        user6 = User.objects.create_user(username="Test6", password="Views6")
        user6.clan = clan2
        user6.save()
        user5 = User.objects.create_user(username="Test5", password="Views5")
        user5.clan = clan2
        user5.save()
        user2.save()
        user3.clan = clan3
        user3.save()

    def test_clan_list(self):
        #unlogged clans view
        clanListUrl = reverse("clans_list")
        response = self.client.get(clanListUrl)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "clans/list.html")

        #logged clans view
        clanListUrl = reverse("clans_list")
        login = self.client.login(username="Test", password="Views")
        self.assertTrue(login)
        response = self.client.get(clanListUrl)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "clans/list.html")
        self.client.logout()

    def test_clan_members_list_not_logged(self):
        response = self.client.post(reverse("clans_details", args=[1]))
        self.assertEqual(response.status_code, 405)

    def test_clan_members_list_logged(self):
        login = self.client.login(username="Test", password="Views")
        self.assertTrue(login)
        response = self.client.post(reverse("clans_details", args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "clans/update.html")


    def test_clan_join(self):
        login = self.client.login(username="Test4", password="Views4")
        self.assertTrue(login)
        clan = Clan.objects.get(name="ClanTest")
        lenght = len((User.objects.filter(clan=clan)))
        #query = urlencode({'joined': True})
        response = self.client.post(reverse("clans_join", args=[1]))
        self.assertEqual(len((User.objects.filter(clan=Clan.objects.get(name="ClanTest")))), lenght+1)

    def test_clan_leave(self):
        login = self.client.login(username="Test4", password="Views4")
        self.assertTrue(login)
        clan = Clan.objects.get(name="ClanTest")
        #query = urlencode({'joined': True})
        response = self.client.post(reverse("clans_join", args=[1]))
        lenght = len((User.objects.filter(clan=clan)))
        query = urlencode({'leaved': True})
        response = self.client.post(reverse("clans_leave"))
        self.assertEqual(len((User.objects.filter(clan=Clan.objects.get(name="ClanTest")))), lenght - 1)

    def test_delete_clan_isCM(self):
        login = self.client.login(username="Test", password="Views")
        self.assertTrue(login)
        clan = Clan.objects.get(name="ClanTest")
        clans = len(Clan.objects.all())
        response = self.client.post(reverse("clans_delete"))
        self.assertEqual(len(Clan.objects.all()),clans-1)

    def test_delete_clan_isNotCM(self):
        login = self.client.login(username="Test4", password="Views4")
        self.assertTrue(login)
        clan = Clan.objects.get(name="ClanTest")
        clans = len(Clan.objects.all())
        response = self.client.post(reverse("clans_delete"))
        self.assertEqual(len(Clan.objects.all()),clans)

    def test_kick_member_same_clan_as_CM(self):
        login = self.client.login(username="Test2", password="Views2")
        self.assertTrue(login)
        clan = Clan.objects.get(name="ClanTest2")
        members = len(User.objects.filter(clan=clan))
        response = self.client.post(reverse("clans_kick", args=["Test5"]))
        self.assertEqual(len(User.objects.filter(clan=clan)), members-1)

    def test_kick_member_same_clan_not_CM(self):
        login = self.client.login(username="Test5", password="Views5")
        self.assertTrue(login)
        clan = Clan.objects.get(name="ClanTest2")
        members = len(User.objects.filter(clan=clan))
        response = self.client.post(reverse("clans_kick", args=["Test6"]))
        self.assertEqual(response.status_code, 403)
        self.assertEqual(len(User.objects.filter(clan=clan)), members)

    def test_kick_member_not_same_clan_as_CM(self):
        login = self.client.login(username="Test2", password="Views2")
        self.assertTrue(login)
        clan = Clan.objects.get(name="ClanTest2")
        members = len(User.objects.filter(clan=clan))
        response = self.client.post(reverse("clans_kick", args=["Test1"]))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(len(User.objects.filter(clan=clan)), members)

    def test_kick_member_not_same_clan_not_CM(self):
        login = self.client.login(username="Test4", password="Views4")
        self.assertTrue(login)
        clan = Clan.objects.get(name="ClanTest2")
        members = len(User.objects.filter(clan=clan))
        response = self.client.post(reverse("clans_kick", args=["Test1"]))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(len(User.objects.filter(clan=clan)), members)


