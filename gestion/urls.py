from django.urls import path
from . import views


urlpatterns = [
    path('', views.landing_page, name='landing'),
    path('productos/', views.lista_productos_protegida, name='lista_productos'),
    path('eliminar/<int:pk>/', views.intentar_eliminar_producto, name='intentar_eliminar_producto'),
]