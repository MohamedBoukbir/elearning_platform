from django.db import models
# Create your models here.
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    # age = models.IntegerField(null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')], null=True, blank=True)
    # score = models.FloatField(null=True, blank=True)
    age = models.IntegerField(blank=True, null=True)  # Champ facultatif pour l'âge
    score = models.FloatField(blank=True, null=True)  # Champ facultatif pour le score
    def __str__(self):
        return self.username
