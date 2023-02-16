from django.db import models

# Create your models here.

class Programme(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name

class Level(models.Model):
    name = models.CharField(max_length=3)

    def __str__(self) -> str:
        return self.name

class Setting(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=255, default='')
    logo = models.FileField(null=True, blank=True)
    signature = models.FileField(null=True, blank=True)
    phone_number = models.CharField(max_length=15)
    website = models.CharField(max_length=255, null=True, blank=True)
