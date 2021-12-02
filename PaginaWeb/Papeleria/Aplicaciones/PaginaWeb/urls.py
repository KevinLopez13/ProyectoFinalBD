from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home),
    path('registrarCliente/',views.registrarCliente),
    path('herramientas/', views.herramientas),
    path('utilidadProducto/',views.utilidadProducto),
    path('analisisVentas/',views.analisisVentas),
    path('revisionInventario/',views.revisionInventario),
    path('miCarrito/',views.carrito),
    path('tienda/',views.tienda),
    path('cliente/',views.cliente)
]