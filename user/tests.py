from django.test import TestCase,Client

class UserTest(TestCase):

    def loginTest(self):
        client=Client()
        result=client.login(username="admin",password='admin')
        self.assertTrue(result)


