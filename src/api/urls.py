from django.urls import path
from . import views


urlpatterns =[
    path('avatars/<int:pk>/', views.AvatarRetrieveView.as_view(), name='avatar-detail'),
    path('spaces/new/', views.CreateSpaceAPIView.as_view(), name='space-create'),
    path('spaces/delete/<int:pk>/', views.DestroySpaceView.as_view(), name='space-delete'),
    path('spaces/all/', views.SpaceListAPIView.as_view(), name='space-list'),
    # path('spaces/<int:pk>/', views.RetrieveSpaceElementAPIView.as_view(), name='space-detail'),
    path('elements/admin/new/', views.ElementCreateAPIView.as_view(), name='element-create'),
]