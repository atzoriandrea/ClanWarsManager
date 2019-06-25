from django.test import SimpleTestCase
from django.urls import reverse, resolve
from ..views import battles, clans, home, user, wars
from django.contrib.auth import views as auth_views
class TestUrls(SimpleTestCase):

    #User urls tests
    def test_user_urls_are_resolved(self):
        url = reverse("user_signup")
        self.assertEqual(resolve(url).func.view_class, user.SignupView)
        url = reverse("user_login")
        self.assertEqual(resolve(url).func.view_class, auth_views.LoginView)
        url = reverse("user_logout")
        self.assertEqual(resolve(url).func.view_class, auth_views.LogoutView)

    #Battle urls tests
    def test_battles_urls_are_resolved(self):
        url = reverse("battles_delete", kwargs={"pk": 1})
        self.assertEqual(resolve(url).func.view_class, battles.BattleDeleteView)
        url = reverse("battles_update", kwargs={"pk": 1})
        self.assertEqual(resolve(url).func.view_class, battles.BattleUpdateView)

    #War urls tests
    def test_wars_urls_are_resolved(self):
        url = reverse("wars_list")
        self.assertEqual(resolve(url).func.view_class, wars.WarListView)
        url = reverse("wars_details", kwargs={"pk": 1})
        self.assertEqual(resolve(url).func.view_class, wars.WarDetailView)
        url = reverse("wars_delete", kwargs={"pk": 1})
        self.assertEqual(resolve(url).func.view_class, wars.WarDeleteView)
        url = reverse("wars_addbattle", kwargs={"pk": 1})
        self.assertEqual(resolve(url).func.view_class, battles.BattleCreateView)

    #Clan urls tests
    def test_clans_urls_are_resolved(self):
        url = reverse("clans_list")
        self.assertEqual(resolve(url).func.view_class, clans.ClanListView)
        url = reverse("clans_details", kwargs={"pk": 1})
        self.assertEqual(resolve(url).func.view_class, clans.ClanDetailsDispatcherView)
        url = reverse("clans_fight", kwargs={"pk": 1})
        self.assertEqual(resolve(url).func.view_class, wars.WarCreateView)
        url = reverse("clans_join", kwargs={"pk": 1})
        self.assertEqual(resolve(url).func.view_class, clans.ClanJoinView)
        url = reverse("clans_delete")
        self.assertEqual(resolve(url).func.view_class, clans.ClanDeleteView)
        url = reverse("clans_update")
        self.assertEqual(resolve(url).func.view_class, clans.ClanUpdateView)
        url = reverse("clans_leave")
        self.assertEqual(resolve(url).func.view_class, clans.ClanLeaveView)
        url = reverse("clans_create")
        self.assertEqual(resolve(url).func.view_class, clans.ClanCreateView)
        url = reverse("clans_kick", kwargs={"username": "TestUsername"})
        self.assertEqual(resolve(url).func.view_class, clans.ClanKickView)
