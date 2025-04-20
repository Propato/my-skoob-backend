from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from .models import UserProfile
from .serializers import UserSerializer


class UserAPITestCase(APITestCase):
    def setUp(self):
        self.user_data = {
            "name": "testuser",
            "email": "user@user.com",
            "password": "testpassword",
        }
        self.superuser_data = {
            "name": "testsuperuser",
            "email": "adm@adm.com",
            "password": "testsuperpassword",
        }
        self.user = UserProfile.objects.create_user(**self.user_data)
        self.superuser = UserProfile.objects.create_superuser(**self.superuser_data)

    def test_get_all_users(self):
        url = reverse("get_all_users")

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data["detail"], "Authentication credentials were not provided."
        )

        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data["detail"],
            "You do not have permission to perform this action.",
        )

        self.client.force_authenticate(user=self.superuser)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        num_users = UserProfile.objects.count()

        self.assertEqual(num_users, len(response.data))

        user = UserProfile.objects.get(email=self.user_data["email"])
        serialized_user = UserSerializer(user).data

        self.assertEqual(
            serialized_user,
            {
                "id": user.id,
                "last_login": None,
                "is_superuser": False,
                "name": self.user_data["name"],
                "email": self.user_data["email"],
                "profile_picture": None,
                "gender": None,
                "birthday": None,
                "is_staff": False,
                "is_active": True,
                "groups": [],
                "user_permissions": [],
            },
        )
        self.assertIn(serialized_user, response.data)

        superuser = UserProfile.objects.get(email=self.superuser_data["email"])
        serialized_superuser = UserSerializer(superuser).data

        self.assertEqual(
            serialized_superuser,
            {
                "id": superuser.id,
                "last_login": None,
                "is_superuser": True,
                "name": self.superuser_data["name"],
                "email": self.superuser_data["email"],
                "profile_picture": None,
                "gender": None,
                "birthday": None,
                "is_staff": True,
                "is_active": True,
                "groups": [],
                "user_permissions": [],
            },
        )
        self.assertIn(serialized_superuser, response.data)

    def test_create_user(self):
        url = reverse("create_user")

        user2_data = {
            "name": "testuser",
            "email": "user@user.com",
            "password": "testpassword",
        }

        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"], "No data")

        response = self.client.post(url, user2_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data, {"email": ["user profile with this email already exists."]}
        )

        user2_data["email"] = "user2@user2.com"
        response = self.client.post(url, user2_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data,
            {
                "id": response.data["id"],
                "last_login": None,
                "is_superuser": False,
                "name": user2_data["name"],
                "email": user2_data["email"],
                "profile_picture": None,
                "gender": None,
                "birthday": None,
                "is_staff": False,
                "is_active": True,
                "groups": [],
                "user_permissions": [],
            },
        )
        self.assertNotIn("password", response.data)

        user = UserProfile.objects.get(email=user2_data["email"])
        self.assertTrue(user.check_password(user2_data["password"]))

        serialized_user = UserSerializer(user).data
        self.assertEqual(response.data, serialized_user)

    # def test_login_user(self):
    #     url = reverse('login_user')

    #     response = self.client.post(url)
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(response.data['detail'], 'No data')

    #     response = self.client.post(url, {"email": "wrongemail", "password": "wrongpassword"})
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    #     self.assertEqual(response.data['detail'], 'Invalid credentials')

    #     response = self.client.post(url, {"email": self.user_data["email"], "password": "wrongpassword"})
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    #     self.assertEqual(response.data['detail'], 'Invalid credentials')

    #     response = self.client.post(url, {"email": self.user_data["email"], "password": self.user_data["password"]})
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    #     token = response.data['token']
    #     user = UserProfile.objects.get(email=self.user_data["email"])

    #     self.assertEqual(user.auth_token.key, token)
