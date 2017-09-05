from django.db import models

# Create your models here.
class Urlshort(models.Model):
    hash_value = models.CharField(max_length=200)
    original_url = models.CharField(max_length=2000)
