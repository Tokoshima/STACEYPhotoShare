from django.urls import path

from .views import PhotoListView, PhotoDeleteView, PhotoTagListView, PhotoCreateView, PhotoUpdateView, MetadataView

app_name = 'photo'

urlpatterns = [
    path('', PhotoListView.as_view(), name='list'),

    path('photo/<int:pk>/delete/', PhotoDeleteView.as_view(), name='delete'),

    path('tag/<slug:tag>/', PhotoTagListView.as_view(), name='tag'),

    path('photo/create/', PhotoCreateView.as_view(), name='create'),

    path('photo/<int:pk>/update/', PhotoUpdateView.as_view(), name='update'),

    path('photo/<int:pk>/', MetadataView.as_view(), name='metadata'),

]
