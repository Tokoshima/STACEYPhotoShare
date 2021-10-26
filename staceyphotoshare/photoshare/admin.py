

# Register your models here.

from django.contrib import admin
from .models import Photo, Metadata

admin.site.register(Photo)
admin.site.register(Metadata)
