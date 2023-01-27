import os, sys, json, yaml

CURRENT = os.path.dirname(os.path.abspath(__file__))
PARENT = os.path.dirname(CURRENT)
ROOT = os.path.dirname(PARENT)
sys.path.append(PARENT)

import consultas
import utilidades as utils

#Archivo de configuración
with open(os.path.join(ROOT, 'config.yaml'), 'r') as f:
    config = yaml.safe_load(f)
f.close()

#Archivo de criterios de búsqueda
with open(file=os.path.join(ROOT, config['etl']['criterios']), mode='r') as f:
    criterios_busqueda = [row.strip() for row in f]        
f.close()

#Archivo de corpus de consulta
with open(file=os.path.join(ROOT, config['etl']['corpus']), mode='r') as f:
    corpus = json.load(f)
f.close()

#Criterios existentes en corpus
existencias = [corpus[idx]['criterio'] for idx in range(len(corpus))]

if __name__ == '__main__':
    print(existencias)