from django.shortcuts import render, redirect

# Create your views here.

def home(request):
    return render(request,'home.html')

def registrarCliente(request):
    return render(request,'registroCliente.html')

def herramientas(request):
    return render(request,'herramientas.html')

def utilidadProducto(request):
    return render(request, 'utilidadProducto.html')

def analisisVentas(request):
    return render(request, 'analisisVentas.html')

def revisionInventario(request):
    return render(request, 'revInventario.html')

def carrito(request):
    return render(request, 'carrito.html')

def tienda(request):
    return render(request, 'tienda.html')

def cliente(request):
    return render(request, 'clienteventa.html')