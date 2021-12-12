from decimal import ConversionSyntax
from django.shortcuts import render, redirect
from django.db import connection
from django.contrib import messages

from .models import *

miCarrito = carrito()

# Create your views here.

def home(request):
    return render(request,'home.html')

def formularioError(request):
    return render(request, 'formularioError.html')

def formularioCliente(request):
    return render(request, 'formularioCliente.html')
 
def validaRegistroCliente(request):
    #is_private = request.POST.get('is_private', False)
    nombre = request.POST['txtNombreform']
    apP = request.POST['txtApP']
    apM = request.POST['txtApM']
    rfc = request.POST['txtRFC']
    correo = request.POST['emCorreo']
    calle = request.POST['txtCalle']
    colonia = request.POST['txtColonia']
    estado = request.POST['txtEstado']
    numero = int(request.POST.get('txtNum',False))
    cp = int(request.POST.get('txtCP',False))
    
    with connection.cursor() as cursor:
        try:
            if len(apM) != 0:
                cursor.execute("INSERT INTO cliente VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s);",
                        [rfc, nombre, apP, apM, cp, numero, estado, calle, colonia])
            else:
                cursor.execute("INSERT INTO cliente VALUES(%s,%s,%s,NULL,%s,%s,%s,%s,%s);",
                        [rfc, nombre, apP, cp, numero, estado, calle, colonia])
        
            cursor.execute("INSERT INTO correo VALUES(%s,%s);",[correo, rfc])
        except:
            cursor.execute("ROLLBACK;")
            return redirect('/formularioError')

    return redirect('/formularioCliente')

def herramientas(request):
    return render(request,'herramientas.html')

def utilidadError(request):
    return render(request, 'utilidadError.html')

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
        return redirect('/utilidadError')
    
def cancelarCompra(request):
    miCarrito.drop()
    return redirect('/miCarrito')
# 
def analisisVentas(request):
    return render(request, 'analisisVentas.html')

def analisisVentasFecha(request):
    fecha1 = request.POST['fDateS']
    fecha2 = request.POST['fDateE']
    consultaSQL = None
    desc = None
    with connection.cursor() as cursor:
        if fecha2 != '':
            cursor.execute("SELECT retorna_pago_Final(%s,%s);",[fecha1, fecha2])
        else:
            cursor.execute("SELECT retorna_pago_Final(%s);",[fecha1])
        consultaSQL = cursor.fetchone()
    ganancia, = consultaSQL
    
    if ganancia != None:
        return render(request, 'analisisVentas.html',{'fecha1':fecha1, 'fecha2':fecha2,'ganancia':ganancia})
    else:
        return redirect('/analisisVenta')   

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

def addCarrito(request, codigo):
    precio = None
    marca = None
    desc = None
    idCat = None
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM producto WHERE cod_Barras=%s;',[codigo])
        cod, precio, marca, desc, idCat = cursor.fetchone()
    precio = float(precio)

    miCarrito.append(codigo, precio, desc)
    return redirect('/tienda/0')

def carrito(request):
    productos = []
    for pr, li in miCarrito.canasta.items():
        producto = type('Prod', (object, ), dict(codigo=pr, cant=li[0], precio=li[1], desc=li[2], total=li[1]*li[0]) )
        productos.append(producto)
    
    return render(request, 'carrito.html',{'productos':productos})

def eliminar_Articulo(request, codigo):
    miCarrito.remove(codigo)
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
    
    return render(request, 'categoria.html',{'idcat':cat,'categoria':categ,'categorias':categorias, 'productos':productos})


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
        return redirect('/venta/{}'.format(rfc))
    else:
        return redirect('/clienteError')
    
def venta(request, rfc):
    pagoVenta = miCarrito.compra()
    idVenta = None
    print(pagoVenta)
    with connection.cursor() as cursor:
        cursor.execute('INSERT INTO venta(pago_final,RFC) VALUES(%s,%s);',[pagoVenta, rfc])
        cursor.execute('SELECT id_Venta_Funcion();')
        idVenta, = cursor.fetchone()

        for pr, li in miCarrito.canasta.items():
            print("Dentro for")
            pagoTotal = li[0]*li[1]
            try:
                cursor.execute('INSERT INTO contiene(cod_Barras, id_Venta, precio_Total_Art, cantidad_Articulo) VALUES(%s,%s,%s,%s);',[int(pr), int(idVenta), float(pagoTotal) , li[0]])
            except:
                cursor.execute('DELETE FROM VENTA WHERE id_Venta = %s;',[idVenta])

    miCarrito.drop()
    return redirect('/factura/{}'.format(idVenta))

def busquedaVenta(request):
    return render(request, 'busquedaVenta.html')

def busquedaError(request):
    return render(request, 'busquedaVentaError.html')

def validaVenta(request):
    idVenta = request.POST['txtidVenta']
    idVentaResponse = False
    # CONSULTA SQL
    with connection.cursor() as cursor:
        cursor.execute("SELECT id_venta FROM  venta WHERE id_venta=%s;",[idVenta])
        row = cursor.fetchone()
        if row != None:
            idVentaResponse = True

    if idVentaResponse:
        return redirect('/factura/{}'.format(idVenta))
    else:
        return redirect('/busquedaError')

def factura(request, idVenta):
    consulta = None
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM FACTURA WHERE id_venta = %s;',[idVenta])
        consulta = cursor.fetchall()
        
        c = consulta[0]
        cliente = type('Cliente', (object,), dict(rfc=c[0], nom=c[1], apP=c[2], apM=c[3], cp=c[4], calle=c[5], col=c[6]))
        venta = type('Venta', (object,), dict( id=c[7], fecha=c[8], pago=c[9] ))
        productos = []
        for p in consulta:
            prod = type('Prod',(object,), dict(precio=p[10], cant=p[11], marca=p[12], desc=p[13], preciotot=p[11]*p[10]))
            productos.append(prod)
    return render(request, 'factura.html',{'cliente':cliente,'productos':productos, 'venta':venta})

