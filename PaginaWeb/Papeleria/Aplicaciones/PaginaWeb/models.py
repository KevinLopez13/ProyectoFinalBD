from django.db import models

# Create your models here.

class producto():
    def __init__(self, registro) -> None:
        self.codigo = registro[0]
        self.precio = registro[1]
        self.marca = registro[2]
        self.descripcion = registro[3]
        self.id_cat = registro[4]

class carrito():
    def __init__(self):
        self.canasta = {}
        self.venta = None

    def append(self, codigo, precio, desc):
        if codigo not in self.canasta:
            if len(self.canasta) < 3:
                self.canasta[codigo] = [1, precio, desc]
        else:
            li = self.canasta.get(codigo)
            li[0] = li[0]+1
            self.canasta[codigo] = li

    def updateCantidad(self, codigo, cant):
        self.canasta[codigo] = cant

    def remove(self, codigo):
        if codigo in self.canasta:
            del self.canasta[codigo]
    
    def drop(self):
        self.canasta.clear()

    def compra(self):
        precioT = 0
        for pr, li in self.canasta.items():
            print("Soy p", li)
            precioT = precioT + (li[0]*li[1])
        return precioT

    def __str__(self):
        return str(self.canasta)
