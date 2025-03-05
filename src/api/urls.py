from django.urls import path
from . import views
from .views import AvatarRetrieveView


urlpatterns =[
    path('avatars/<int:pk>/', AvatarRetrieveView, name='avatar-detail'),
    path('spaces/new/', views.CreateSpaceAPIView.as_view(), name='space-create'),
    path('spaces/delete/<int:pk>/', views.DestroySpaceView.as_view(), name='space-delete'),
    path('spaces/all/', views.SpaceListAPIView.as_view(), name='space-list'),
    # path('spaces/<int:pk>/', views.RetrieveSpaceElementAPIView.as_view(), name='space-detail'),
    path('admin/element/new/', views.ElementCreateAPIView.as_view(), name='element-create'),
    path('admin/element/update/<int:pk>/', views.ElementUpdateAPIView.as_view(), name='element-update'),
    path('admin/avatar/new/', views.CreateAvatarAPIView.as_view(), name='avatar-create'),
    path('admin/map/new/', views.MapCreateAPIView.as_view(), name='map-create'),
]
