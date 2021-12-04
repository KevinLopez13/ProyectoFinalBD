SELECT fecha_Venta, SUM(pago_Final) FROM Venta
GROUP BY fecha_Venta;


SELECT fecha_Venta, SUM(pago_Final) FROM Venta
WHERE id_Venta IN (SELECT id_Venta FROM Contiene
WHERE cod_Barras IN (SELECT cod_Barras FROM Producto))
GROUP BY fecha_Venta;

--Obtencion de la venta total por fecha
SELECT fecha_Venta, SUM(pago_Final) FROM Venta
GROUP BY fecha_Venta;

--FUNCTION para retornar ganancias
CREATE OR REPLACE FUNCTION retorna_Ganancia(p_fecha DATE) RETURNS DECIMAL(7,2) AS
$$
DECLARE
   v_ganancia DECIMAL(7,2);
   v_fecha DATE;
BEGIN 
   SELECT fecha_Venta, SUM(pago_Final) INTO v_fecha, v_ganancia FROM Venta
   WHERE fecha_Venta = p_fecha
   GROUP BY fecha_Venta;
   RETURN v_ganancia;
END;
$$
LANGUAGE plpgsql;

--FUNCTION para retornar ganancias en un rango de fechas
CREATE OR REPLACE FUNCTION retorna_Ganancia(p_fecha1 DATE, p_fecha2 DATE)
RETURNS DECIMAL(7,2) AS
$$
DECLARE
   v_ganancia DECIMAL(7,2);
   v_ganancia2 DECIMAL(7,2);
   v_fecha DATE;
   v_fecha2 DATE;
BEGIN
   IF p_fecha2 IS NOT NULL THEN
      SELECT fecha_Venta, SUM(pago_Final) INTO v_fecha, v_ganancia FROM Venta
      WHERE fecha_Venta = p_fecha1
      GROUP BY fecha_Venta;
      RETURN v_ganancia;
   ELSE 
      SELECT fecha_Venta, SUM(pago_Final) INTO v_fecha2, v_ganancia2 FROM Venta
      WHERE fecha_Venta BETWEEN p_fecha1 AND p_fecha2
      GROUP BY fecha_Venta;
      RETURN v_ganancia2;
   END IF;
END;
$$
LANGUAGE plpgsql;

SELECT retorna_Ganancia('2021-10-24');
SELECT retorna_Ganancia('2021-10-24','2021-11-24');

DROP FUNCTION retorna_Ganancia(DATE);

--Declare de obtencion de ventas por fecha
DO $$
DECLARE
v_Fecha DATE := '2021-11-24';
BEGIN
SELECT fecha_Venta, SUM(pago_Final) 
INTO v_Fecha FROM Venta
WHERE fecha_Venta=v_Fecha
GROUP BY fecha_Venta;
raise notice '% pesos en la fecha %',
       SUM(pago_Final),
	   fecha_Venta;
END $$;

do $$ 
declare
   fecha    varchar(10) := '2021-11-24';
   cantidad DECIMAL(7,2) := 12359.50;
begin 
   raise notice '% peso en la fecha %',
       cantidad,
	   fecha;
end $$;