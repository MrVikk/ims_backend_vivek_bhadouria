from django.urls import path
from .views import create_item, item_list, update_item, delete_item

urlpatterns = [
    path('create/', create_item, name='create_item'),
    path('list/', item_list, name='item_list'),
    path('update/<int:pk>/', update_item, name='update_item'),
    path('delete/<int:pk>/', delete_item, name='delete_item'),
]