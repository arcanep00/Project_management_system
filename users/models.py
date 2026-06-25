from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class UserRole(models.TextChoices):
    ADMIN = "ADMIN", "Admin"
    EMPLOYEE = "EMPLOYEE", "Employee"

class User(AbstractUser):
    email = models.EmailField(
        unique=True
    )
    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.EMPLOYEE
    )
    department = models.CharField(
        max_length=100,
        blank=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.username



