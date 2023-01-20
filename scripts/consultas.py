import json
import datetime as dt

from dateutil.relativedelta import relativedelta
from pytrends.request import TrendReq

class Consultar:
    
    def __init__(self, criterio, inicio, fin):
        self.criterio = criterio
        self.consulta = TrendReq(hl='es-MX', tz=300, geo='MX')
        self.inicio = inicio
        self.fin = fin


    def interes_tiempo(self, periodo=2):
        fecha_fin = dt.date.today()
        fecha_inicio = fecha_fin - relativedelta(years=periodo)
        periodo = f"{fecha_inicio.strftime('%Y-%m-%d')} {fecha_fin.strftime('%Y-%m-%d')}"

        self.consulta.build_payload(kw_list=[self.criterio], cat=0, timeframe=periodo, geo='MX')
        
        salida = self.consulta.interest_over_time().reset_index()
        salida['date'] = salida['date'].astype(str)
        salida.columns = ["fecha","valor","parcial"]
        salida = salida.to_dict()

        return salida

    def temas_relacionado(self):
        periodo = f"{self.inicio} {self.fin}"

        self.consulta.build_payload(kw_list=[self.criterio], cat=0, timeframe=periodo, geo='MX')

        


