import os, sys

CURRENT = os.path.dirname(os.path.abspath(__file__))
PARENT = os.path.dirname(CURRENT)
ROOT = os.path.dirname(PARENT)
sys.path.append(PARENT)

import json
import yaml
import utilidades as utils

#Archivo de configuracion
with open(os.path.join(ROOT, "config.yaml"), "r") as file:
    config = yaml.safe_load(file)


if __name__ == "__main__":
    
    print(CURRENT, PARENT, ROOT)