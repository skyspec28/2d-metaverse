from django.urls import path
from . import views
from .views import AvatarView , SpaceCreateAPIView ,AdminCreateAvatarView


urlpatterns =[
    path('', views.index, name='index'),
    path('avatars/<int:pk>/', AvatarView, name='avatar-detail'),
    path('spaces/new/', SpaceCreateAPIView, name='space-create'),
    path('spaces/delete/<int:pk>/', views.DestroySpaceView.as_view(), name='space-delete'),
    path('spaces/all/', views.SpaceListAPIView.as_view(), name='space-list'),
    # path('spaces/<int:pk>/', views.RetrieveSpaceElementAPIView.as_view(), name='space-detail'),
    path('admin/element/new/', views.ElementCreateAPIView.as_view(), name='element-create'),
    path('admin/element/update/<int:pk>/', views.ElementUpdateAPIView.as_view(), name='element-update'),
    path('admin/avatar/new/', AdminCreateAvatarView, name='avatar-create'),
    path('admin/map/new/', views.MapCreateAPIView.as_view(), name='map-create'),
    path("metaverse/", views.metaverse, name="metaverse"),
    path("<str:room_name>/", views.room, name="room"),
]
