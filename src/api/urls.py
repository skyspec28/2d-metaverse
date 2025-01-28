from django.urls import path
from . import views


urlpatterns =[
    path('avatars/<int:pk>/', views.AvatarRetrieveView.as_view(), name='avatar-detail'),
    path('spaces/<int:pk>/', views.SpaceView.as_view(), name='space-create')
]