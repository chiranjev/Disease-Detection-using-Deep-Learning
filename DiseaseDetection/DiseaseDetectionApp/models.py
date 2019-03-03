from django.db import models

# Create your models here.

class Malaria(models.Model):
    malaria_img = models.ImageField(upload_to='images/')
    prediction = models.CharField(max_length=50) 
