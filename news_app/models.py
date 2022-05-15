from email import message
from email.errors import MessageError
from django.db import models
from django.utils import timezone

class Article(models.Model):
    name = models.CharField(max_length=100, default='NY Times')
    title = models.CharField(max_length=400)
    url = models.URLField()
    description = models.TextField()
    pub_date = models.DateTimeField(default=timezone.now)
    image = models.URLField()
    guid = models.CharField(max_length=400)

    def __str__(self):
        return f"{self.title}"
