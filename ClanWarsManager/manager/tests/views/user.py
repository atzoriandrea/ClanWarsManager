from django.test import TestCase, Client
from django.urls import reverse
from manager.models import User

class TestUserViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="Test", password="Views")

    #SignupView Tests
    def test_signup(self):
        signUpUrl = reverse("user_signup")
        login = self.client.login(username="Test", password="Views") 
        self.assertTrue(login)
        response = self.client.get(signUpUrl)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "user/signup.html")
        self.client.logout()

        response = self.client.get(signUpUrl)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "user/signup.html")
        response = self.client.post(signUpUrl)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "user/signup.html")