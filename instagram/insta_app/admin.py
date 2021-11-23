from django.contrib import admin
from .models import Album
from .models import Picture
from .models import Caption
from .models import Similarity


# Register your models here.
admin.site.register(Album)
admin.site.register(Picture)
admin.site.register(Caption)
admin.site.register(Similarity)