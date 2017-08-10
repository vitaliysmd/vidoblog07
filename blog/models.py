from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from stdimage import StdImageField

class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, null=True
    )
    title = models.CharField(max_length=200)
    text = models.TextField()
    description = models.CharField(max_length=200, blank=True, null=True)

    image = StdImageField(upload_to='images/',
        null=True,
        blank=True,
        verbose_name='Изображение',
        variations={'thumbnail': {'width': 400, 'height': 400}})

    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return "/blog/%i/" % self.id

class Comment(models.Model):
    post = models.ForeignKey('blog.Post', related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text
