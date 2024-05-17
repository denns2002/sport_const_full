from rest_framework.reverse import reverse_lazy
from rest_framework.test import APITestCase, APIRequestFactory
from users.models.user import User


class UserTests(APITestCase):
    def test_login(self):
        factory = APIRequestFactory
        response = factory.post(reverse_lazy('login'), {'login': 'admin', 'password': 'admin'})
        print(response)
        user_data = User.objects.get()
        self.assertEqual(response, user_data)
