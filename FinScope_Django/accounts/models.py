from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    email = models.EmailField(max_length=254, unique=True)
    nickname = models.CharField(max_length=20)
    followings = models.ManyToManyField(
        "self", symmetrical=False, related_name="followers"
    )

    def __str__(self) -> str:
        return self.username
