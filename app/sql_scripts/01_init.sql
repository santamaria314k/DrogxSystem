-- ============================================================
--  Script de inicialización — se ejecuta automáticamente
--  cuando el contenedor MySQL se crea por primera vez
-- ============================================================

USE gestion_productos;

-- ── CATÁLOGOS ────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS ROL (
    idrol     BIGINT NOT NULL,
    nombrerol TEXT   NOT NULL,
    PRIMARY KEY (idrol)
);

CREATE TABLE IF NOT EXISTS UNIDADMEDIDA (
    id_unidad          BIGINT NOT NULL,
    descripcion_unidad TEXT   NOT NULL,
    PRIMARY KEY (id_unidad)
);

CREATE TABLE IF NOT EXISTS VIAADMINISTRACION (
    id_via          BIGINT NOT NULL,
    descripcion_via TEXT   NOT NULL,
    PRIMARY KEY (id_via)
);

CREATE TABLE IF NOT EXISTS VIGENCIA (
    id_vigencia          BIGINT NOT NULL,
    descripcion_vigencia TEXT   NOT NULL,
    PRIMARY KEY (id_vigencia)
);

CREATE TABLE IF NOT EXISTS LABORATORIO (
    id_laboratorio BIGINT NOT NULL,
    nombre         TEXT   NOT NULL,
    PRIMARY KEY (id_laboratorio)
);

-- ── TABLAS PRINCIPALES ────────────────────────────────────────
CREATE TABLE IF NOT EXISTS USUARIO (
    idusuario BIGINT NOT NULL,
    username  TEXT   NOT NULL,
    password  TEXT   NOT NULL,
    rol       BIGINT NOT NULL,
    PRIMARY KEY (idusuario),
    CONSTRAINT fk_usuario_rol FOREIGN KEY (rol) REFERENCES ROL (idrol)
        ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS PRODUCTO (
    id_producto      BIGINT    NOT NULL,
    nombre_producto  TEXT      NOT NULL,
    cantidad         INT       NOT NULL DEFAULT 0,
    id_unidad        BIGINT    NOT NULL,
    id_via           BIGINT    NOT NULL,
    expediente       INT,
    fechaexpedicion  TIMESTAMP NULL,
    id_vigencia      BIGINT    NOT NULL,
    id_laboratorio   BIGINT    NOT NULL,
    PRIMARY KEY (id_producto),
    CONSTRAINT fk_prod_unidad  FOREIGN KEY (id_unidad)      REFERENCES UNIDADMEDIDA (id_unidad)        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_prod_via     FOREIGN KEY (id_via)         REFERENCES VIAADMINISTRACION (id_via)      ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_prod_vig     FOREIGN KEY (id_vigencia)    REFERENCES VIGENCIA (id_vigencia)          ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_prod_lab     FOREIGN KEY (id_laboratorio) REFERENCES LABORATORIO (id_laboratorio)    ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS INVENTARIO (
    id_inventario BIGINT    NOT NULL,
    id_producto   BIGINT    NOT NULL,
    cantidad      INT       NOT NULL DEFAULT 0,
    fechaingreso  TIMESTAMP NULL     DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id_inventario),
    CONSTRAINT fk_inv_prod FOREIGN KEY (id_producto) REFERENCES PRODUCTO (id_producto)
        ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS VENTA (
    id_venta         BIGINT    NOT NULL,
    id_producto      BIGINT    NOT NULL,
    precio_unitario  DOUBLE    NOT NULL,
    cantidad_vendida INT       NOT NULL,
    fecha_venta      TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id_venta),
    CONSTRAINT fk_venta_prod FOREIGN KEY (id_producto) REFERENCES PRODUCTO (id_producto)
        ON UPDATE CASCADE ON DELETE RESTRICT
);

-- ── DATOS DE EJEMPLO ─────────────────────────────────────────
INSERT IGNORE INTO ROL VALUES (1,'Administrador'),(2,'Farmaceutico'),(3,'Vendedor');

INSERT IGNORE INTO UNIDADMEDIDA VALUES
    (1,'Tableta'),(2,'Cápsula'),(3,'Mililitro (ml)'),(4,'Gramo (g)'),(5,'Ampolla');

INSERT IGNORE INTO VIAADMINISTRACION VALUES
    (1,'Oral'),(2,'Intravenosa'),(3,'Tópica'),(4,'Intramuscular'),(5,'Sublingual');

INSERT IGNORE INTO VIGENCIA VALUES
    (1,'Vigente'),(2,'Por vencer (menos de 3 meses)'),(3,'Vencido'),(4,'En cuarentena');

INSERT IGNORE INTO LABORATORIO VALUES
    (1,'Bayer'),(2,'Pfizer'),(3,'Genfar'),(4,'MK Laboratories'),(5,'Novartis');

INSERT IGNORE INTO USUARIO VALUES
    (1,'admin','hash_admin_123',1),
    (2,'jperez','hash_jperez_456',2),
    (3,'mgarcia','hash_mgarcia_789',3),
    (4,'lrodriguez','hash_lrod_321',2);

INSERT IGNORE INTO PRODUCTO VALUES
    (1,'Acetaminofén 500mg',500,1,1,10234,'2023-01-15',1,3),
    (2,'Amoxicilina 250mg',200,2,1,10235,'2023-03-20',1,4),
    (3,'Ibuprofeno 400mg',350,1,1,10236,'2022-11-10',2,1),
    (4,'Suero Fisiológico 0.9%',80,3,2,10237,'2023-06-01',1,2),
    (5,'Loratadina 10mg',150,1,1,10238,'2023-02-28',1,5),
    (6,'Hidrocortisona crema',60,4,3,10239,'2022-08-05',2,1),
    (7,'Diclofenaco 75mg/3ml',40,5,4,10240,'2023-07-12',1,4),
    (8,'Metformina 850mg',300,1,1,10241,'2023-05-18',1,3),
    (9,'Omeprazol 20mg',180,2,1,10242,'2021-12-30',3,2),
    (10,'Atorvastatina 20mg',120,1,1,10243,'2023-09-01',1,5);

INSERT IGNORE INTO INVENTARIO VALUES
    (1,1,200,'2023-01-16 08:00:00'),(2,1,300,'2023-03-01 09:30:00'),
    (3,2,200,'2023-03-21 10:00:00'),(4,3,350,'2022-11-11 08:45:00'),
    (5,4,80,'2023-06-02 11:00:00'),(6,5,150,'2023-03-01 08:00:00'),
    (7,6,60,'2022-08-06 09:00:00'),(8,7,40,'2023-07-13 10:30:00'),
    (9,8,300,'2023-05-19 08:00:00'),(10,9,180,'2022-01-05 07:30:00'),
    (11,10,120,'2023-09-02 08:00:00');

INSERT IGNORE INTO VENTA VALUES
    (1,1,850.00,30,'2024-01-10 10:15:00'),(2,2,1200.00,15,'2024-01-11 11:00:00'),
    (3,3,950.00,20,'2024-01-12 09:30:00'),(4,4,4500.00,5,'2024-01-13 14:00:00'),
    (5,5,600.00,25,'2024-01-14 10:45:00'),(6,6,3200.00,8,'2024-01-15 16:00:00'),
    (7,7,5800.00,6,'2024-01-16 08:30:00'),(8,8,780.00,40,'2024-01-17 11:15:00'),
    (9,1,850.00,50,'2024-01-18 09:00:00'),(10,5,600.00,30,'2024-01-19 13:30:00'),
    (11,10,2100.00,12,'2024-01-20 15:00:00'),(12,8,780.00,20,'2024-01-21 10:00:00');
