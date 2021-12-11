from django.shortcuts import render, redirect
from django.db import connection
from django.contrib import messages

class categoria():
    def __init__(self,id,tipo) -> None:
        self.id = id
        self.tipo = tipo

class producto():
    def __init__(self, registro) -> None:
        self.codigo = registro[0]
        self.precio = registro[1]
        self.marca = registro[2]
        self.descripcion = registro[3]
        self.id_cat = registro[4]
        self.id_inv = registro[5]

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

def tienda(request, cat):
    categorias = []
    productos = []
    categ = "Todos los productos"
    categoriasSQL = None
    productosSQL = None

    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM categoria;")
        categoriasSQL = cursor.fetchall()

        if cat == 0:
            cursor.execute("SELECT * FROM producto;")
        else:
            cursor.execute("SELECT tipo FROM categoria WHERE id_categoria=%s;",[cat])
            categ, = cursor.fetchone()
            cursor.execute("SELECT * FROM producto WHERE id_categoria=%s;",[cat])
        productosSQL = cursor.fetchall()
        
    for c in categoriasSQL:
        id, tipo = c
        categorias.append( categoria(id, tipo) )

    for p in productosSQL:
        productos.append( producto(p) )
    
    return render(request, 'categoria.html',{'categoria':categ,'categorias':categorias, 'productos':productos})

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
