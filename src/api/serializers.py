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

class SpaceSerializer(serializers.ModelSerializer):
    map_id = serializers.PrimaryKeyRelatedField(
        source='map.id',
        read_only=True
    )
    dimension = serializers.CharField(read_only=True)

    class Meta:
        model = Space
        fields = [
            'id',
            'name',
            'width',
            'height',
            'dimension',
            'map',
            'thumbnail',
            'map_id',
        ]

    def create(self, validated_data):
        try:
            # Map is already validated by the serializer
            map_obj = validated_data['map']
            
            # Create space with the validated data
            space = Space.objects.create(
                name=validated_data['name'],
                width=validated_data['width'],
                height=validated_data['height'],
                map=map_obj,
            )
            return space
            
        except KeyError as e:
            raise serializers.ValidationError(f"Missing required field: {str(e)}")

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

