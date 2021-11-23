from django.db import models
from taggit.managers import TaggableManager
from django.contrib.auth.models import User
import uuid

# Create your models here.

# Table for Album
class Album(models.Model):
    title = models.CharField(max_length=120)
    creator = models.ForeignKey(User,on_delete=models.CASCADE)
    tags = TaggableManager()
    published = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
  
    def __str__(self):
        return self.title


# Table for image in an album
class Picture(models.Model):
    
    image = models.ImageField(upload_to="images/",default=False)
    image_id = models.UUIDField(
         primary_key = True,
         default = uuid.uuid4,
         editable = False)
    album = models.ForeignKey(Album,on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.image.url     


# Table for caption of an image
class Caption(models.Model):
    title = models.CharField(max_length=120)
    font_color = models.CharField(max_length=120, default="black")
    picture = models.OneToOneField(
        Picture,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    def __str__(self):
        return self.title 

# Table for position of an image
class Pos(models.Model):
    position = models.CharField(max_length=60,default="static",blank=False)
    top = models.CharField(max_length=60, null=True)
    bottom = models.CharField(max_length=60,null=True)
    right = models.CharField(max_length=60,null=True)
    left = models.CharField(max_length=60,null=True)
    caption = models.OneToOneField(
        Caption,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    def __str__(self):
        return self.position  


# Table for similarity scores
class Similarity(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_one')
    similar_user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_two')
    score = models.IntegerField(null=True)
    
    def __str__(self):
        return self.user.username + " : "+self.similar_user.username    