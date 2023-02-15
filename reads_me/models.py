from django.db import models
from django.utils import timezone

from reads_me.constants import HISTORY


class Post(models.Model):
    timestamp = models.DateTimeField(default=timezone.now)
    date_popular = models.DateTimeField(default=timezone.now)
    wikipedia_id = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    content = models.TextField()
    image_url = models.URLField(null=True)
    category = models.CharField(max_length=100, default=HISTORY)
    slug = models.CharField(max_length=100, default=None, null=True)

    def __str__(self):
        return self.title


