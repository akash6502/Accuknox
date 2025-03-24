from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class FriendRequest(models.Model):
    status = models.BooleanField(default=False)
    to_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='to_user')
    from_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='from_user')

    def __str__(self):
        return f"FriendRequest sent from {self.from_user} to {self.to_user}"


# users/models.py

# from django.contrib.auth.models import User
# from django.db import models

# class FriendRequest(models.Model):
#     from_user = models.ForeignKey(User, related_name='sent_friend_requests', on_delete=models.CASCADE)
#     to_user = models.ForeignKey(User, related_name='received_friend_requests', on_delete=models.CASCADE)
#     timestamp = models.DateTimeField(auto_now_add=True)
#     accepted = models.BooleanField(default=False)

#     def __str__(self):
#         return f"FriendRequest from {self.from_user} to {self.to_user}"
