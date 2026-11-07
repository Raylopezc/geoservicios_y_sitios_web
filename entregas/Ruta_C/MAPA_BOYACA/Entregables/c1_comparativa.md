# C1. Estándares y servicios geográficos

## 1. Introducción

El presente documento registra los resultados de los ejercicios
prácticos desarrollados en el componente C1 de la Ruta C,
orientados al reconocimiento y consulta de servicios geográficos
mediante estándares y tecnologías de publicación de información
espacial.

Se analizaron tres servicios:

- Web Map Service (WMS) del DANE.
- ArcGIS FeatureServer para información de veredas de Boyacá.
- OGC API – Features mediante la plataforma pygeoapi.

El propósito es identificar sus características, capacidades
de consulta, formatos de respuesta y posibilidades de utilización
en aplicaciones de Sistemas de Información Geográfica (SIG).

## 2. Ejercicio 1. Consulta del servicio WMS del DANE

### 2.1. Servicio consultado

Institución: Departamento Administrativo Nacional de Estadística (DANE).

Servicio: MGN2024 - Serv_CapasMGN_2024.

Operación consultada: GetCapabilities.

### 2.2. Resultados

Se identificaron 10 capas consultables:

| Código | Capa |
|---|---|
| 0 | Manzana |
| 1 | Sección Urbana |
| 2 | Sector Urbano |
| 3 | Sección Rural |
| 4 | Sector Rural |
| 5 | Clase |
| 6 | Zona Urbana |
| 7 | Municipio |
| 8 | Departamento |
| 9 | País |

La capa denominada Serv_CapasMGN_2024 corresponde a una
capa agrupadora y no se contabiliza como una capa consultable.

### 2.3. Sistemas de referencia identificados

Durante la consulta se identificaron los siguientes CRS:

- CRS:84
- EPSG:4326
- EPSG:3857
- EPSG:102100

EPSG:3857 y EPSG:102100 corresponden a referencias de
Web Mercator.

### 2.4. Formatos GetMap identificados

Se identificaron nueve formatos de respuesta:

- image/bmp
- image/jpeg
- image/tiff
- image/png
- image/png8
- image/png24
- image/png32
- image/gif
- image/svg+xml

Es importante diferenciar los formatos de la operación
GetMap de los formatos disponibles para GetFeatureInfo.

### 2.5. Interpretación

El servicio WMS permite visualizar información geográfica
mediante imágenes cartográficas generadas por un servidor.

Su principal utilidad consiste en integrar información
cartográfica en aplicaciones SIG y visores web sin requerir
necesariamente la descarga de las geometrías originales.

## 3. Ejercicio 2. Consulta de ArcGIS FeatureServer

### 3.1. Servicio consultado

Servicio: Veredas_Boyaca_2024.

Capa consultada: FeatureServer/0.

Operación: Query.

Formato solicitado: GeoJSON.

Se realizó una consulta solicitando tres entidades geográficas.

### 3.2. Resultados obtenidos

Se identificaron tres registros correspondientes al municipio
de Tunja, departamento de Boyacá.

| Vereda | Código | Municipio | Área (ha) |
|---|---|---|---:|
| LA LAJITA | 15001004 | Tunja | 242.1036 |
| LA HOYA | 15001003 | Tunja | 809.7410 |
| BARON | 15001000 | Tunja | 1185.2031 |

En los registros consultados se identificaron los siguientes
atributos:

- Nombre de la vereda.
- Código de la vereda.
- Municipio.
- Departamento.
- Vigencia.
- Fuente.
- Área en hectáreas.
- Observaciones.

Los tres registros consultados presentan geometría de tipo
Polygon.

### 3.3. Observaciones sobre los datos

Los registros consultados indican vigencia 2012 y fuente
Catastro IGAC, aunque el nombre del servicio corresponde
a Veredas_Boyaca_2024.

Esta diferencia debe considerarse al evaluar la actualidad
y procedencia de la información.

La respuesta también presentó el indicador
exceededTransferLimit: true, por lo que no debe asumirse
que la consulta de tres registros representa la totalidad
de entidades disponibles.

### 3.4. Interpretación

ArcGIS FeatureServer permite consultar entidades geográficas
y recuperar simultáneamente sus geometrías y atributos.

A diferencia de un servicio WMS, permite acceder a información
vectorial que puede ser utilizada en procesos de análisis,
filtrado, consulta y representación espacial.

## 4. Ejercicio 2. Consulta de OGC API – Features mediante pygeoapi

### 4.1. Servicio consultado

Plataforma: pygeoapi.

Colección: lakes.

Nombre: Large Lakes.

Operación: consulta de elementos (items).

Formato solicitado: GeoJSON.

Parámetro de consulta: limit=3.

