--Retornar info del producto que haya menos de 3 en stock
CREATE OR REPLACE FUNCTION menos_Thr() RETURNS TABLE (stock integer, marca varchar, descripcion varchar)
AS $$
DECLARE
v_stock integer;
nom_Marca varchar(120);
BEGIN
RETURN QUERY EXECUTE
'SELECT stock, marca, descripcion FROM guarda LEFT JOIN producto
ON guarda.cod_Barras=producto.cod_Barras 
WHERE stock <= 3';
END;
$$
LANGUAGE plpgsql;

--Vista tipo factura
CREATE VIEW FACTURA
AS 
SELECT Cliente.RFC, Cliente.nombre, Cliente.ap_Paterno, Cliente.ap_Materno, Cliente.cp, 
Cliente.calle, Cliente.colonia, Venta.id_Venta, Venta.fecha_Venta, Venta.pago_Final, 
Contiene.precio_Total_Art, Contiene.cantidad_Articulo, Producto.marca, Producto.descripcion FROM CLIENTE 
INNER JOIN VENTA ON CLIENTE.RFC=VENTA.RFC INNER JOIN CONTIENE ON VENTA.id_Venta=CONTIENE.id_Venta 
INNER JOIN PRODUCTO ON CONTIENE.cod_Barras=PRODUCTO.cod_Barras;

--Indice de venta
CREATE INDEX id_Vent ON VENTA(id_Venta);

--Secuencia para id_Vent
CREATE SEQUENCE Vent
START WITH 0
INCREMENT BY 1
MINVALUE 0
MAXVALUE 10
CYCLE;

--Modificaciones a la tabla venta
ALTER TABLE Venta ALTER id_Venta SET DEFAULT NEXTVAL('Vent');
ALTER TABLE Venta ALTER fecha_Venta SET DEFAULT current_date;

--Procedimiento para verificar stock
CREATE OR REPLACE FUNCTION existe() RETURNS TRIGGER AS $existe$
DECLARE decremento integer;
BEGIN 
decremento= new.cantidad_Articulo;
IF (select stock FROM guarda WHERE cod_Barras = NEW.cod_Barras) < decremento THEN 
raise notice 'No hay suficiente producto';
ROLLBACK; 
RETURN stock;
END IF;
IF (select stock FROM guarda where cod_Barras = NEW.cod_Barras ) >= decremento THEN
UPDATE guarda SET stock= ((SELECT stock FROM guarda WHERE cod_Barras=             NEW.cod_Barras) - decremento) WHERE cod_Barras = NEW.cod_Barras;
IF (select stock FROM guarda where  cod_Barras = NEW.cod_Barras ) <= 3 THEN
raise notice 'stock actualizado, REVISE SU INVENTARIO';
END IF;
RETURN NULL;
END IF; 
RETURN NULL;
END;
$existe$ LANGUAGE plpgsql;

CREATE TRIGGER existe AFTER INSERT
ON CONTIENE FOR EACH ROW
EXECUTE PROCEDURE existe();

--FUNTCION para la utilidad de cada producto
CREATE OR REPLACE FUNCTION retorna_Utilidad(codigo INT)RETURNS DECIMAL(7,2) AS
$$
DECLARE
v_Cod_Barras INT;
v_Utilidad DECIMAL(7,2);
BEGIN
SELECT Guarda.cod_Barras, SUM(precio-precio_Compra) INTO v_Cod_Barras, v_Utilidad FROM Guarda 
INNER JOIN Producto
ON Producto.cod_Barras = Guarda.cod_Barras
WHERE Guarda.cod_Barras = codigo
GROUP BY Guarda.cod_Barras;
RETURN v_Utilidad;
END;
$$
LANGUAGE plpgsql;

--FUNCTION para retornar los pagos finales
CREATE OR REPLACE FUNCTION retorna_Pago_Final(fecha DATE)RETURNS DECIMAL(7,2) AS
$$
DECLARE
v_Pago DECIMAL(7,2);
v_Fecha DATE;
BEGIN
SELECT fecha_Venta, SUM(pago_Final) INTO v_Fecha, v_Pago FROM Venta
WHERE fecha_Venta = fecha
GROUP BY fecha_Venta;
RETURN v_Pago;
END;
$$
LANGUAGE plpgsql;

--FUNCTION para retornar los pagos finales entre fechas
CREATE OR REPLACE FUNCTION retorna_Pago_Final(fecha_inicio DATE, fecha_fin DATE)RETURNS DECIMAL(7,2) AS
$$
DECLARE
v_Pago DECIMAL(7,2);
BEGIN
SELECT SUM(pago_Final) INTO v_Pago FROM Venta
WHERE fecha_Venta BETWEEN fecha_inicio AND fecha_fin;
RETURN v_Pago;
END;
$$
LANGUAGE plpgsql;

--FUNCTION para retornar las ganancias
CREATE OR REPLACE FUNCTION retorna_Pago_Ganancia(fecha DATE)RETURNS DECIMAL(7,2) AS
$$
DECLARE
v_Pago DECIMAL(7,2);
v_Bruto DECIMAL(7,2);
v_Ganancia DECIMAL(7,2);
BEGIN
SELECT SUM(pago_Final), SUM(precio_Compra*cantidad_articulo) 
INTO v_Pago, v_Bruto FROM Venta 
INNER JOIN (Contiene INNER JOIN (Producto INNER JOIN Guarda ON Producto.cod_Barras = Guarda.cod_Barras)
ON Contiene.cod_Barras = Producto.cod_Barras)
ON Venta.id_Venta = Contiene.id_Venta
WHERE Venta.fecha_venta = fecha;
v_Ganancia = v_Pago - v_Bruto;
RETURN v_Ganancia;
END;
$$
LANGUAGE plpgsql;

--FUNCTION para retornar las ganancias por fechas
CREATE OR REPLACE FUNCTION retorna_Pago_Ganancia(fecha_inicio DATE, fecha_fin DATE)RETURNS DECIMAL(7,2) AS
$$
DECLARE
v_Pago DECIMAL(7,2);
v_Bruto DECIMAL(7,2);
v_Ganancia DECIMAL(7,2);
BEGIN
SELECT SUM(pago_Final), SUM(precio_Compra*cantidad_articulo) 
INTO v_Pago, v_Bruto FROM Venta 
INNER JOIN (Contiene 
INNER JOIN (Producto 
INNER JOIN Guarda ON Producto.cod_Barras = Guarda.cod_Barras)
ON Contiene.cod_Barras = Producto.cod_Barras)
ON Venta.id_Venta = Contiene.id_Venta
WHERE Venta.fecha_Venta BETWEEN fecha_inicio AND fecha_fin;
v_Ganancia = v_Pago - v_Bruto;
RETURN v_Ganancia;
END;
$$
LANGUAGE plpgsql;

--Llamada de funciones
SELECT retorna_Utilidad(53204);

SELECT menos_Thr();

SELECT * FROM FACTURA WHERE RFC = 'GEC85014014I2';

SELECT retorna_Pago_Final('2021-10-24');
SELECT retorna_Pago_Final('2021-10-20','2021-11-30');

SELECT retorna_Pago_Ganancia('2021-11-24');
SELECT retorna_Pago_Ganancia('2021-10-20','2021-10-30');

INSERT INTO CONTIENE VALUES (53205,004,9500.50,3);

INSERT INTO Venta(pago_final,RFC) VALUES(9500.50, 'GEC85014014I1');