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
        client = {
            "name": "Felicity",
            "surname": "Jones",
            "email": "felicity@gmail.com",
            "telephone": "11984345678",
            "cpf": "34598712387",
        }
        self.client.login(username='camilo', password='uluyac')
        response = self.client.post('/clients/', data=client, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.Client.objects.count(), 1)
        self.assertEqual(response.data, client)

    def test_create_complete_client(self):
        client = {
            "name": "Felicity",
            "surname": "Jones",
            "email": "felicity@gmail.com",
            "telephone": "11984345678",
            "cpf": "34598712387",
        }
        self.client.login(username='camilo', password='uluyac')
        for key in client.keys():
            temporary_client_data = {**client}
            del temporary_client_data[key]
            response = self.client.post(
                '/clients/', data=temporary_client_data, format='json'
            )
            self.assertContains(response, key, status_code=status.HTTP_400_BAD_REQUEST)
            self.assertEqual(models.Client.objects.count(), 0)

    def test_client_unique_cpf(self):
        client1 = {
            "name": "Felicity",
            "surname": "Jones",
            "email": "felicity@gmail.com",
            "telephone": "11984345678",
            "cpf": "34598712387",
        }
        client2 = {
            "name": "Angelica",
            "surname": "Huck",
            "email": "angeliquinha.huckinha@gmail.com",
            "telephone": "11983789585",
            "cpf": "34598712387",
        }
        self.client.login(username='camilo', password='uluyac')
        response = self.client.post('/clients/', data=client1, format='json')
        self.assertEqual(models.Client.objects.count(), 1)
        response = self.client.post('/clients/', data=client2, format='json')
        self.assertContains(response, 'cpf', status_code=status.HTTP_400_BAD_REQUEST)
        self.assertEqual(models.Client.objects.count(), 1)

    def test_client_unique_email(self):
        client1 = {
            "name": "Felicity",
            "surname": "Jones",
            "email": "felicity@gmail.com",
            "telephone": "11984345678",
            "cpf": "34598712387",
        }
        client2 = {
            "name": "Angelica",
            "surname": "Huck",
            "email": "felicity@gmail.com",
            "telephone": "11983789585",
            "cpf": "97825380823",
        }
        self.client.login(username='camilo', password='uluyac')
        response = self.client.post('/clients/', data=client1, format='json')
        self.assertEqual(models.Client.objects.count(), 1)
        response = self.client.post('/clients/', data=client2, format='json')
        self.assertContains(response, 'email', status_code=status.HTTP_400_BAD_REQUEST)
        self.assertEqual(models.Client.objects.count(), 1)

    def test_create_client_valid_cpf(self):
        client = {
            "name": "Felicity",
            "surname": "Jones",
            "email": "felicity@gmail.com",
            "telephone": "11984345678",
            "cpf": "34598712387",
        }
        self.client.login(username='camilo', password='uluyac')

        client['cpf'] = "3459871238"  # cpf thinner than the espected
        response = self.client.post('/clients/', data=client, format='json')
        self.assertContains(response, 'cpf', status_code=status.HTTP_400_BAD_REQUEST)
        self.assertEqual(models.Client.objects.count(), 0)

        client['cpf'] = "345987123879"  # cpf wider than the espected
        response = self.client.post('/clients/', data=client, format='json')
        self.assertContains(response, 'cpf', status_code=status.HTTP_400_BAD_REQUEST)
        self.assertEqual(models.Client.objects.count(), 0)

        client['cpf'] = "3459a712_387"  # unespected  character.
        response = self.client.post('/clients/', data=client, format='json')
        self.assertContains(response, 'cpf', status_code=status.HTTP_400_BAD_REQUEST)
        self.assertEqual(models.Client.objects.count(), 0)

    def test_create_client_valid_email(self):
        client = {
            "name": "Felicity",
            "surname": "Jones",
            "email": "felicity@gmail.com",
            "telephone": "11984345678",
            "cpf": "34598712387",
        }
        self.client.login(username='camilo', password='uluyac')

        client['email'] = "@gmail.com"  # email without prefix
        response = self.client.post('/clients/', data=client, format='json')
        self.assertContains(response, 'email', status_code=status.HTTP_400_BAD_REQUEST)
        self.assertEqual(models.Client.objects.count(), 0)

        client['email'] = ".fel=icit-@gmail.com"  # prefix with invalid prefix
        response = self.client.post('/clients/', data=client, format='json')
        self.assertContains(response, 'email', status_code=status.HTTP_400_BAD_REQUEST)
        self.assertEqual(models.Client.objects.count(), 0)

        client['email'] = "felicity@"  # email without domain
        response = self.client.post('/clients/', data=client, format='json')
        self.assertContains(response, 'email', status_code=status.HTTP_400_BAD_REQUEST)
        self.assertEqual(models.Client.objects.count(), 0)

        client['email'] = "felicity@gm+ail.c_m"  # unespected characters in domain.
        response = self.client.post('/clients/', data=client, format='json')
        self.assertContains(response, 'email', status_code=status.HTTP_400_BAD_REQUEST)
        self.assertEqual(models.Client.objects.count(), 0)

        client['email'] = "felicity@gmail.coma"  # domain with more characters than the espected after the dot.
        response = self.client.post('/clients/', data=client, format='json')
        self.assertContains(response, 'email', status_code=status.HTTP_400_BAD_REQUEST)
        self.assertEqual(models.Client.objects.count(), 0)

        client['email'] = "felicity@gmail.c"  # domain with less characters than the espected after the dot.
        response = self.client.post('/clients/', data=client, format='json')
        self.assertContains(response, 'email', status_code=status.HTTP_400_BAD_REQUEST)
        self.assertEqual(models.Client.objects.count(), 0)

    def test_create_client_valid_telephone(self):
        client = {
            "name": "Felicity",
            "surname": "Jones",
            "email": "felicity@gmail.com",
            "telephone": "11984345678",
            "cpf": "34598712387",
        }
        self.client.login(username='camilo', password='uluyac')

        client['telephone'] = "119843456789"  # telephone wider than the espected.
        response = self.client.post('/clients/', data=client, format='json')
        self.assertContains(response, 'telephone', status_code=status.HTTP_400_BAD_REQUEST)
        self.assertEqual(models.Client.objects.count(), 0)

        client['telephone'] = "1198434569"  # telephone thinner than the espected.
        response = self.client.post('/clients/', data=client, format='json')
        self.assertContains(response, 'telephone', status_code=status.HTTP_400_BAD_REQUEST)
        self.assertEqual(models.Client.objects.count(), 0)

        client['telephone'] = "119a43.56-8"  # telephone with unespected characters.
        response = self.client.post('/clients/', data=client, format='json')
        self.assertContains(response, 'telephone', status_code=status.HTTP_400_BAD_REQUEST)
        self.assertEqual(models.Client.objects.count(), 0)