### 4.2. Resultados obtenidos

La consulta devolvió tres entidades geográficas:

| ID | Nombre | Tipo de geometría |
|---:|---|---|
| 0 | Lake Baikal | Polygon |
| 1 | Lake Winnipeg | Polygon |
| 2 | Great Slave Lake | Polygon |

Se identificaron atributos como:

- id
- scalerank
- name
- name_alt
- admin
- featureclass

Las tres entidades corresponden a polígonos que representan
superficies de lagos.

### 4.3. Sistema de referencia

La colección declara como sistema de referencia espacial
OGC CRS84.

Las coordenadas se presentan como pares de longitud
y latitud.

### 4.4. Paginación

La respuesta presentó los siguientes resultados:

| Campo | Valor | Interpretación |
|---|---:|---|
| numberMatched | 25 | Total de entidades coincidentes |
| numberReturned | 3 | Entidades entregadas en la respuesta |

Adicionalmente, se identificó un enlace con la relación
next, que permite consultar los siguientes registros
mediante el parámetro offset.

### 4.5. Interpretación

OGC API – Features permite consultar entidades geográficas
individuales mediante solicitudes web.

La estructura de respuesta GeoJSON facilita la integración
con aplicaciones SIG, herramientas de programación y
visores cartográficos web.

La paginación permite controlar la cantidad de registros
recibidos y facilita el acceso a colecciones de mayor tamaño.

## 5. Comparación de los servicios geográficos

| Característica | WMS DANE | ArcGIS FeatureServer | OGC API – Features |
|---|---|---|---|
| Tecnología | OGC WMS | API REST de ArcGIS | Estándar OGC |
| Información principal | Imágenes cartográficas | Entidades vectoriales | Entidades vectoriales |
| Operación consultada | GetCapabilities | Query | Collections / Items |
| Geometrías disponibles | No se entregan como entidades en GetMap | Sí | Sí |
| Atributos | Consulta adicional mediante GetFeatureInfo | Sí | Sí |
| Formato observado | Imágenes | GeoJSON | GeoJSON |
| Paginación | No aplica de la misma manera | Parámetros de consulta y límites del servicio | limit y offset |
| Organización | Capas | Capas del servicio | Colecciones |

## 6. Análisis comparativo

Los ejercicios permitieron reconocer diferencias importantes
entre los servicios de publicación de información geográfica.

WMS está orientado principalmente a la visualización
cartográfica. Su funcionamiento permite solicitar mapas
representados como imágenes, lo que resulta útil para
integrar cartografía de diferentes instituciones en
visores geográficos.

ArcGIS FeatureServer ofrece acceso a entidades vectoriales,
incluyendo sus geometrías y atributos. Esta característica
permite desarrollar consultas y utilizar los datos en
procesos de análisis espacial.

Por su parte, OGC API – Features proporciona un mecanismo
estandarizado para consultar entidades geográficas mediante
colecciones y elementos. Su estructura permite recuperar
información en formatos como GeoJSON y realizar consultas
paginadas.

En consecuencia, la selección del servicio depende de la
finalidad del proyecto: visualización cartográfica,
consulta de entidades o integración de información
vectorial en aplicaciones geoespaciales.

## 7. Conclusiones

1. Los servicios geográficos permiten acceder y compartir
   información espacial mediante interfaces web.

2. WMS es especialmente útil para visualizar información
   cartográfica sin necesidad de descargar las geometrías
   de las capas.

3. ArcGIS FeatureServer permite consultar entidades
   vectoriales y recuperar sus atributos y geometrías.

4. OGC API – Features facilita el acceso estandarizado
   a colecciones de entidades geográficas mediante
   solicitudes web.

5. GeoJSON constituye un formato útil para intercambiar
   información vectorial e integrarla en aplicaciones
   SIG y visores web.

6. La paginación es una funcionalidad importante para
   controlar la transferencia de información y consultar
   colecciones de mayor tamaño.

7. Es necesario revisar la procedencia, vigencia,
   sistema de referencia y calidad de los datos antes
   de incorporarlos en análisis geoespaciales.

## 8. Evidencias de los ejercicios

Se deberán incorporar las siguientes evidencias:

- Consulta GetCapabilities del servicio WMS del DANE.
- Respuesta GeoJSON del FeatureServer de veredas de Boyacá.
- Catálogo de colecciones de pygeoapi.
- Consulta de los tres elementos de la colección lakes.

## 9. Observación final

Este documento consolida los resultados de las consultas
realizadas durante el componente C1. Los resultados
corresponden a las respuestas observadas en los servicios
consultados y no constituyen una evaluación exhaustiva
de su disponibilidad o rendimiento.
    C:\Users\Ray Lopez\servicios-sig\servicios_sig_y_websites
    