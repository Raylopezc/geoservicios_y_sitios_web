
-- ============================================================
-- CAPITULO 03. POSTGRESQL Y POSTGIS
-- Ejercicio: analisis espacial de ciudades de Colombia
-- Base de datos: taller_gis
-- Sistema de referencia: EPSG:4326
-- Autor: Ray Lopez
-- Fecha: 06/11/2026
--
-- Script consolidado y seguro para ejecuciones repetidas.
-- No elimina las tablas ni los registros existentes.
-- ============================================================


-- ============================================================
-- ACTIVIDAD 1. VERIFICACION DE POSTGIS
-- ============================================================

SELECT version();

SELECT PostGIS_Full_Version();


-- ============================================================
-- ACTIVIDAD 2. CREACION DE LA TABLA CIUDADES
-- ============================================================

CREATE TABLE IF NOT EXISTS public.ciudades (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    poblacion INTEGER,
    geom GEOMETRY(POINT, 4326)
);


-- ============================================================
-- ACTIVIDAD 3. INSERCION DE CIUDADES
-- ============================================================

INSERT INTO public.ciudades (nombre, poblacion, geom)
SELECT v.nombre, v.poblacion,
       ST_SetSRID(ST_MakePoint(v.longitud, v.latitud), 4326)
FROM (VALUES
    ('Bogotá', 7181469, -74.0721, 4.7110),
    ('Medellín', 2508452, -75.5636, 6.2442),
    ('Cali', 2227642, -76.5225, 3.4516),
    ('Barranquilla', 1232766, -74.7813, 10.9685),
    ('Cartagena', 1028736, -75.5144, 10.3910),
    ('Montería', NULL, -75.8814, 8.74798)
) AS v(nombre, poblacion, longitud, latitud)
WHERE NOT EXISTS (
    SELECT 1
    FROM public.ciudades c
    WHERE c.nombre = v.nombre
);


-- Verificar registros de ciudades

SELECT
    id,
    nombre,
    poblacion,
    ST_AsText(geom) AS coordenadas,
    ST_SRID(geom) AS srid
FROM public.ciudades
ORDER BY id;


-- ============================================================
-- ACTIVIDAD 4. CALCULO DE DISTANCIAS ENTRE CIUDADES
-- ============================================================

SELECT
    c1.nombre AS ciudad_origen,
    c2.nombre AS ciudad_destino,
    ROUND(
        (ST_Distance(
            c1.geom::geography,
            c2.geom::geography
        ) / 1000)::numeric, 2
    ) AS distancia_km
FROM public.ciudades c1
JOIN public.ciudades c2
    ON c1.id < c2.id
ORDER BY distancia_km;


-- ============================================================
-- ACTIVIDAD 5. CREACION Y ANALISIS DEL BUFFER DE MONTERIA
-- ============================================================

CREATE TABLE IF NOT EXISTS public.buffer_monteria (
    ciudad_id INTEGER,
    nombre VARCHAR(100),
    distancia_metros INTEGER,
    geom GEOMETRY(Polygon, 4326)
);


-- Insertar buffer de 200 kilometros si aun no existe

INSERT INTO public.buffer_monteria (
    ciudad_id,
    nombre,
    distancia_metros,
    geom
)
SELECT
    c.id,
    c.nombre,
    200000,
    ST_Buffer(c.geom::geography, 200000)::geometry(Polygon, 4326)
FROM public.ciudades c
WHERE c.nombre = 'Montería'
AND NOT EXISTS (
    SELECT 1
    FROM public.buffer_monteria b
    WHERE b.nombre = 'Montería'
);


-- Consultar area y perimetro del buffer

SELECT
    nombre,
    distancia_metros,
    ROUND(
        (ST_Area(geom::geography) / 1000000)::numeric, 2
    ) AS area_km2,
    ROUND(
        (ST_Perimeter(geom::geography) / 1000)::numeric, 2
    ) AS perimetro_km,
    ST_IsValid(geom) AS geometria_valida
FROM public.buffer_monteria;


-- Verificar tipo de geometria y SRID

SELECT
    nombre,
    ST_GeometryType(geom) AS tipo_geometria,
    ST_SRID(geom) AS srid,
    ST_IsValid(geom) AS geometria_valida
FROM public.buffer_monteria;


-- ============================================================
-- ACTIVIDAD 6. CONSULTA Y TRANSFORMACION DE SRID
-- ============================================================

-- Consultar sistemas de referencia disponibles

SELECT
    srid,
    auth_name,
    srtext
FROM public.spatial_ref_sys
WHERE srid IN (4326, 3857, 9377, 3116);


-- Transformar coordenadas de EPSG:4326 a EPSG:3857

SELECT
    nombre,
    ST_SRID(geom) AS srid_original,
    ST_AsText(geom) AS coordenadas_originales,
    ST_AsText(ST_Transform(geom, 3857))
        AS coordenadas_transformadas,
    ST_SRID(ST_Transform(geom, 3857))
        AS srid_destino
FROM public.ciudades
ORDER BY nombre;


-- Verificar geometrias de las ciudades

SELECT
    nombre,
    ST_GeometryType(geom) AS tipo_geometria,
    ST_SRID(geom) AS srid,
    ST_IsValid(geom) AS geometria_valida
FROM public.ciudades;


-- ============================================================
-- ACTIVIDAD 7. CREACION Y VERIFICACION DEL INDICE ESPACIAL
-- ============================================================

-- Crear indice espacial GiST

CREATE INDEX IF NOT EXISTS idx_ciudades_geom
ON public.ciudades
USING GIST (geom);


-- Actualizar estadisticas de la tabla

ANALYZE public.ciudades;


-- Consultar indices existentes

SELECT
    indexname,
    indexdef
FROM pg_indexes
WHERE schemaname = 'public'
AND tablename = 'ciudades';


-- Consultar estadisticas del indice espacial

SELECT
    indexrelname AS nombre_indice,
    idx_scan AS consultas_realizadas,
    idx_tup_read AS registros_leidos,
    idx_tup_fetch AS registros_recuperados
FROM pg_stat_user_indexes
WHERE relname = 'ciudades';


-- ============================================================
-- VALIDACION FINAL
-- ============================================================

-- Total de ciudades

SELECT COUNT(*) AS total_ciudades
FROM public.ciudades;


-- Validacion de geometrias de ciudades

SELECT
    COUNT(*) AS total_geometrias,
    COUNT(*) FILTER (WHERE ST_IsValid(geom)) AS geometrias_validas,
    COUNT(*) FILTER (WHERE ST_SRID(geom) = 4326) AS geometrias_srid_4326
FROM public.ciudades;


-- Validacion del buffer de Monteria

SELECT
    COUNT(*) AS total_buffers,
    COUNT(*) FILTER (WHERE ST_IsValid(geom)) AS buffers_validos
FROM public.buffer_monteria;


-- FIN DEL SCRIPT
-- ============================================================
