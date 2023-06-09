from django.urls import path
from . import views

app_name = 'main_app'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('add-product/<int:product_id>/', views.add_product, name='add-product'),
    path('remove-product/<int:product_id>/', views.remove_product, name='remove-product'),
]
