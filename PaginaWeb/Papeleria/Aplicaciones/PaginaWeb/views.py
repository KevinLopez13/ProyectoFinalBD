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
    return render(request, 'ventas.html')

def revisionInventario(request):
    return render(request, 'revInventario.html')