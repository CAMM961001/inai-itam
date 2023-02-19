import os
import json
import yaml
import logging

import modulos.consultas as consultas
import utilidades as utils


# Paths absolutos
CURRENT = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(CURRENT)

# Archivo de configuración
with open(os.path.join(ROOT, 'config.yaml'), 'r') as f:
    config = yaml.safe_load(f)
f.close()

# PAths de script
TIEMPO_PATH = os.path.join(ROOT, config['datos']['tiempo'])
REGION_PATH = os.path.join(ROOT, config['datos']['region'])
RELACION_PATH = os.path.join(ROOT, config['datos']['relacionados'])

# Configuración de logs
logging.basicConfig(
    filename=config['logs']['etl'],
    level=logging.INFO,
    filemode='a',
    datefmt='%Y-%m-%d %H:%M:%S',
    format='%(levelname)s|%(asctime)s|%(name)s|\n%(message)s')

# Cargar criterios de búsqueda en memoria
with open(file=os.path.join(ROOT, config['datos']['criterios']), mode='r') as f:
    criterios_busqueda = [row.strip() for row in f]        
f.close()

# Periodos de consulta
periodos = utils.generar_periodos(
    anios=config['etl']['anios'],
    meses=config['etl']['meses'])

# Enlistar criterios existentes
with open(file=TIEMPO_PATH, mode='r') as f:
    corpus = json.load(f)
f.close()
existencias = [corpus[idx]['criterio'] for idx in range(len(corpus))]


# Extracción de información y almacenamiento
for criterio in criterios_busqueda:

    # ---- Interés en el tiempo ----
    estructura = {
        "criterio":criterio,
        "contenidos":[]
        }
    
    consulta = consultas.Consultar(
        criterio=criterio,
        inicio=periodos[0][0],
        fin=periodos[0][1],
        ventana=config['etl']['anios'])

    # Criterios nuevos en corpus
    if criterio not in existencias:
        print(criterio)

        # Leer archivo JSON
        listObj = list()
        with open(TIEMPO_PATH, 'r') as f:
            listObj = json.load(f)
            estructura['contenidos'] = consulta.interes_tiempo()
            listObj.append(estructura)
        f.close()
        
        # Escribir resultados de consulta en corpus
        with open(TIEMPO_PATH, 'w') as json_file:
            json.dump(listObj, json_file, separators=(',',': '))
        json_file.close()



# # Criterios existentes en corpus


# def etl():
#     """
    
#     """
#     prompt = f"Trabajo: {__file__}\n"
#     for criterio in criterios_busqueda:
        
#         # ---- Criterio de búsqueda nuevo ----
#         if criterio not in existencias:        
#             try:
#                 consulta = consultas.consulta_completa(criterio=criterio, anio=2, meses=3)
#                 prompt += f'\t- "{criterio}" agregado\n'
            
#             except Exception:
#                 consulta = None
#                 prompt += f'\t- "{criterio}" error\n'
#                 break

#             if consulta != None:
                # # Leer archivo JSON
                # listObj = list()
                # with open(CORPUS_PATH, 'r') as f:
                #     listObj = json.load(f)
                #     listObj.append(consulta)
                # f.close()
                
                # # Escribir resultados de consulta en corpus
                # with open(CORPUS_PATH, 'w') as json_file:
                #     json.dump(listObj, json_file, separators=(',',': '))
                # json_file.close()

#         # ---- Criterio de búsqueda existente ----
#         else:
#             prompt += f'\t- "{criterio}" existente\n'

#     logging.info(prompt)


if __name__ == '__main__':
    print('Done')