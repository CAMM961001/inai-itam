import json
import datetime as dt

from dateutil.relativedelta import relativedelta
from pytrends.request import TrendReq

class Consultar:
    
    def __init__(self, criterio, inicio, fin, ventana=2):
        self.criterio = criterio
        self.consulta = TrendReq(hl='es-MX', tz=300, geo='MX')
        self.inicio = inicio
        self.fin = fin
        self.ventana = ventana


    def interes_tiempo(self):
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
        periodo = f"{self.inicio} {self.fin}"

        self.consulta.build_payload(kw_list=[self.criterio], cat=0, timeframe=periodo, geo='MX')

        salida = self.consulta.related_topics()
        aumento = salida[self.criterio]['rising'][['value','formattedValue','topic_title','topic_type']]
        aumento.columns = ["valor","pct_valor","descripcion","tipo"]
        top = salida[self.criterio]['top'][['value','formattedValue','topic_title','topic_type']]
        top.columns = ["valor","pct_valor","descripcion","tipo"]
        salida = {"aumento":aumento.to_dict(), "top":top.to_dict()}

        return salida

    def interes_region(self):
        periodo = f"{self.inicio} {self.fin}"

        self.consulta.build_payload(kw_list=[self.criterio], cat=0, timeframe=periodo, geo='MX')

        salida = self.consulta.interest_by_region().reset_index()
        salida.columns = ["estado","valor"]
        salida = salida.to_dict()

        return salida




