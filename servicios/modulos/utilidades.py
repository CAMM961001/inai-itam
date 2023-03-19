import re
import datetime as dt
import pandas as pd

from itertools import product
from unidecode import unidecode
from dateutil.relativedelta import relativedelta

from nltk.corpus import stopwords

# Descargar base de stopwords de NLTK
#from nltk import download
#download('stopwords')

def generar_periodos(anios=2, meses=3):
    """
    Generar lotes de tiempo para un periodo dado

    Params:
        anios (int): Años comprendidos en el periodo de tiempo.
        meses (int): Duración en meses que tendrá cada lote.

    Salidas:
        periodos (list): Lista de tuplas con la fecha de inicio
        y la fecha de fin de cada lote.
    """
    #Definir número de lotes del periodo
    NUM_LOTES = [meses] * int(anios * 12/meses)
    
    #Obtener periodos de cada lote
    periodos = list()
    inicial = dt.date.today()
    for i in NUM_LOTES:
        #Obtener fecha final de lote
        final = inicial - relativedelta(months=i)

        #Construir tupla de lote
        periodos.append((final.strftime("%Y-%m-%d"), inicial.strftime("%Y-%m-%d")))

        #Acutalizar fecha inicial de nuevo lote
        inicial = final

    return periodos


def formatear_palabras(doc_, idioma='spanish'):
    stop_words = set(stopwords.words(idioma))

    # Quitar mayúsculas
    doc_ = doc_.lower()

    # Quitar stopwords
    ref = doc_.split()
    filtro = [val for val in ref if val not in stop_words]
    doc_ = ' '.join(filtro)

    # Quitar acentos
    doc_ = unidecode(doc_)

    # Quitar caracteres especiales
    doc_ = re.sub('[,"|@$#]', '', doc_)

    # Cambiar de str a lista
    doc_ = doc_.split(sep=' ')
    
    return doc_


def tabla_temas_relacionados(obj_json, id_lote):
    
    # Dataframe de resultados
    criterios_lote = pd.DataFrame(columns=['descripcion','tipo','inicio','fin','lote','criterio','id_criterio'])

    # Iteradores
    criterios = range(len(obj_json))
    tipos = range(len(obj_json[0]['contenidos'][id_lote]['consulta']))

    for id_criterio, id_tipo in product(criterios, tipos):
        # Parámetros de consulta en JSON
        CRITERIO = obj_json[id_criterio]['criterio']
        LOTE = obj_json[id_criterio]['contenidos'][id_lote]
        INICIO = LOTE['fecha_inicio']
        FIN = LOTE['fecha_fin']
        TIPO = list( LOTE['consulta'].keys() )[id_tipo]

        # Transformación de datos
        df_ = (
            pd.DataFrame(LOTE['consulta'][TIPO])
            .filter(items=['descripcion'])
            .assign(
                tipo = TIPO
                ,inicio = INICIO
                ,fin = FIN
                ,lote = id_lote
                ,criterio = CRITERIO
                ,id_criterio = id_criterio
            )
        )

        # Agregar resultados a conjunto de análisis
        criterios_lote = pd.concat([criterios_lote, df_], axis=0, ignore_index=True)

    return criterios_lote
