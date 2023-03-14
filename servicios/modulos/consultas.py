import os, json
import datetime as dt

from dateutil.relativedelta import relativedelta
from pytrends.request import TrendReq

CURRENT = os.path.dirname(os.path.abspath(__file__))
PARENT = os.path.dirname(CURRENT)
ROOT = os.path.dirname(PARENT)
#sys.path.append(PARENT)

class Consultar:
    """
    Clase para realizar consultas a GoogleTrends optimizada para criterios
    de búsqueda de México.

    Parámetros:
    -   criterio: <str>, palabra clave que se desea consultar
    -   inicio: <str>, fecha de inicio del periodo de interés 'yyyy-mm-dd'
    -   fin: <str>, fecha de fin del periodo de interés 'yyyy-mm-dd'
    -   ventana: <int>, ventana de consulta anual. Aplica para los métodos:
        -   interes_tiempo()
    """
    def __init__(self, criterio, inicio, fin, ventana=2):
        self.criterio = criterio
        self.consulta = TrendReq(hl='es-MX', tz=360, geo='MX')
        self.inicio = inicio
        self.fin = fin
        self.ventana = ventana


    def interes_tiempo(self):
        """
        Método de clase.
        
        Interés a lo largo del tiempo para un criterio de búsqueda dado.
        """
        fecha_fin = dt.date.today()
        fecha_inicio = fecha_fin - relativedelta(years=self.ventana)
        periodo = f"{fecha_inicio.strftime('%Y-%m-%d')} {fecha_fin.strftime('%Y-%m-%d')}"

        self.consulta.build_payload(kw_list=[self.criterio], cat=0, timeframe=periodo, geo='MX')
        
        salida = self.consulta.interest_over_time().reset_index()
        salida['date'] = salida['date'].astype(str)
        salida.columns = ["fecha","valor","parcial"]
        salida = salida.to_dict()

        return salida

    def temas_relacionados(self):
        """
        Método de clase.
        
        Temas relacionados con el criterio de búsqueda dado.
        Regresa dos conjuntos:
        -   Temas en aumento
        -   Temas top
        """
        periodo = f"{self.inicio} {self.fin}"

        self.consulta.build_payload(kw_list=[self.criterio], cat=0, timeframe=periodo, geo='MX')

        salida = self.consulta.related_topics()

        try:
            if salida[self.criterio]['rising'].empty: aumento = None
            else:
                aumento = salida[self.criterio]['rising'][['value','formattedValue','topic_title','topic_type']]
                aumento.columns = ["valor","pct_valor","descripcion","tipo"]
                aumento = aumento.to_dict()
            
            if salida[self.criterio]['top'].empty: top = None
            else:
                top = salida[self.criterio]['top'][['value','formattedValue','topic_title','topic_type']]
                top.columns = ["valor","pct_valor","descripcion","tipo"]
                top = top.to_dict()
            
            salida = {"aumento":aumento, "top":top}

        except KeyError:
            pass      

        return salida

    def interes_region(self):
        """
        Método de clase.
        
        Interés por estado de la república para un criterio dado.
        """
        periodo = f"{self.inicio} {self.fin}"

        self.consulta.build_payload(kw_list=[self.criterio], cat=0, timeframe=periodo, geo='MX')

        salida = self.consulta.interest_by_region().reset_index()
        salida.columns = ["estado","valor"]
        salida = salida.to_dict()

        return salida


def criterios_existentes(file):
    
    # Se abre el archivo json
    with open(file=file, mode='r') as f:
        corpus = json.load(f)
    f.close()

    existencias = [corpus[idx]['criterio'] for idx in range(len(corpus))]
    
    return existencias

