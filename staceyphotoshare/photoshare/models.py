from django.db import models

# Create your models here.

from django.db import models

from django.contrib.auth import get_user_model

from taggit.managers import TaggableManager


class Photo(models.Model):
    image = models.ImageField(upload_to='photos/')

    # def __str__(self):
    #     return self.image


class Metadata(models.Model):
    title = models.CharField(max_length=100)

    description = models.CharField(max_length=300)

    created = models.DateTimeField(auto_now_add=True)

    submitter = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    tags = TaggableManager()

    def __str__(self):
        return self.title