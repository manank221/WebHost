from django.db import models
from django.contrib.auth.models import User

# Optional: UserProfile for extra info
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Add extra fields here if needed
    # e.g. phone_number = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.user.username
