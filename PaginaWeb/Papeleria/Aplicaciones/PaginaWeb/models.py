from django.db import models

# Create your models here.

class producto():
    def __init__(self, codigo, precio, marca, desc, id_inv, id_cat):
        self.codigo = int(codigo)
        self.precio = float(precio)
        self.marca = marca
        self.desc = desc
        self.id_inv = int(id_inv)
        self.id_cat = int(id_cat)



class venta():
    def __init__(self, id_Venta, rfc):
        self.id_venta = id_Venta
        self.fecha_Venta = None
        self.pago_Final = None
        self.rfc = rfc

class contiene():
    def __init__(self):
        self.codigo = None
        self.id_Venta = None
        self.precio_Total_Art = {}
        self.cantidad_Articulo = {}

class carrito():
    def __init__(self):
        self.canasta = {}
        self.venta = None

    def append(self, codigo):
        if len(self.canasta) < 3:
            if codigo not in self.canasta:
                self.canasta[codigo] = 1
            else:
                self.canasta[codigo] = self.canasta.get(codigo) + 1

    def updateCantidad(self, codigo, cant):
        self.canasta[codigo] = cant

    def remove(self, codigo):
        del self.canasta[codigo]

    def sell(self):
        pass

    def __str__(self):
        return str(self.canasta)

    