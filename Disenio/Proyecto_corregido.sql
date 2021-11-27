--
-- ER/Studio 8.0 SQL Code Generation
-- Company :      FI-UNAM
-- Project :      Proyecto.DM1
-- Author :       IsaacLopez117
--
-- Date Created : Thursday, November 25, 2021 20:40:01
-- Target DBMS : IBM DB2 UDB 8.x
--

-- 
-- TABLE: Categoria 
--

CREATE TABLE Categoria(
    id_Categoria    SMALLINT       NOT NULL,
    tipo            VARCHAR(20)    NOT NULL,
    CONSTRAINT PK10 PRIMARY KEY (id_Categoria)
);



-- 
-- TABLE: Cliente 
--

CREATE TABLE Cliente(
    RFC           VARCHAR(13)    NOT NULL,
    nombre        VARCHAR(32)    NOT NULL,
    ap_Paterno    VARCHAR(32)    NOT NULL,
    ap_Materno    VARCHAR(32),
    cp            SMALLINT       NOT NULL,
    numero        SMALLINT       NOT NULL,
    estado        VARCHAR(32)    NOT NULL,
    calle         VARCHAR(32)    NOT NULL,
    colonia       VARCHAR(32)    NOT NULL,
    CONSTRAINT PK2 PRIMARY KEY (RFC)
);


-- 
-- TABLE: Contiene 
--

CREATE TABLE Contiene(
    cod_Barras           BIGINT          NOT NULL,
    id_Venta             VARCHAR(32)          NOT NULL,
    precio_Total_Art     DECIMAL(7, 2)    NOT NULL,
    cantidad_Articulo    INTEGER          NOT NULL,
    CONSTRAINT PK4 PRIMARY KEY (cod_Barras, id_Venta)
);


-- 
-- TABLE: Email
--

CREATE TABLE Email(
    email    VARCHAR(64)    NOT NULL,
    RFC      VARCHAR(13)    NOT NULL,
    CONSTRAINT PK1 PRIMARY KEY (email)
);




-- 
-- TABLE: Inventario 
--

CREATE TABLE Inventario(
    id_Inventario    SMALLINT          NOT NULL,
    precio_Compra    DECIMAL(10, 2)    NOT NULL,
    stock            SMALLINT          NOT NULL,
    fecha_Compra     DATE              NOT NULL,
    CONSTRAINT PK9 PRIMARY KEY (id_Inventario)
);


-- 
-- TABLE: Producto 
--

CREATE TABLE Producto(
    cod_Barras       BIGINT          NOT NULL,
    precio           DECIMAL(7, 2)    NOT NULL,
    marca            VARCHAR(120)     NOT NULL,
    descripcion      VARCHAR(50)      NOT NULL,
    id_Categoria     SMALLINT         NOT NULL,
    id_Inventario    SMALLINT         NOT NULL,
    CONSTRAINT PK5 PRIMARY KEY (cod_Barras)
);


-- 
-- TABLE: Proveedor 
--

CREATE TABLE Proveedor(
    id_Proveedor    SMALLINT       NOT NULL,
    nombre          VARCHAR(50)    NOT NULL,
    razon_Social    VARCHAR(50)    NOT NULL,
    estado          VARCHAR(50)    NOT NULL,
    colonia         VARCHAR(50)    NOT NULL,
    numero          SMALLINT       NOT NULL,
    cp              SMALLINT       NOT NULL,
    calle           VARCHAR(50)    NOT NULL,
    CONSTRAINT PK7 PRIMARY KEY (id_Proveedor)
);



-- 
-- TABLE: Surte 
--

CREATE TABLE Surte(
    id_Proveedor     SMALLINT    NOT NULL,
    id_Inventario    SMALLINT    NOT NULL,
    CONSTRAINT PK8 PRIMARY KEY (id_Proveedor, id_Inventario)
);


-- 
-- TABLE: Telefono 
--

CREATE TABLE Telefono(
    num_Telefono    BIGINT      NOT NULL,
    id_Proveedor    SMALLINT    NOT NULL,
    CONSTRAINT PK6 PRIMARY KEY (num_Telefono)
);


-- 
-- TABLE: Venta 
--

CREATE TABLE Venta(
    id_Venta       VARCHAR (32)          NOT NULL,
    fecha_Venta    DATE             NOT NULL,
    pago_Final     DECIMAL(7, 2)    NOT NULL,
    RFC      VARCHAR(13)    NOT NULL,
    CONSTRAINT PK3 PRIMARY KEY (id_Venta)
);



-- 
-- TABLE: Contiene 
--

ALTER TABLE Contiene ADD CONSTRAINT RefVenta4 
    FOREIGN KEY (id_Venta)
    REFERENCES Venta(id_Venta)
;

ALTER TABLE Contiene ADD CONSTRAINT RefProducto5 
    FOREIGN KEY (cod_Barras)
    REFERENCES Producto(cod_Barras)
;


-- 
-- TABLE: EMAIL
--

ALTER TABLE EMAIL ADD CONSTRAINT RefCliente2 
    FOREIGN KEY (RFC)
    REFERENCES Cliente(RFC)
;


-- 
-- TABLE: Producto 
--

ALTER TABLE Producto ADD CONSTRAINT RefInventario9 
    FOREIGN KEY (id_Inventario)
    REFERENCES Inventario(id_Inventario)
;

ALTER TABLE Producto ADD CONSTRAINT RefCategoria10 
    FOREIGN KEY (id_Categoria)
    REFERENCES Categoria(id_Categoria)
;


-- 
-- TABLE: Surte 
--

ALTER TABLE Surte ADD CONSTRAINT RefProveedor6 
    FOREIGN KEY (id_Proveedor)
    REFERENCES Proveedor(id_Proveedor)
;

ALTER TABLE Surte ADD CONSTRAINT RefInventario7 
    FOREIGN KEY (id_Inventario)
    REFERENCES Inventario(id_Inventario)
;


-- 
-- TABLE: Telefeno 
--

ALTER TABLE Telefono ADD CONSTRAINT RefProveedor8 
    FOREIGN KEY (id_Proveedor)
    REFERENCES Proveedor(id_Proveedor)
;


-- 
-- TABLE: Venta 
--

ALTER TABLE Venta ADD CONSTRAINT RefCliente3 
    FOREIGN KEY (RFC)
    REFERENCES Cliente(RFC)
;


