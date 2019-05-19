from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User

from core import models


class ClientTestCase(APITestCase):
    def setUp(self):
        User.objects.create_user(
            username='camilo', email='camilolgon@gmail.com', password='uluyac'
        )

    def test_create_client(self):
        client_data = {
            "name": "Felicity",
            "surname": "Jones",
            "email": "felicity@gmail.com",
            "telephone": "11984345678",
            "cpf": "34598712387",
        }
        self.client.login(username='camilo', password='uluyac')
        response = self.client.post('/clients/', data=client_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.Client.objects.count(), 1)
        self.assertEqual(response.data, client_data)

    def test_create_complete_client(self):
        client_data = {
            "name": "Felicity",
            "surname": "Jones",
            "email": "felicity@gmail.com",
            "telephone": "11984345678",
            "cpf": "34598712387",
        }
        self.client.login(username='camilo', password='uluyac')
        for key in client_data.keys():
            temporary_client_data = {**client_data}
            del temporary_client_data[key]
            response = self.client.post(
                '/clients/', data=temporary_client_data, format='json'
            )
            self.assertContains(response, key, status_code=status.HTTP_400_BAD_REQUEST)
            self.assertEqual(models.Client.objects.count(), 0)

    def test_client_unique_cpf(self):
        client1_data = {
            "name": "Felicity",
            "surname": "Jones",
            "email": "felicity@gmail.com",
            "telephone": "11984345678",
            "cpf": "34598712387",
        }
        client2_data = {
            "name": "Angelica",
            "surname": "Huck",
            "email": "angeliquinha.huckinha@gmail.com",
            "telephone": "11983789585",
            "cpf": "34598712387",
        }
        self.client.login(username='camilo', password='uluyac')
        response = self.client.post('/clients/', data=client1_data, format='json')
        self.assertEqual(models.Client.objects.count(), 1)
        response = self.client.post('/clients/', data=client2_data, format='json')
        self.assertContains(response, 'cpf', status_code=status.HTTP_400_BAD_REQUEST)
        self.assertEqual(models.Client.objects.count(), 1)

    def test_client_unique_email(self):
        client1_data = {
            "name": "Felicity",
            "surname": "Jones",
            "email": "felicity@gmail.com",
            "telephone": "11984345678",
            "cpf": "34598712387",
        }
        client2_data = {
            "name": "Angelica",
            "surname": "Huck",
            "email": "felicity@gmail.com",
            "telephone": "11983789585",
            "cpf": "97825380823",
        }
        self.client.login(username='camilo', password='uluyac')
        response = self.client.post('/clients/', data=client1_data, format='json')
        self.assertEqual(models.Client.objects.count(), 1)
        response = self.client.post('/clients/', data=client2_data, format='json')
        self.assertContains(response, 'email', status_code=status.HTTP_400_BAD_REQUEST)
        self.assertEqual(models.Client.objects.count(), 1)

    def test_create_client_valid_cpf(self):
        client_data = {
            "name": "Felicity",
            "surname": "Jones",
            "email": "felicity@gmail.com",
            "telephone": "11984345678",
            "cpf": "34598712387",
        }
        self.client.login(username='camilo', password='uluyac')

        client_data['cpf'] = "3459871238"  # cpf shorter than the espected
        response = self.client.post('/clients/', data=client_data, format='json')
        self.assertContains(response, 'cpf', status_code=status.HTTP_400_BAD_REQUEST)
        self.assertEqual(models.Client.objects.count(), 0)

        client_data['cpf'] = "345987123879"  # cpf longer than the espected
        response = self.client.post('/clients/', data=client_data, format='json')
        self.assertContains(response, 'cpf', status_code=status.HTTP_400_BAD_REQUEST)
        self.assertEqual(models.Client.objects.count(), 0)

        client_data['cpf'] = "3459a712_387"  # unexpected  character.
        response = self.client.post('/clients/', data=client_data, format='json')
        self.assertContains(response, 'cpf', status_code=status.HTTP_400_BAD_REQUEST)
        self.assertEqual(models.Client.objects.count(), 0)

    def test_create_client_valid_email(self):
        client_data = {
            "name": "Felicity",
            "surname": "Jones",
            "email": "felicity@gmail.com",
            "telephone": "11984345678",
            "cpf": "34598712387",
        }
        self.client.login(username='camilo', password='uluyac')

        client_data['email'] = "@gmail.com"  # email without prefix
        response = self.client.post('/clients/', data=client_data, format='json')
        self.assertContains(response, 'email', status_code=status.HTTP_400_BAD_REQUEST)
        self.assertEqual(models.Client.objects.count(), 0)

        client_data['email'] = ".fel=icit-@gmail.com"  # prefix with invalid prefix
        response = self.client.post('/clients/', data=client_data, format='json')
        self.assertContains(response, 'email', status_code=status.HTTP_400_BAD_REQUEST)
        self.assertEqual(models.Client.objects.count(), 0)

        client_data['email'] = "felicity@"  # email without domain
        response = self.client.post('/clients/', data=client_data, format='json')
        self.assertContains(response, 'email', status_code=status.HTTP_400_BAD_REQUEST)
        self.assertEqual(models.Client.objects.count(), 0)

        client_data['email'] = "felicity@gm+ail.c_m"  # unexpected characters in domain.
        response = self.client.post('/clients/', data=client_data, format='json')
        self.assertContains(response, 'email', status_code=status.HTTP_400_BAD_REQUEST)
        self.assertEqual(models.Client.objects.count(), 0)

        client_data['email'] = "felicity@gmail.coma"  # domain with more characters than the espected after the dot.
        response = self.client.post('/clients/', data=client_data, format='json')
        self.assertContains(response, 'email', status_code=status.HTTP_400_BAD_REQUEST)
        self.assertEqual(models.Client.objects.count(), 0)

        client_data['email'] = "felicity@gmail.c"  # domain with less characters than the espected after the dot.
        response = self.client.post('/clients/', data=client_data, format='json')
        self.assertContains(response, 'email', status_code=status.HTTP_400_BAD_REQUEST)
        self.assertEqual(models.Client.objects.count(), 0)

    def test_create_client_valid_telephone(self):
        client_data = {
            "name": "Felicity",
            "surname": "Jones",
            "email": "felicity@gmail.com",
            "telephone": "11984345678",
            "cpf": "34598712387",
        }
        self.client.login(username='camilo', password='uluyac')

        client_data['telephone'] = "119843456789"  # telephone longer than the espected.
        response = self.client.post('/clients/', data=client_data, format='json')
        self.assertContains(response, 'telephone', status_code=status.HTTP_400_BAD_REQUEST)
        self.assertEqual(models.Client.objects.count(), 0)

        client_data['telephone'] = "1198434569"  # telephone shorter than the espected.
        response = self.client.post('/clients/', data=client_data, format='json')
        self.assertContains(response, 'telephone', status_code=status.HTTP_400_BAD_REQUEST)
        self.assertEqual(models.Client.objects.count(), 0)

        client_data['telephone'] = "119a43.56-8"  # telephone with unexpected characters.
        response = self.client.post('/clients/', data=client_data, format='json')
        self.assertContains(response, 'telephone', status_code=status.HTTP_400_BAD_REQUEST)
        self.assertEqual(models.Client.objects.count(), 0)
