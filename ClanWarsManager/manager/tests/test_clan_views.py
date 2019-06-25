from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from manager.models import War, User, Clan, UserSnapshot, Battle

class TestClanViews(TestCase):
    def setUp(self):
        self.client = Client()
        user = User.objects.create_user(username="Test", password="Views")
        user2 = User.objects.create_user(username="Test2", password="Views2")
        user3 = User.objects.create_user(username="Test3", password="Views3")
        user4 = User.objects.create_user(username="Test4", password="Views4")
        user5 = User.objects.create_user(username="Test5", password="Views5")
        User.objects.create_user(username="Test6", password="Views6")
        clan = Clan.objects.create(name="ClanTest", maxMembers=10, clanMaster=user)
        clan2 = Clan.objects.create(name="ClanTest2", maxMembers=10, clanMaster=user2)
        clan3 = Clan.objects.create(name="ClanTest3", maxMembers=1, clanMaster=user3)
        user.clan = clan
        user.save()
        user2.clan = clan2
        user2.save()
        user3.clan = clan3
        user3.save()
        user4.clan = clan
        user4.save()
        user5.clan = clan2
        user5.save()

    #ClanListView Tests
    def test_clan_list(self):
        #unlogged clans view
        clanListUrl = reverse("clans_list")
        response = self.client.get(clanListUrl)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "clans/list.html")

        #logged clans view
        login = self.client.login(username="Test", password="Views")
        self.assertTrue(login)
        response = self.client.get(clanListUrl)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "clans/list.html")
        self.client.logout()

    #ClanDetailsDispatcherView Tests
    def test_clan_details(self):
        clanDetailsUrl = reverse("clans_details", kwargs={"pk": 1})
        response = self.client.get(clanDetailsUrl)
        self.assertEqual(response.status_code, 200)

        login = self.client.login(username="Test", password="Views")
        self.assertTrue(login)
        response = self.client.post(clanDetailsUrl)
        self.assertEqual(response.status_code, 200)
        response = self.client.get(clanDetailsUrl)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "clans/update.html")
        self.client.logout()

        login = self.client.login(username="Test4", password="Views4")
        self.assertTrue(login)
        response = self.client.post(clanDetailsUrl)
        self.assertEqual(response.status_code, 405)
        response = self.client.get(clanDetailsUrl)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "clans/details.html")
        self.client.logout()

    #ClanJoinView Tests
    def test_clan_join_valid_data(self):
        clanJoinUrl = reverse("clans_join", kwargs={"pk": 1})
        login = self.client.login(username="Test6", password="Views6")
        self.assertTrue(login)
        clan = Clan.objects.get(id=1)
        clanMembers = User.objects.filter(clan=clan).count()
        response = self.client.post(clanJoinUrl)
        self.assertEqual(response.status_code, 302)
        user = User.objects.get(username="Test6")
        updateClanMembers = User.objects.filter(clan=clan).count()
        self.assertEqual(user.clan, clan)
        self.assertEqual(updateClanMembers, clanMembers+1)
        self.client.logout()

        response = self.client.get(clanJoinUrl)
        self.assertEqual(response.status_code, 302)
        response = self.client.post(clanJoinUrl)
        self.assertEqual(response.status_code, 302)
        
    def test_clan_join_invalid_data(self):
        clanJoinUrl = reverse("clans_join", kwargs={"pk": 100})
        login = self.client.login(username="Test6", password="Views6")
        self.assertTrue(login)
        response = self.client.post(clanJoinUrl)
        self.assertEqual(response.status_code, 404)
        user = User.objects.get(username="Test6")
        self.assertIsNone(user.clan)
        self.client.logout()
    
    def test_clan_join_max_members(self):
        clanJoinUrl = reverse("clans_join", kwargs={"pk": 3})
        login = self.client.login(username="Test6", password="Views6")
        self.assertTrue(login)
        clan = Clan.objects.get(id=3)
        clanMembers = User.objects.filter(clan=clan).count()
        response = self.client.post(clanJoinUrl)
        self.assertEqual(response.status_code, 403)
        user = User.objects.get(username="Test6")
        updateClanMembers = User.objects.filter(clan=clan).count()
        self.assertIsNone(user.clan)
        self.assertEqual(updateClanMembers, clanMembers)
        self.client.logout()
    
    def test_clan_join_already_in_clan(self):
        clanJoinUrl = reverse("clans_join", kwargs={"pk": 1})
        login = self.client.login(username="Test5", password="Views5")
        self.assertTrue(login)
        clan = Clan.objects.get(id=1)
        clanMembers = User.objects.filter(clan=clan).count()
        response = self.client.post(clanJoinUrl)
        self.assertEqual(response.status_code, 403)
        user = User.objects.get(username="Test5")
        updateClanMembers = User.objects.filter(clan=clan).count()
        self.assertNotEqual(user.clan, clan)
        self.assertEqual(updateClanMembers, clanMembers)
        self.client.logout()

        login = self.client.login(username="Test4", password="Views4")
        self.assertTrue(login)
        clan = Clan.objects.get(id=1)
        clanMembers = User.objects.filter(clan=clan).count()
        response = self.client.post(clanJoinUrl)
        self.assertEqual(response.status_code, 403)
        user = User.objects.get(username="Test4")
        updateClanMembers = User.objects.filter(clan=clan).count()
        self.assertEqual(user.clan, clan)
        self.assertEqual(updateClanMembers, clanMembers)
        self.client.logout()

    #ClanLeaveiew Tests
    def test_clan_leave_as_member(self):
        clanLeaveUrl = reverse("clans_leave")
        login = self.client.login(username="Test4", password="Views4")
        self.assertTrue(login)
        user = User.objects.get(username="Test4")
        clanMembers = User.objects.filter(clan=user.clan).count()
        response = self.client.post(clanLeaveUrl)
        self.assertEqual(response.status_code, 302)
        updateClanMembers = User.objects.filter(clan=user.clan).count()
        user.refresh_from_db()
        self.assertIsNone(user.clan)
        self.assertEqual(updateClanMembers, clanMembers - 1)
        self.client.logout()

        response = self.client.get(clanLeaveUrl)
        self.assertEqual(response.status_code, 302)
        response = self.client.post(clanLeaveUrl)
        self.assertEqual(response.status_code, 302)
    
    def test_clan_leave_as_cm(self):
        clanLeaveUrl = reverse("clans_leave")
        login = self.client.login(username="Test3", password="Views3")
        self.assertTrue(login)
        user = User.objects.get(username="Test3")
        response = self.client.post(clanLeaveUrl)
        self.assertEqual(response.status_code, 403)
        self.assertIsNotNone(user.clan)
        self.client.logout()
    
    def test_clan_leave_no_clan(self):
        clanLeaveUrl = reverse("clans_leave")
        login = self.client.login(username="Test6", password="Views6")
        self.assertTrue(login)
        user = User.objects.get(username="Test6")
        response = self.client.post(clanLeaveUrl)
        self.assertEqual(response.status_code, 403)
        self.assertIsNone(user.clan)
        self.client.logout()

    #ClanDeleteView Tests
    def test_clan_delete_as_member(self):
        clanDeleteUrl = reverse("clans_delete")
        login = self.client.login(username="Test4", password="Views4")
        self.assertTrue(login)
        user = User.objects.get(username="Test4")
        clan = user.clan
        response = self.client.post(clanDeleteUrl)
        self.assertEqual(response.status_code, 403)
        user.refresh_from_db()
        clan.refresh_from_db()
        self.assertIsNotNone(user.clan)
        self.assertIsNotNone(clan)
        self.client.logout()

        response = self.client.get(clanDeleteUrl)
        self.assertEqual(response.status_code, 302)
        response = self.client.post(clanDeleteUrl)
        self.assertEqual(response.status_code, 302)
    
    def test_clan_delete_as_cm(self):
        clanDeleteUrl = reverse("clans_delete")
        login = self.client.login(username="Test2", password="Views2")
        self.assertTrue(login)
        cm = User.objects.get(username="Test2")
        clan = cm.clan
        member = User.objects.get(username="Test5")
        response = self.client.post(clanDeleteUrl)
        self.assertEqual(response.status_code, 302)
        cm.refresh_from_db()
        member.refresh_from_db()
        self.assertIsNone(cm.clan)
        self.assertIsNone(member.clan)
        self.assertFalse(Clan.objects.filter(id=clan.id).exists())
        self.client.logout()
    
    def test_clan_delete_no_clan(self):
        clanDeleteUrl = reverse("clans_delete")
        login = self.client.login(username="Test6", password="Views6")
        self.assertTrue(login)
        user = User.objects.get(username="Test6")
        response = self.client.post(clanDeleteUrl)
        self.assertEqual(response.status_code, 403)
        self.assertIsNone(user.clan)
        self.client.logout()


    #ClanKickView Tests
    def test_clan_kick_member_in_clan_as_cm(self):
        clanKickUrl = reverse("clans_kick", kwargs={"username": "Test4"})
        login = self.client.login(username="Test", password="Views")
        self.assertTrue(login)
        user = User.objects.get(username="Test4")
        clanMembers = User.objects.filter(clan=user.clan).count()
        response = self.client.post(clanKickUrl)
        self.assertEqual(response.status_code, 302)
        updatedClanMembers = User.objects.filter(clan=user.clan).count()
        user.refresh_from_db()
        self.assertIsNone(user.clan)
        self.assertEqual(updatedClanMembers, clanMembers - 1)
        self.client.logout()

    def test_clan_kick_member_as_unauthorized_user(self):
        clanKickUrl = reverse("clans_kick", kwargs={"username": "Test"})
        login = self.client.login(username="Test4", password="Views4")
        self.assertTrue(login)
        user = User.objects.get(username="Test")
        clanMembers = User.objects.filter(clan=user.clan).count()
        response = self.client.post(clanKickUrl)
        self.assertEqual(response.status_code, 403)
        updatedClanMembers = User.objects.filter(clan=user.clan).count()
        user.refresh_from_db()
        self.assertIsNotNone(user.clan)
        self.assertEqual(updatedClanMembers, clanMembers)
        self.client.logout()

        clanKickUrl = reverse("clans_kick", kwargs={"username": "Test2"})
        login = self.client.login(username="Test4", password="Views4")
        self.assertTrue(login)
        user = User.objects.get(username="Test2")
        response = self.client.post(clanKickUrl)
        self.assertEqual(response.status_code, 403)
        user.refresh_from_db()
        self.assertIsNotNone(user.clan)
        self.client.logout()

        clanKickUrl = reverse("clans_kick", kwargs={"username": "Test2"})
        login = self.client.login(username="Test", password="Views")
        self.assertTrue(login)
        user = User.objects.get(username="Test2")
        response = self.client.post(clanKickUrl)
        self.assertEqual(response.status_code, 403)
        user.refresh_from_db()
        self.assertIsNotNone(user.clan)
        self.client.logout()
        
        clanKickUrl = reverse("clans_kick", kwargs={"username": "Test2"})
        login = self.client.login(username="Test6", password="Views6")
        self.assertTrue(login)
        user = User.objects.get(username="Test2")
        response = self.client.post(clanKickUrl)
        self.assertEqual(response.status_code, 403)
        user.refresh_from_db()
        self.assertIsNotNone(user.clan)
        self.client.logout()

        response = self.client.get(clanKickUrl)
        self.assertEqual(response.status_code, 302)
        response = self.client.post(clanKickUrl)
        self.assertEqual(response.status_code, 302)

    #ClanUpdateView Tests
    def test_clan_update_as_cm(self):
        clanUpdateUrl = reverse("clans_update")
        login = self.client.login(username="Test", password="Views") 
        self.assertTrue(login)
        clan = Clan.objects.get(id=1)
        data = {
            "name": "TestUpdate",
            "maxMembers": 40
        }
        response = self.client.post(clanUpdateUrl, data=data)
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed("clans/update.html")
        clan.refresh_from_db()
        self.assertEqual(clan.name, "TestUpdate")
        self.assertEqual(clan.maxMembers, 40)
        self.client.logout()

        response = self.client.get(clanUpdateUrl)
        self.assertEqual(response.status_code, 302)
        response = self.client.post(clanUpdateUrl)
        self.assertEqual(response.status_code, 302)

    def test_clan_update_as_member(self):
        clanUpdateUrl = reverse("clans_update")
        login = self.client.login(username="Test4", password="Views4") 
        self.assertTrue(login)
        clan = Clan.objects.get(id=1)
        data = {
            "name": "TestUpdate",
            "maxMembers": 40
        }
        response = self.client.post(clanUpdateUrl, data=data)
        self.assertEqual(response.status_code, 403)
        clan.refresh_from_db()
        self.assertNotEqual(clan.name, "TestUpdate")
        self.assertNotEqual(clan.maxMembers, 40)
        self.client.logout()

    def test_clan_update_no_clan(self):
        clanUpdateUrl = reverse("clans_update")
        login = self.client.login(username="Test6", password="Views6") 
        self.assertTrue(login)
        response = self.client.post(clanUpdateUrl)
        self.assertEqual(response.status_code, 403)
        self.client.logout()

    #ClanCreateView Tests
    def test_clan_create_no_clan(self):
        clanCreateUrl = reverse("clans_create")
        login = self.client.login(username="Test6", password="Views6") 
        self.assertTrue(login)
        user = User.objects.get(username="Test6")
        response = self.client.post(clanCreateUrl)
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed("clans/update.html")
        user.refresh_from_db()
        newClan = Clan.objects.get(id=4)
        self.assertIsNotNone(user.clan)
        self.assertEqual(user.clan, newClan)
        self.assertEqual(newClan.clanMaster, user)
        self.client.logout()

        response = self.client.get(clanCreateUrl)
        self.assertEqual(response.status_code, 302)
        response = self.client.post(clanCreateUrl)
        self.assertEqual(response.status_code, 302)

    def test_clan_create_with_clan(self):
        clanCreateUrl = reverse("clans_create")
        login = self.client.login(username="Test", password="Views") 
        self.assertTrue(login)
        user = User.objects.get(username="Test")
        clan = Clan.objects.get(id=1)
        response = self.client.post(clanCreateUrl)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(user.clan, clan)
        self.assertEqual(clan.clanMaster, user)
        self.client.logout()

        login = self.client.login(username="Test4", password="Views4") 
        self.assertTrue(login)
        user = User.objects.get(username="Test4")
        clan = Clan.objects.get(id=1)
        response = self.client.post(clanCreateUrl)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(user.clan, clan)
        self.client.logout()