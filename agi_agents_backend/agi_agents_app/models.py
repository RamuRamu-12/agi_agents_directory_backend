from django.db import models

# Create your models here.

class Agent(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=50)
    industry = models.CharField(max_length=50)
    pricing_model = models.CharField(max_length=20)
    accessory_model = models.CharField(max_length=20)
    date_added = models.DateTimeField(auto_now_add=True)
    website_url = models.URLField(max_length=200)

    def __str__(self):
        return self.name
