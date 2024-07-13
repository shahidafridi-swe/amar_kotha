from django.db import models
from django.contrib.auth.models import User

USER_TYPE = (
    ('Editor', 'Editor'),
    ('Viewer', 'Viewer'),
)

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='account')
    image = models.ImageField(upload_to='users/images/', null=True, blank=True)
    phone = models.CharField(max_length=11)
    user_type = models.CharField(max_length=10, choices=USER_TYPE)
    
    def __str__(self) -> str:
        return f"{self.user.username} - {self.user_type}"
