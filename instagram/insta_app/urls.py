"""instagram URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from . import views

urlpatterns = [
    
    path('',views.home, name='home'),
    path('albums/<username>',views.albums, name='albums'),
    path('published_albums/<username>',views.published_albums, name='published_albums'),
    # path('create_album/<username>',views.create_album, name='create_album'),
    path('publish_album/<username>/<title>',views.publish_album, name='publish_album'),
    path('add_photo/<username>/<title>',views.add_photo, name='add_photo'),
    path('similar_users/<username>',views.similar_users, name='similar_users'),
    path('display_album/<username>/<title>',views.display_album, name='album'),
    path('add_hashtag/<username>/<title>',views.add_hashtag, name='add_hashtag'),
    path('delete_photo/<username>/<title>/<image_id>',views.delete_photo, name='delete_photo'),
    path('delete_album/<username>/<title>',views.delete_album, name='delete_album'),
]
