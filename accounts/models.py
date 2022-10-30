from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
# Create your models here.

class Account(AbstractUser):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)

    is_seller = models.BooleanField(default=False)
    first_name = models.CharField(max_length = 50)
    last_name = models.CharField(max_length = 50)
    

    REQUIRED_FIELDS = ['first_name', 'last_name']

