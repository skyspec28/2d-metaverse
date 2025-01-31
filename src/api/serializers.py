from rest_framework import serializers 
from api.models import Avatar,Space,SpaceElement,Element,CustomUser,Map ,MapElement


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


class MapElementSerializer(serializers.ModelSerializer):
    element = ElementSerializer(read_only=True)
    element_id = serializers.PrimaryKeyRelatedField(
        queryset=Element.objects.all(), 
        source='element', 
        write_only=True
    )

    class Meta:
        model = MapElement
        fields = ['element', 'element_id', 'x_coordinate', 'y_coordinate', 'rotation', 'z_index']

class MapSerializer(serializers.ModelSerializer):
    elements = MapElementSerializer(
        source='mapelement_set', 
        many=True, 
        required=False
    )
    

    class Meta:
        model = Map
        fields = ['id', 'name', 'width', 'height', 'background_image', 'tile_size', 'elements']

    def create(self, validated_data):
        # Extract elements data if provided
        elements_data = validated_data.pop('mapelement_set', [])
        
        # Create map first
        map_instance = Map.objects.create(**validated_data)
        
        # Add elements if provided
        for element_data in elements_data:
            MapElement.objects.create(
                map=map_instance,
                element=element_data['element'],
                x_coordinate=element_data['x_coordinate'],
                y_coordinate=element_data['y_coordinate'],
                rotation=element_data.get('rotation', 0),
                z_index=element_data.get('z_index', 0)
            )
        
        return map_instance