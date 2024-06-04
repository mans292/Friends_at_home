from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name="about"),
    path('care/', views.care, name="care"),
    path('add_to_cart/<str:pk>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<str:pk>/', views.remove_from_cart, name='remove_from_cart'),
    path('create_order', views.create_klarna_order, name='create_order'),
    path('thankyou.php', views.read_klarna_order, name='thankyou_page'),
    path('add_quantity/<str:pk>/', views.add_quantity, name='add_quantity'),
    path('decrease_quantity/<str:pk>/', views.decrease_quantity, name='decrease_quantity'),
    path('product_info/<str:pk>/', views.product_info, name='product_info'),
    path('policies/', views.policies, name='policies'),
    path('kopvillkor/', views.villkor, name="villkor"),
]