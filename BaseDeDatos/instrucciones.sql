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

--FUNCTION para retornar los precios por producto
CREATE OR REPLACE FUNCTION retorna_Pago_Ganancia(fecha DATE)RETURNS DECIMAL(7,2) AS
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
WHERE Venta.fecha_venta = fecha;
v_Ganancia = v_Pago - v_Bruto;
RETURN v_Ganancia;
END;
$$
LANGUAGE plpgsql;


--Llamada de funciones
SELECT retorna_Pago_Final('2021-10-24');
SELECT retorna_Pago_Ganancia('2021-11-24');