from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('home/', views.home),
    path('formularioCliente/',views.formularioCliente),
    path('validaRegistroCliente/', views.validaRegistroCliente),
    path('formularioError/',views.formularioError),
    path('herramientas/', views.herramientas),
    path('utilidadProducto/',views.utilidadProducto),
    path('calculaUtilidad/',views.calculaUtilidad),
    path('utilidadError/',views.utilidadError),
    path('analisisVentas/',views.analisisVentas),
    path('revisionInventario/',views.revisionInventario),
    path('miCarrito/',views.carrito),
    path('tienda/<int:cat>',views.tienda),
    path('cliente/',views.cliente),
    path('clienteError/',views.clienteError),      
    path('validaCliente/', views.validaCliente),  
    path('factura/<rfc>',views.factura),
    path('eliminacionArticulo/<int:codigo>', views.eliminar_Articulo),
    path('addCarrito/<int:codigo>', views.addCarrito),
    path('cancelarCompra/',views.cancelarCompra),
    path('venta/<rfc>',views.venta)
]