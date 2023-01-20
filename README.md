# INAI ITAM
Proyecto de adquisición y monitoreo de datos de Google Trends para el Instituto Nacional de Acceso a la Informaación y Protección de Datos Personales, INAI. Se definireron los siguientes requisitos que debe satisfacer la API:
-   Hacer consultas histróricas con palabras clave
-   Hacer consultas en tiempo real
-   API preferentemente libre

# Pytrends
En el siguiente [enlace](https://pypi.org/project/pytrends/) se puede encontrar la documentación oficial de la API.

## Métodos de la API
Los métodos de `pytrends` típicamente utilizan los siguientes parámetros:
-   `kw_list`: Lista de pálabras clave o criterios de búsqueda
-   `cat`: Categoría para reducir resultados
-   `geo`: Abrebiación de dos letras de un país.
-   `tz`: Offset de zona horaria en minutos, para más información ir a la [liga](https://en.wikipedia.org/wiki/UTC_offset)
-   `timeframe`: Ventana de tiempo de consulta
-   `gprop`: (Metadato) Propiedad de google que se quiere filtrar

Y permite consultar información a través de los siguientes métodos:

`Interés en el tiempo`

>Regresa datos históricos indexados para los momentos en los que los criterios de búsqueda, definidos en `kw_list`, tuvieron una mayor cantidad de búsquedas.
>
>**IMPORTANTE**: Los números representan el interés de búsqueda en relación con el valor máximo de la lista correspondiente a la región y el período especificados. El valor 100 indica la popularidad máxima del término, 50 implica la mitad de popularidad, y 0 significa que no hubo suficientes datos para este término


# Proceso de adquisición de datos

![adquisicion-datos](/diagramas-flujo/adquisicion_datos_trends_api.drawio.png)


# Convención de nombres de archivos

Como regla general, y con el único propósito de mantener ordenado el repositorio del proyecto, para el nombre de los archivos, se determina **NO UTILIZAR**:
-   Mayúsculas.
-   Acentos.
-   Espacios.
-   Cualquier tipo de caracter especial.

Adicionalmente, se debe respetar la siguiente convención:
-   Archivos: `<nombre_del_archivo_separado_por_guion_bajo>.<ext>`
-   Directiorios: `<nombre-del-directiorio-separado-por-guion-medio>`
-   Prototipos: Los prototipos no son considerados archivos productivos, por ende, su incorporación al repositorio está descartada por defecto. Para ello, se puede utilizar algún nombre bajo la convención:
    -   `prototipo.<ext>`
    -   `prototipado.<ext>`
    -   `proto.<ext>`