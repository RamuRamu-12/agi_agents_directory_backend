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

    tagline = models.CharField(max_length=255, null=True, blank=True)
    likes = models.PositiveIntegerField(default=0)
    overview = models.TextField(null=True, blank=True)
    key_features = models.TextField(null=True, blank=True)
    use_cases = models.TextField(null=True, blank=True)
    created_by = models.CharField(max_length=255, null=True, blank=True)
    access = models.CharField(max_length=50, null=True, blank=True)
    tags = models.TextField(null=True, blank=True)
    
    # Fields for preview image and demo video
    preview_image = models.URLField(max_length=500, null=True, blank=True)
    demo_video = models.URLField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.name
