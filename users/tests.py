from django.test import TestCase
from django.contrib.auth.models import User

# Create your tests here.
class TestModels(TestCase):

    def create_user(self, username="user1", password="Pxxswrd23409q", email="testuser@email.com"):
        return User.objects.create(username=username, password=password, email=email)

    def test_user_creation(self):
        user = self.create_user()
        self.assertTrue(isinstance(user, User))
        self.assertEquals(user.__str__(), user.username)

