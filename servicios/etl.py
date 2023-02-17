import os, json, yaml, sys

CURRENT = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(CURRENT)

import modulos.consultas as consultas

# Archivo de configuración
with open(os.path.join(ROOT, 'config.yaml'), 'r') as f:
    config = yaml.safe_load(f)
f.close()

# Archivo de criterios de búsqueda
with open(file=os.path.join(ROOT, config['etl']['criterios']), mode='r') as f:
    criterios_busqueda = [row.strip() for row in f]        
f.close()

# Archivo de corpus de consulta
CORPUS_PATH = os.path.join(ROOT, config['etl']['corpus'])
with open(file=CORPUS_PATH, mode='r') as f:
    corpus = json.load(f)
f.close()

# Criterios existentes en corpus
existencias = [corpus[idx]['criterio'] for idx in range(len(corpus))]


def etl():
    """
    
    """
    for criterio in criterios_busqueda:
        
        # ---- Criterio de búsqueda nuevo ----
        if criterio not in existencias:

            # Leer archivo JSON
            listObj = list()
            with open(CORPUS_PATH) as f:
                listObj = json.load(f)
                consulta = consultas.consulta_completa(criterio=criterio, anio=2, meses=3)
                listObj.append(consulta)
            f.close()
            
            # Escribir resultados de consulta en corpus
            with open(CORPUS_PATH, 'w') as json_file:
                json.dump(listObj, json_file, separators=(',',': '))
            json_file.close()
            
            # Registrar estado de consulta en log
            print(f"Se agregó existosamente criterio: {criterio}")
        
        # ---- Criterio de búsqueda existente ----
        else:
            print(criterio, '\texistente')



if __name__ == '__main__':
    etl()