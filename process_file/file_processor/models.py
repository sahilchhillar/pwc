from django.db import models

# Create your models here.
class File(models.Model):
    _id = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    file_data = models.BinaryField()