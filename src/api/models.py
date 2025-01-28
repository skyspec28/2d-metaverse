import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
   avatar = models.ForeignKey('Avatar', on_delete=models.SET_NULL, null=True, blank=True)
   
   
   def __str__(self):
       return self.username

class Space(models.Model):
   space_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
   name = models.CharField(max_length=255)
   width = models.IntegerField()
   height = models.IntegerField(null=True, blank=True) 
   map= models.ForeignKey('Map', on_delete=models.CASCADE)
   thumbnail = models.URLField(null=True, blank=True)
   
   def __str__(self):
       return self.name

class SpaceElement(models.Model):
   element = models.ForeignKey('Element', on_delete=models.CASCADE)
   space = models.ForeignKey('Space', on_delete=models.CASCADE)
   x = models.IntegerField()
   y = models.IntegerField()
   
   def __str__(self):
       return f"Element {self.element.id} in Space {self.space.id}"

class Element(models.Model):
   element_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
   width = models.IntegerField()
   height = models.IntegerField()
   image_url = models.URLField()
   
   def __str__(self):
       return f"Element {self.id}"

class Map(models.Model):
   
   width = models.IntegerField()
   height = models.IntegerField()
   name = models.CharField(max_length=255)
   image_url = models.URLField()
   static = models.BooleanField(default=True)
   
   def __str__(self):
       return self.name

class MapElement(models.Model):
   map = models.ForeignKey('Map', on_delete=models.CASCADE)
   element = models.ForeignKey('Element', on_delete=models.SET_NULL, null=True, blank=True)
   x = models.IntegerField(null=True, blank=True)
   y = models.IntegerField(null=True, blank=True)
   
   def __str__(self):
       return f"Element {self.element.id} in Map {self.map.id}"

class Avatar(models.Model):
   avatar_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
   image_url = models.URLField(null=True, blank=True)
   name = models.CharField(max_length=255, null=True, blank=True)
   
   def __str__(self):
       return self.name if self.name else "Avatar"
   
class UserMetadata(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    avatar = models.ForeignKey('Avatar', on_delete=models.CASCADE )