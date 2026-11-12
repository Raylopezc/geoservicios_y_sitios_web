# Información de publicación del visor geográfico

## Estado de publicación

El visor geográfico se encuentra implementado y validado en un entorno local de desarrollo.

No se registra una publicación en un servidor público de Internet.

## Componentes necesarios

- Docker Desktop.
- Docker Compose.
- PostgreSQL con PostGIS.
- GeoServer.
- Navegador web.
- Node.js y npm para ejecutar el servidor local.

## Inicio de los servicios geográficos

Desde la carpeta superior del repositorio de trabajo:

docker compose up -d

## Inicio de la aplicación web

Desde la carpeta 02_APLICACION_WEB del proyecto:

npx.cmd serve . -l 3000

## Direcciones locales

- Aplicación web: http://localhost:3000
- GeoServer: http://localhost:8080/geoserver
- Servicio WMS: http://localhost:8080/geoserver/taller/wms
- Servicio WFS: http://localhost:8080/geoserver/taller/ows
- pg_tileserv: http://localhost:7800

## Consideraciones

Para reproducir el entorno se requieren el archivo docker-compose.yml y la configuración geoserver_config/web.xml ubicados en la carpeta superior del repositorio.

La configuración CORS está habilitada para el origen local http://localhost:3000.

Las direcciones localhost solo son accesibles desde el equipo donde se ejecutan los servicios.
