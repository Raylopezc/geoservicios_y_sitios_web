# VISOR GEOGRÁFICO DE COLOMBIA

## Proyecto final – Taller de Servicios Web Geográficos

Aplicación web para visualizar y consultar información geográfica de los departamentos y municipios de Colombia mediante servicios geográficos web.

## 1. Descripción general

El proyecto integra una base de datos espacial PostgreSQL/PostGIS, un servidor GeoServer y una aplicación web desarrollada con HTML, CSS, JavaScript y Leaflet.

La aplicación permite visualizar las capas de departamentos y municipios sobre un mapa base de OpenStreetMap, activar o desactivar las capas y consultar información de sus entidades mediante interacción con el mapa.

## 2. Objetivo general

Implementar un visor geográfico web que permita visualizar y consultar información espacial de los departamentos y municipios de Colombia mediante servicios geográficos publicados desde GeoServer.

## 3. Tecnologías utilizadas

| Tecnología | Función |
|---|---|
| PostgreSQL | Sistema gestor de base de datos |
| PostGIS | Administración de información espacial |
| GeoServer 2.25.3 | Publicación de servicios geográficos |
| WMS | Visualización de capas geográficas |
| WFS | Consulta y recuperación de entidades |
| Leaflet 1.9.4 | Biblioteca de mapas web |
| HTML5 | Estructura de la aplicación |
| CSS3 | Diseño de la interfaz |
| JavaScript | Lógica e interacción |
| OpenStreetMap | Mapa base |

## 4. Arquitectura del proyecto

La solución se compone de los siguientes elementos:

1. Base de datos espacial: taller_gis.
2. Esquema de almacenamiento: public.
3. Servidor de publicación: GeoServer.
4. Espacio de trabajo: taller.
5. Servicios geográficos: WMS y WFS.
6. Cliente web: Leaflet.

### Capas publicadas

| Capa | Nombre publicado en GeoServer |
|---|---|
| Departamentos | taller:departamentos |
| Municipios | taller:Municipios |

Nota: se debe respetar la escritura exacta de los nombres de las capas.

## 5. Estructura de carpetas

```text
PROYECTO_FINAL_SERVICIOS_WEB_GEOGRAFICOS/
│
├── README.md
│
├── 01_DOCUMENTACION/
│   └── Informe_Tecnico_Visor_Geografico_Colombia.docx
│
├── 02_APLICACION_WEB/
│   ├── index.html
│   ├── css/
│   │   └── styles.css
│   ├── js/
│   │   ├── servicios.js
│   │   ├── mapa.js
│   │   ├── consultas.js
│   │   └── app.js
│   └── assets/
│
├── 03_EVIDENCIAS/
│   ├── 01_POSTGIS/
│   ├── 02_GEOSERVER/
│   ├── 03_SERVICIOS_WMS_WFS/
│   ├── 04_APLICACION/
│   ├── 05_PRUEBAS/
│   └── 06_PUBLICACION/
│
├── 04_ENTREGABLES/
│
└── 05_PUBLICACION/
```

## 6. Configuración del entorno

El entorno de servicios geográficos se ejecuta mediante Docker Compose desde la carpeta superior del repositorio de trabajo.

Servicios utilizados:

| Servicio | Dirección local |
|---|---|
| GeoServer | http://localhost:8080/geoserver |
| PostGIS | localhost:5432 |
| pg_tileserv | http://localhost:7800 |

Base de datos:
- Nombre: taller_gis
- Usuario: postgres
- Puerto: 5432

Las credenciales de acceso son de desarrollo local. No deben publicarse en repositorios públicos.

## 7. Servicios geográficos

### Servicio WMS

URL:

http://localhost:8080/geoserver/taller/wms

Función: representar las capas geográficas como imágenes cartográficas.

### Servicio WFS

URL:

http://localhost:8080/geoserver/taller/ows

Función: consultar y recuperar entidades y atributos espaciales.

### Solicitud WFS de departamentos

http://localhost:8080/geoserver/taller/ows?service=WFS&version=2.0.0&request=GetFeature&typeNames=taller:departamentos&count=5&outputFormat=application/json

### Solicitud WFS de municipios

http://localhost:8080/geoserver/taller/ows?service=WFS&version=2.0.0&request=GetFeature&typeNames=taller:Municipios&count=5&outputFormat=application/json

## 8. Ejecución de la aplicación web

### Requisitos

- Docker Desktop instalado y en ejecución.
- Node.js instalado.
- Servicios PostGIS y GeoServer activos.
- Archivos de la aplicación web disponibles.

### Procedimiento

1. Iniciar Docker Desktop.
2. Abrir PowerShell en la carpeta superior del repositorio.
3. Verificar los servicios:

```powershell
docker compose ps
```

4. Ingresar a la carpeta de la aplicación:

```powershell
cd "PROYECTO_FINAL_SERVICIOS_WEB_GEOGRAFICOS\02_APLICACION_WEB"
```

5. Iniciar el servidor web:

```powershell
npx.cmd serve . -l 3000
```

6. Abrir el navegador en:

http://localhost:3000

El servidor debe permanecer activo mientras se utiliza la aplicación.

## 9. Configuración CORS

Se habilitó el filtro CORS de Tomcat en GeoServer para permitir solicitudes desde el origen local:

http://localhost:3000

Esta configuración permite que la aplicación web consulte los servicios geográficos mediante solicitudes JavaScript.

Para una publicación en un servidor externo se debe ajustar el origen autorizado al dominio definitivo.

## 10. Pruebas realizadas

Durante el desarrollo se documentaron las siguientes verificaciones:

- Conexión a la base de datos PostGIS.
- Conteo de 66 registros de departamentos.
- Conteo de 1121 registros de municipios.
- Disponibilidad de GeoServer.
- Respuesta HTTP 200 del servicio WMS.
- Respuesta HTTP 200 del servicio WFS de departamentos.
- Respuesta HTTP 200 del servicio WFS de municipios.
- Recuperación de entidades en formato GeoJSON.
- Validación del encabezado CORS.
- Visualización de las capas en Leaflet.
- Consulta de atributos mediante interacción con el mapa.

Las solicitudes WFS de prueba recuperaron cinco entidades por capa como muestra. Esto no representa una descarga integral de todos los registros.

## 11. Alcance y limitaciones

El visor está orientado a la visualización y consulta de departamentos y municipios de Colombia.

La ejecución documentada corresponde a un entorno local. No se debe considerar que la aplicación está publicada en Internet hasta completar y verificar un despliegue externo.

Las pruebas realizadas no constituyen una auditoría integral de calidad temática, posicional o topológica de la información geográfica.

## 12. Documentación y evidencias

El informe técnico se encuentra en:

01_DOCUMENTACION/

Las evidencias de configuración, publicación y pruebas se encuentran en:

03_EVIDENCIAS/

## 13. Autoría

Proyecto académico: Visor Geográfico de Colombia.

Desarrollo realizado como proyecto final del Taller de Servicios Web Geográficos.

---

**Fin del documento.**
