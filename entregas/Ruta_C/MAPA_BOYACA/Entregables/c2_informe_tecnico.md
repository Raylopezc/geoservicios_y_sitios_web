# INFORME TÉCNICO – RUTA C2
## Implementación de infraestructura geoespacial con PostGIS, GeoServer y pg_tileserv

**Proyecto:** Servicios SIG y sitios web  
**Componente:** C2 – Implementación del stack geoespacial  
**Área de aplicación:** Departamento de Boyacá, Colombia  
**Fecha:** Octubre de 2026

---

## 1. Introducción

El presente informe documenta la implementación y validación de una infraestructura de servicios geoespaciales mediante tecnologías de código abierto. La solución integra PostgreSQL con la extensión espacial PostGIS, GeoServer y pg_tileserv, utilizando Docker para la administración y ejecución de los servicios.

Como parte del ejercicio se incorporó información geográfica correspondiente a los municipios del departamento de Boyacá, almacenándola en una base de datos espacial y habilitando su publicación mediante servicios de teselas vectoriales.

El desarrollo permite disponer de una infraestructura básica para almacenar, administrar, consultar y visualizar información geográfica a través de servicios interoperables.

## 2. Objetivos

### 2.1. Objetivo general

Implementar y validar una infraestructura de servicios geoespaciales mediante PostGIS, GeoServer y pg_tileserv, utilizando contenedores Docker y datos geográficos del departamento de Boyacá.

### 2.2. Objetivos específicos

- Configurar una base de datos PostgreSQL con la extensión espacial PostGIS.
- Mantener operativo GeoServer como servidor de publicación de información geográfica.
- Incorporar pg_tileserv para la publicación de teselas vectoriales.
- Importar la información geográfica de los municipios de Boyacá a PostGIS.
- Verificar la integridad de los registros, las geometrías y el sistema de referencia espacial.
- Comprobar la disponibilidad de las capas mediante pg_tileserv.

## 3. Tecnologías implementadas

| Tecnología | Función | Configuración |
|---|---|---|
| Docker | Administración de contenedores | Docker Compose |
| PostgreSQL | Sistema gestor de bases de datos | Puerto 5432 |
| PostGIS | Extensión para almacenamiento y análisis espacial | PostGIS 3.4 |
| GeoServer | Publicación de servicios geográficos | Puerto 8080 |
| pg_tileserv | Publicación de teselas vectoriales | Puerto 7800 |
| GDAL/OGR | Lectura e importación de información geográfica | Contenedor GDAL |

## 4. Configuración de la infraestructura

Se utilizó Docker Compose para administrar los servicios que integran la infraestructura geoespacial.

Los contenedores implementados son:

- `curso_postgis`: administra la base de datos espacial.
- `curso_geoserver`: permite publicar servicios geográficos.
- `curso_pg_tileserv`: publica las tablas espaciales como teselas vectoriales.

La base de datos utilizada fue `taller_gis`, con el usuario `postgres`.

Los servicios se configuraron de la siguiente manera:

| Servicio | Dirección local |
|---|---|
| PostgreSQL/PostGIS | localhost:5432 |
| GeoServer | http://localhost:8080/geoserver |
| pg_tileserv | http://localhost:7800 |

Se incorporó pg_tileserv al archivo `docker-compose.yml`, conservando los servicios y volúmenes existentes.

La validación de los contenedores mediante `docker ps` permitió comprobar que los tres servicios se encontraban en ejecución. PostGIS y GeoServer reportaron estado saludable.

## 5. Incorporación de información geográfica

### 5.1. Fuente de información

Se utilizó el archivo:

`municipios_boyaca.geojson`

Ubicación:

`nivelacion/datos/municipios_boyaca.geojson`

El archivo tiene un tamaño aproximado de 11,75 MB.

### 5.2. Características de los datos

Mediante la herramienta `ogrinfo` de GDAL se verificaron las características del archivo antes de realizar su importación.

Los resultados fueron:

| Característica | Resultado |
|---|---|
| Formato | GeoJSON |
| Nombre de la capa | municipios_boyaca |
| Número de entidades | 123 |
| Tipo de geometría | Polygon |
| Sistema de referencia | EPSG:4326 |
| Coordenadas | Longitud y latitud |
| Extensión X | -74.664960 a -71.948854 |
| Extensión Y | 4.655196 a 7.055557 |

Los atributos identificados en la fuente incluyen:

- `mpio_ccdgo`
- `mpio_cnmbr`
- `dpto_cnmbr`
- `mpio_narea`

### 5.3. Importación a PostGIS

La información se incorporó a la base de datos `taller_gis`, dentro del esquema `public`, mediante la herramienta `ogr2ogr`.

La tabla resultante se denominó:

`public.municipios_boyaca`

Para la importación se definió el campo geométrico `geom` y el identificador `gid`.

La operación se realizó sin reemplazar las tablas que ya existían en la base de datos.

## 6. Validación de la información espacial

Después de la importación se ejecutaron consultas SQL para comprobar la cantidad de registros, la disponibilidad de geometrías y sus características espaciales.

### 6.1. Conteo de registros

La consulta ejecutada fue:

```sql
SELECT COUNT(*) AS total_municipios
FROM public.municipios_boyaca;
