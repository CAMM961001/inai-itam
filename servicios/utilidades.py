import datetime as dt

from dateutil.relativedelta import relativedelta

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