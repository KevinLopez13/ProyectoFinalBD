from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home),
    path('formularioCliente/',views.formularioCliente),
    path('herramientas/', views.herramientas),
    path('utilidadProducto/',views.utilidadProducto),
    path('analisisVentas/',views.analisisVentas),
    path('revisionInventario/',views.revisionInventario),
    path('miCarrito/',views.carrito),
    path('tienda/<int:cat>',views.tienda),
    path('cliente/',views.cliente),
    path('clienteError/',views.clienteError),      
    path('validaCliente/', views.validaCliente),  
    path('factura/',views.factura),
    path('eliminacionArticulo/', views.eliminar_Articulo)
]