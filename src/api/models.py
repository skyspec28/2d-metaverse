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
    """
    Represents interactive or static elements in a map
    """
    ELEMENT_TYPES = [
        ('furniture', 'Furniture'),
        ('interactive', 'Interactive Object'),
        ('decoration', 'Decoration'),
        ('portal', 'Portal'),
        ('spawn', 'Spawn Point'),
    ]

    name = models.CharField(max_length=255 ,null=True ,blank=True)
    type = models.CharField(max_length=20, choices=ELEMENT_TYPES , null=True, blank=True)
    
    # Sprite or image representation
    sprite_url = models.URLField(null=True, blank=True)
    
    is_walkable = models.BooleanField(default=False)
    interaction_script = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.type})"


class Map(models.Model):
    """
    Represents a spatial map/environment in the Gather Town clone
    """
    name = models.CharField(max_length=255)
    width = models.IntegerField()  # Map width in tiles
    height = models.IntegerField()  # Map height in tiles
    
    background_image = models.URLField(null=True, blank=True)
    
    tile_size = models.IntegerField(default=32)  # Pixel size of each tile
    
    elements = models.ManyToManyField(
        Element, 
        through='MapElement', 
        related_name='maps'
    )

    def __str__(self):
        return self.name
    

class MapElement(models.Model):
    """
    Represents the placement of an Element within a specific Map
    """
    map = models.ForeignKey(Map, on_delete=models.CASCADE)
    element = models.ForeignKey(Element, on_delete=models.CASCADE)
    
    x_coordinate = models.FloatField()  # X position on the map
    y_coordinate = models.FloatField()  # Y position on the map
    

    rotation = models.FloatField(default=0)
    z_index = models.IntegerField(default=0)  # For layering elements

    class Meta:
        unique_together = ('map', 'x_coordinate', 'y_coordinate')

    def __str__(self):
        return f"{self.element.name} at ({self.x_coordinate}, {self.y_coordinate}) in {self.map.name}"

class Avatar(models.Model):
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # renamed from avatar_id
    image_url = models.URLField(null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name if self.name else "Avatar" 

class UserMetadata(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    avatar = models.ForeignKey('Avatar', on_delete=models.CASCADE)