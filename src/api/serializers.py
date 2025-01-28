from rest_framework import serializers
from api.models import Avatar ,Space ,SpaceElement ,Element ,Map ,MapElement ,CustomUser


class CustomUserMetadataSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'avatar_id',
        ]


        

class AvatarsSerializer( serializers.ModelSerializer):
    class Meta:
        model = Avatar
        fields = [
            'id',
            'image_url',
            'name',
        ]

class SpaceSerializer( serializers.ModelSerializer):
    class Meta:
        model = Space
        fields = [
            'name',
            'dimensions',
            'map',
        ]

        #get map objects
        def create(self, validated_data):
            dimension = validated_data['dimension']
            width, height = map(int ,dimension.split('x'))
            map_id = validated_data['map_id']
            map_obj = Map.objects.get(id=map_id)

        #create space and return 
            space =Space.objects.create(
                name=validated_data['name'],
                width=width,
                height=height,
                map=map_obj,
            )
            return space

class SpaceElementSerializer( serializers.ModelSerializer):
    class Meta:
        model = SpaceElement
        fields = [
            'id',
            'element',
            'space',
            'x',
            'y',
        ]

class ElementSerializer( serializers.ModelSerializer):
    class Meta:
        model = Element
        fields = [
            'id',
            'width',
            'height',
            'image_url',

        ]
        
class MapSerializeer(serializers.ModelSerializer):
    class Meta:
        model = Map
        fields =[
            'weidth',
            'height',
            'name',
            
        ]

class MapELementSerializer(serializers.ModelSerializer):
    class Meta:
        model= MapElement
        fields = [
            'id',
            'map',
            'element',
            'x',
            'y'
        ]

