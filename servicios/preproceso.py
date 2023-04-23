import os
import csv
import yaml
import json
import logging

import pandas as pd

import modulos.utilidades as utils


# Paths absolutos
CURRENT = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(CURRENT)

# Archivo de configuración
with open(os.path.join(ROOT, 'config.yaml'), 'r') as f:
    config = yaml.safe_load(f)
f.close()

# Paths de script
RELACIONADOS = os.path.join(ROOT, config['datos']['relacionados'])
RELACIONADOS_PROCES = os.path.join(ROOT, config['etl']['relacionados'])
RELACIONADOS_EXPAND = os.path.join(ROOT, config['etl']['relacionados_expand'])

# Configuración de logs
logging.basicConfig(
    filename=config['logs']['etl'],
    level=logging.INFO,
    filemode='a',
    datefmt='%Y-%m-%d %H:%M:%S',
    format='%(levelname)s|%(asctime)s|%(name)s|\n%(message)s')


# ---- Temas relacionados ----
with open(RELACIONADOS, 'r') as f:
    contenido = json.load(f)
f.close()

# Formateo de datos
n_criterios = len(contenido)
filas_csv = [['criterio','inicio','fin','tipo','descripcion']]
for id_criterio in range(n_criterios):
    
    # Extraer lotes de consulta
    lotes = contenido[id_criterio]['contenidos']
    n_lotes = len(lotes)
    
    for id_lote in range(n_lotes):
        
        # Extraer el tipo de consulta del lote
        tipos = lotes[id_lote]['consulta']

        for tipo in tipos.keys():
            try:
                #Filtrar consulta
                consulta = pd.Series(
                    tipos[tipo]['descripcion']
                )

                for val_ in consulta:
                    # Almacenar dato en csv expandido
                    fila_ = [
                        contenido[id_criterio]['criterio']
                        ,lotes[id_lote]['fecha_inicio']
                        ,lotes[id_lote]['fecha_fin']
                        ,tipo
                        ,val_
                    ]
                    filas_csv.append(fila_)

                # Formatear consulta
                consulta = consulta.apply(utils.formatear_palabras)
                
                (# Asignar datos formateados a objeto original
                    contenido
                    [id_criterio]['contenidos']
                    [id_lote]['consulta']
                    [tipo]['descripcion']
                ) = consulta.to_dict()
                
                
            except TypeError:
                continue


# Almacenar resultados
with open(RELACIONADOS_PROCES, 'w') as json_file:
    json.dump(contenido, json_file)
json_file.close()

# Almacenar resultados expandidos
with open(RELACIONADOS_EXPAND, 'w') as csvfile: 
    # Crear objeto csv
    csvwriter = csv.writer(csvfile) 
        
    # Escribir filas de csv
    csvwriter.writerows(filas_csv)


if __name__ == '__main__':
    print('Trabajo terminado')