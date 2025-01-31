from django.contrib import admin
from api.models import Avatar ,CustomUser ,Space ,UserMetadata ,Map , Element , SpaceElement ,MapElement 
# Register your models here.

admin.site.register(Avatar )
admin.site.register(CustomUser)
admin.site.register(Space)
admin.site.register(UserMetadata)
admin.site.register(Map)
admin.site.register(Element)
admin.site.register(SpaceElement)
admin.site.register(MapElement)
