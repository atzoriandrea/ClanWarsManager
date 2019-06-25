from django.test import TestCase, Client
from manager.models import User, Clan, War, Battle, UserSnapshot
from django.urls import reverse
from django.utils import timezone

class TestAcceptance(TestCase):
    def setUp(self):
        #Client
        self.client = Client()
        #User with no clan
        self.uN = User.objects.create_user(username="TestN", password="TestAcceptanceN")
        #Users
        self.u1 = User.objects.create_user(username="Test1", password="TestAcceptance1")
        self.u2 = User.objects.create_user(username="Test2", password="TestAcceptance2")
        self.u3 = User.objects.create_user(username="Test3", password="TestAcceptance3")
        self.u4 = User.objects.create_user(username="Test4", password="TestAcceptance4")
        #Clans
        self.c1 = Clan.objects.create(name="TestClan", clanMaster=self.u1)
        self.c2 = Clan.objects.create(name="TestClan2", maxMembers=1, clanMaster=self.u2)
        self.u1.clan = self.c1
        self.u1.save()
        self.u2.clan = self.c2
        self.u2.save()
        self.u4.clan = self.c1
        self.u4.save()
        #Wars

    def test_acceptance_login_valid_data(self):
        #login with valid data
        loginUrl = reverse("user_login")
        data = {
            "username": "Test1",
            "password": "TestAcceptance1"
        }
        response = self.client.post(loginUrl, data=data)
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed("home/homepage.html")
        response = self.client.get(loginUrl)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("registration/login.html")
    
    def test_acceptance_login_invalid_data(self):
        #login with invalid data
        loginUrl = reverse("user_login")
        data = {
            "username": "Test2",
            "password": "TestAcceptance1"
        }
        response = self.client.post(loginUrl, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("registration/login.html")
        response = self.client.get(loginUrl)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("registration/login.html")

    def test_acceptance_clan_list(self):
        #unlogged clans view
        clanListUrl = reverse("clans_list")
        response = self.client.get(clanListUrl)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("clans/list.html")

        #logged with no clan view
        login = self.client.login(username="TestN", password="TestAcceptanceN")
        self.assertTrue(login)
        response = self.client.get(clanListUrl)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("clans/list.html")
        self.client.logout()

        #logged clans view
        login = self.client.login(username="Test1", password="TestAcceptance1")
        self.assertTrue(login)
        response = self.client.get(clanListUrl)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("clans/list.html")
        self.client.logout()
    
    def test_acceptance_clan_details(self):
        #unlogged clans view
        clanDetailsUrl = reverse("clans_details", kwargs={"pk": 1})
        response = self.client.get(clanDetailsUrl)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("clans/details.html")
        
        #logged with no clan view
        login = self.client.login(username="TestN", password="TestAcceptanceN")
        clanDetailsUrl = reverse("clans_details", kwargs={"pk": 1})
        response = self.client.get(clanDetailsUrl)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("clans/details.html")
        self.client.logout()

        #logged clan member view 
        login = self.client.login(username="Test4", password="TestAcceptance4")
        self.assertTrue(login)
        response = self.client.get(clanDetailsUrl)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("clans/details.html")
        self.client.logout()

        #logged clan master view 
        login = self.client.login(username="Test1", password="TestAcceptance1")
        self.assertTrue(login)
        response = self.client.get(clanDetailsUrl)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("clans/update.html")
        self.client.logout()

    def test_acceptance_clan_create_no_clan(self):
        #logged user with no clan create view
        clanCreateUrl = reverse("clans_create")
        login = self.client.login(username="TestN", password="TestAcceptanceN") 
        self.assertTrue(login)
        response = self.client.post(clanCreateUrl)
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed("clans/update.html")
        response = self.client.get(clanCreateUrl)
        self.assertEqual(response.status_code, 405)

        self.uN.refresh_from_db()
        newClan = Clan.objects.get(id=3)
        self.assertIsNotNone(self.uN.clan)
        self.assertEqual(self.uN.clan, newClan)
        self.assertEqual(newClan.clanMaster, self.uN)
        self.client.logout()

    def test_acceptance_clan_create_no_login(self):
        #unlogged user create view
        clanCreateUrl = reverse("clans_create")
        response = self.client.get(clanCreateUrl)
        self.assertEqual(response.status_code, 302)
        response = self.client.post(clanCreateUrl)
        self.assertEqual(response.status_code, 302)

    def test_acceptance_clan_create_with_clan(self):
        #logged user with clan create view
        clanCreateUrl = reverse("clans_create")
        login = self.client.login(username="Test1", password="TestAcceptance1") 
        self.assertTrue(login)
        clan = self.u1.clan
        response = self.client.post(clanCreateUrl)
        self.assertEqual(response.status_code, 403)
        self.u1.refresh_from_db()
        self.assertEqual(self.u1.clan, clan)
        self.assertEqual(clan.clanMaster, self.u1)
        self.client.logout()

    def test_acceptance_clan_join(self):
        #logged user with no clan join view
        clanJoinUrl = reverse("clans_join", kwargs={"pk": 1})
        login = self.client.login(username="TestN", password="TestAcceptanceN")
        self.assertTrue(login)
        clanMembers = User.objects.filter(clan=self.c1).count()
        response = self.client.post(clanJoinUrl)
        self.assertEqual(response.status_code, 302)
        updateClanMembers = User.objects.filter(clan=self.c1).count()
        self.uN.refresh_from_db()
        self.assertEqual(self.uN.clan, self.c1)
        self.assertEqual(updateClanMembers, clanMembers+1)
        self.client.logout()
        
        #logged user with clan join view
        login = self.client.login(username="Test2", password="TestAcceptance2")
        self.assertTrue(login)
        clanMembers = User.objects.filter(clan=self.c1).count()
        response = self.client.post(clanJoinUrl)
        self.assertEqual(response.status_code, 403)
        updateClanMembers = User.objects.filter(clan=self.c1).count()
        self.assertNotEqual(self.u2.clan, self.c1)
        self.assertEqual(updateClanMembers, clanMembers)
        self.client.logout()

        #unlogged user join view
        response = self.client.get(clanJoinUrl)
        self.assertEqual(response.status_code, 302)
        response = self.client.post(clanJoinUrl)
        self.assertEqual(response.status_code, 302)
    
    def test_acceptance_clan_join_max_members(self):
        #join clan with max members view
        clanJoinUrl = reverse("clans_join", kwargs={"pk": 2})
        login = self.client.login(username="TestN", password="TestAcceptanceN")
        self.assertTrue(login)
        clanMembers = User.objects.filter(clan=self.c2).count()
        response = self.client.post(clanJoinUrl)
        self.assertEqual(response.status_code, 403)
        updateClanMembers = User.objects.filter(clan=self.c2).count()
        self.assertIsNone(self.uN.clan)
        self.assertEqual(updateClanMembers, clanMembers)
        self.client.logout()

    def test_acceptance_clan_leave_as_member(self):
        #logged member leave view
        clanLeaveUrl = reverse("clans_leave")
        login = self.client.login(username="Test4", password="TestAcceptance4")
        self.assertTrue(login)
        clanMembers = User.objects.filter(clan=self.u4.clan).count()
        response = self.client.post(clanLeaveUrl)
        self.assertEqual(response.status_code, 302)
        updateClanMembers = User.objects.filter(clan=self.u4.clan).count()
        self.u4.refresh_from_db()
        self.assertIsNone(self.u4.clan)
        self.assertEqual(updateClanMembers, clanMembers - 1)
        self.client.logout()
        
        #unlogged user leave view
        response = self.client.get(clanLeaveUrl)
        self.assertEqual(response.status_code, 302)
        response = self.client.post(clanLeaveUrl)
        self.assertEqual(response.status_code, 302)
    
    def test_acceptance_clan_leave_as_cm(self):
        #logged clan master leave view
        clanLeaveUrl = reverse("clans_leave")
        login = self.client.login(username="Test1", password="TestAcceptance1")
        self.assertTrue(login)
        response = self.client.post(clanLeaveUrl)
        self.assertEqual(response.status_code, 403)
        self.assertIsNotNone(self.u1.clan)
        self.client.logout()

    def test_acceptance_clan_delete_as_cm(self):
        #logged clan master delete view
        clanDeleteUrl = reverse("clans_delete")
        login = self.client.login(username="Test1", password="TestAcceptance1")
        self.assertTrue(login)
        clan = self.u1.clan
        response = self.client.post(clanDeleteUrl)
        self.assertEqual(response.status_code, 302)
        self.u1.refresh_from_db()
        self.u4.refresh_from_db()
        self.assertIsNone(self.u1.clan)
        self.assertIsNone(self.u4.clan)
        self.assertFalse(Clan.objects.filter(id=clan.id).exists())
        self.client.logout()
    
    def test_acceptance_clan_delete_as_member(self):
        #logged member delete view
        clanDeleteUrl = reverse("clans_delete")
        login = self.client.login(username="Test4", password="TestAcceptance4")
        self.assertTrue(login)
        clan = self.u4.clan
        response = self.client.post(clanDeleteUrl)
        self.assertEqual(response.status_code, 403)
        self.u4.refresh_from_db()
        clan.refresh_from_db()
        self.assertIsNotNone(self.u4.clan)
        self.assertIsNotNone(clan)
        self.client.logout()

        #unlogged user delete view
        response = self.client.get(clanDeleteUrl)
        self.assertEqual(response.status_code, 302)
        response = self.client.post(clanDeleteUrl)
        self.assertEqual(response.status_code, 302)

    def test_acceptance_clan_kick_member_in_clan_as_cm(self):
        #logget clan master kick member view 
        clanKickUrl = reverse("clans_kick", kwargs={"username": "Test4"})
        login = self.client.login(username="Test1", password="TestAcceptance1")
        self.assertTrue(login)
        clanMembers = User.objects.filter(clan=self.u4.clan).count()
        response = self.client.post(clanKickUrl)
        self.assertEqual(response.status_code, 302)
        updatedClanMembers = User.objects.filter(clan=self.u4.clan).count()
        self.u4.refresh_from_db()
        self.assertIsNone(self.u4.clan)
        self.assertEqual(updatedClanMembers, clanMembers - 1)
        self.client.logout()

    def test_acceptance_clan_kick_member_as_member(self):
        #logged member kick clan master view
        clanKickUrl = reverse("clans_kick", kwargs={"username": "Test1"})
        login = self.client.login(username="Test4", password="TestAcceptance4")
        self.assertTrue(login)
        clanMembers = User.objects.filter(clan=self.u1.clan).count()
        response = self.client.post(clanKickUrl)
        self.assertEqual(response.status_code, 403)
        updatedClanMembers = User.objects.filter(clan=self.u1.clan).count()
        self.u1.refresh_from_db()
        self.assertIsNotNone(self.u1.clan)
        self.assertEqual(updatedClanMembers, clanMembers)
        self.client.logout()
        
        #logged clan master kick other clan master view
        clanKickUrl = reverse("clans_kick", kwargs={"username": "Test2"})
        login = self.client.login(username="Test1", password="TestAcceptance1")
        self.assertTrue(login)
        response = self.client.post(clanKickUrl)
        self.assertEqual(response.status_code, 403)
        self.u2.refresh_from_db()
        self.assertIsNotNone(self.u2.clan)
        self.client.logout()

        #unlogged user kick view
        response = self.client.get(clanKickUrl)
        self.assertEqual(response.status_code, 302)
        response = self.client.post(clanKickUrl)
        self.assertEqual(response.status_code, 302)


        '''
        L’utente autenticato nel sistema e capo del suo clan, deve poter creare una guerra con un altro clan già esistente.
        Deve, quindi, poter registrare battaglie, decidendo per ognuna
        il membro alleato e quello nemico da far sfidare, le loro percentuali di distruzione e l’esito della singola battaglia.
        '''
    def test_acceptance_war_create_as_cm(self):
        warCreateUrl = reverse('clans_fight', kwargs={'pk': self.c2.pk})
        login = self.client.login(username="Test1", password="TestAcceptance1")
        self.assertTrue(login)
        wars = War.objects.filter(allyClan=self.u1.clan).count()
        response = self.client.post(warCreateUrl)
        self.assertEqual(response.status_code, 302)
        warsAfterCreation = War.objects.filter(allyClan=self.u1.clan).count()
        war = War.objects.get(allyClan=self.u1.clan)
        self.assertIsNotNone(war)
        self.assertEqual(wars+1, warsAfterCreation)
        battleCreateUrl = reverse('wars_addbattle', kwargs={'pk': war.pk})
        response = self.client.post(battleCreateUrl)
        self.assertEqual(response.status_code, 302)
        battle = Battle.objects.get(war=war)
        battle.ally = UserSnapshot.objects.create(username=self.c1.clanMaster.username, isAlly=True, war=war)
        battle.enemy = UserSnapshot.objects.create(username=self.c2.clanMaster.username, isAlly=False, war=war)
        battle.allyDestruction = 50
        battle.enemyDestruction = 80
        self.assertEqual(battle.enemy.username, self.c2.clanMaster.username)
        self.assertEqual(battle.allyDestruction, 50)
        self.assertEqual(battle.enemyDestruction, 80)
        battle.allyVictory = False
        self.assertFalse(battle.allyVictory)

















