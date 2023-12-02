from django.db import models
from PIL import Image

# Create your models here.

class Photo(models.Model):
    image = models.ImageField(upload_to= 'uploaded_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)