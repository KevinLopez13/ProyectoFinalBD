from django.shortcuts import render, redirect
from django.db import connection
from django.contrib import messages


# Create your views here.

def home(request):
    return render(request,'home.html')

def formularioCliente(request):
    return render(request,'formularioCliente.html')

def herramientas(request):
    return render(request,'herramientas.html')

def utilidadProducto(request):
    return render(request, 'utilidadProducto.html')

def analisisVentas(request):
    return render(request, 'analisisVentas.html')

def revisionInventario(request):
    return render(request, 'revInventario.html')

# Modulos del carrito 

def carrito(request):
    return render(request, 'carrito.html')

def eliminar_Articulo(request):

    #Trabajar aqui directamente con la BD mediante sentencias SQL

    return redirect('/miCarrito')

# Modulos de la vista de tienda

def tienda(request):
    return render(request, 'tienda.html')

def cliente(request):
    return render(request, 'clienteventa.html')

def clienteError(request):
    return render(request, 'clienteError.html')

# Modulos de la  factura

def validaCliente(request):
    rfc = request.POST['txtRFC']
    rfcResponse = False
    # CONSULTA SQL
    with connection.cursor() as cursor:
        cursor.execute("SELECT rfc FROM cliente WHERE rfc=%s;",[rfc])
        row = cursor.fetchone()
        if row != None:
            rfcResponse = True
            #print("Response SQL:", rfcResponse)

    if rfcResponse:
        #print("Cliente Encontrado")
        return redirect('/factura')
    else:
        # messages.warning(request,'Cliente no encontrado')
        return redirect('/clienteError')
        #return redirect('/cliente')


def factura(request):
    return render(request, 'factura.html')
