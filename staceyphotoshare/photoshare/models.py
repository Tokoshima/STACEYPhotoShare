from django.db import models

# Create your models here.

from django.db import models

from django.contrib.auth import get_user_model

from taggit.managers import TaggableManager


class Photo(models.Model):
    image = models.ImageField(upload_to='photos/', default='default.jpg')
    submitter = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='submitter_type')
    access = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='accessor_type')


    # def __str__(self):
    #     return self.image


# metadata.photo.image
class Metadata(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    created = models.DateTimeField(auto_now_add=True)
    submitter = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    location = models.CharField(max_length=300)
    # image = models.ForeignKey(Photo, on_delete=models.CASCADE, default=1)
    tags = TaggableManager()
    photo = models.OneToOneField(Photo, on_delete=models.CASCADE, primary_key=True)
    access = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='+')

    def __str__(self):
        return self.title


class Album(models.Model):
    title = models.CharField(max_length=100)

    image = models.ManyToManyField(Photo, default=1)

    def __str__(self):
        return self.title
