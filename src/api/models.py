from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import ValidationError

class CustomUser(AbstractUser):
    def __str__(self):
        return self.username

class Space(models.Model):
    name = models.CharField(max_length=255)
    width = models.IntegerField()
    height = models.IntegerField(null=True, blank=True)
    dimension = models.CharField(max_length=10, null=True, blank=True)  # Store "widthxheight"
    map = models.ForeignKey('Map', on_delete=models.CASCADE)
    thumbnail = models.URLField(null=True, blank=True)

    def clean(self):
        if self.width or self.height <= 0 :
            raise ValidationError("Width and height must be greater than zero.")

    def save(self, *args, **kwargs):
        """Automatically generate the dimension field before saving."""
        if self.width and self.height:
            self.dimension = f"{self.width}x{self.height}"
        else:
            self.dimension = None  # If width or height is missing, set dimension to None
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Space {self.id} - {self.name}"

class SpaceElement(models.Model):
    element = models.ForeignKey('Element', on_delete=models.CASCADE)
    space = models.ForeignKey('Space', on_delete=models.CASCADE)
    x = models.IntegerField()
    y = models.IntegerField()

    def __str__(self):
        return f"Element {self.element.id} in Space {self.space.id}"

class Element(models.Model):
    width = models.IntegerField()
    height = models.IntegerField()
    image_url = models.URLField()
    is_static = models.BooleanField(default=True)
 

    def __str__(self):
        return f"Element {self.id}"

class Map(models.Model):
    width = models.IntegerField()
    height = models.IntegerField()
    name = models.CharField(max_length=255)
    image_url = models.URLField(null=True, blank=True)
    is_static = models.BooleanField(default=True)

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
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # renamed from avatar_id
    image_url = models.URLField(null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name if self.name else "Avatar" 

class UserMetadata(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    avatar = models.ForeignKey('Avatar', on_delete=models.CASCADE)