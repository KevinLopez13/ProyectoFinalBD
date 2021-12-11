from django.shortcuts import render, redirect
from django.db import connection
from django.contrib import messages

from .models import *

miCarrito = carrito()

# Create your views here.

def home(request):
    return render(request,'home.html')

def formularioCliente(request):
    nombre = request.post['txtNombre']
    apP = request.post['txtApP']
    apM = request.post['txtApM']
    rfc = request.post['txtRFC']
    correo = request.post['emCorreo']
    calle = request.post['txtCalle']
    colonia = request.post['txtColonia']
    estado = request.post['txtEstado']
    cp = request.post['txtCP']
    with connection.cursor() as cursor:
        cursor.execute("INSERT INTO cliente VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s);",
                    [rfc, nombre, apP, apM, cp, num])
                    
    return render(request,'formularioCliente.html')

def herramientas(request):
    return render(request,'herramientas.html')

# Utilidad
def utilidadProducto(request):
    return render(request, 'utilidadProducto.html')

def calculaUtilidad(request):
    codigo = int(request.POST['txtCodBarras'])
    consultaSQL = None
    desc = None
    with connection.cursor() as cursor:
        cursor.execute("SELECT retorna_Utilidad(%s);",[codigo])
        consultaSQL = cursor.fetchone()
        cursor.execute("SELECT descripcion FROM producto WHERE cod_Barras=%s;",[codigo])
        desc = cursor.fetchone()
    util, = consultaSQL
    
    if util != None:
        desc, = desc
        return render(request, 'utilidadProducto.html',{'codigo':codigo,'descripcion':desc,'utilidad':util})
    else:
        return render(request, 'utilidadProducto.html')
    

# 
def analisisVentas(request):
    return render(request, 'analisisVentas.html')

# Productos que tengan menos de 3 en stock
def revisionInventario(request):
    consultaSQL = None
    productos = []
    with connection.cursor() as cursor:
        cursor.execute("SELECT menos_Thr();")
        consultaSQL = cursor.fetchall()

    for p in consultaSQL:
        reg, = p
        tup = tuple(reg[1:-1].replace('"','').split(','))
        prod = type('Producto', (object, ), dict(stock = tup[0], marca = tup[1], desc = tup[2]))
        productos.append(prod)

    return render(request, 'revInventario.html',{'productos':productos})

# Modulos del carrito 
def carrito(request):
    productos = []

    return render(request, 'carrito.html')

# Agregar al carrito
def adgregarCarrito(request, codigo):
    miCarrito.append(codigo)

    return redirect('/miCarrito')

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
        catObj = type('Categoria', (object, ), dict(id = c[0], tipo = c[1]))
        categorias.append( catObj )

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
