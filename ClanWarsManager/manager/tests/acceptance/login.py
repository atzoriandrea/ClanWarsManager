from django.test import TestCase, Client
from manager.models import User
from django.urls import reverse

"""
L’utente deve potersi autenticare nel sistema, inserendo il proprio nome utente e la propria password.
Se le credenziali non sono corrette, deve invece visualizzare un errore.
"""

class TestAcceptanceLogin(TestCase):
    def setUp(self):
        #Client
        self.client = Client()
        #Users
        User.objects.create_user(username="Test1", password="TestAcceptance1")

    #Login with valid credentials
    def test_acceptance_login_valid_data(self):
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
    
    #Login with invalid credentials
    def test_acceptance_login_invalid_data(self):
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