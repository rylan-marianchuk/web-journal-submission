from django.test import TestCase
from .models import Journal
from users.models import Profile
from django.contrib.auth.models import User
# Create your tests here.


class TestModel(TestCase):

    def setUp(self):
        self.u1 = User.objects.create(username='Editor_test', password='Pyyzxxswrd23409q', email='editor@email.com' )
        self.up1 = Profile.objects.create(user=self.u1)


    def create_journal(self, title='Machine Learning', subject='computation'):
        return Journal.objects.create(title=title, subject=subject)

    def test_create_journal(self):
        journal = self.create_journal()
        self.assertTrue(isinstance(journal, Journal))
        self.assertEquals(journal.__str__(),  journal.title)


    def tearDown(self):
        self.u1.delete()
        self.up1.delete()