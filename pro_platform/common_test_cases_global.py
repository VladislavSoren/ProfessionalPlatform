from typing import Type

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.urls import reverse_lazy

from shop_projects.models import Creator

UserModel: Type[AbstractUser] = get_user_model()


class CreateTestUser:
    login_url = reverse_lazy("auth_block:login")

    @classmethod
    def setUpClass(cls):
        cls.username = "user_testing"
        cls.password = "superpass123!"
        cls.user: AbstractUser = UserModel.objects.create_user(
            username=cls.username,
            password=cls.password,
        )

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()


class CreateTestCreator(CreateTestUser):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.creator = Creator.objects.create(
            user=cls.user,
            rating='5',
        )

    @classmethod
    def tearDownClass(cls):
        cls.creator.delete()
        super().tearDownClass()


def login_test_user(self):
    response = self.client.post(
        self.login_url,
        {
            "username": self.username,
            "password": self.password,
        },
    )
    return response
