from app.models.gerente import Gerente

def resumen_general():
    return Gerente.resumen()

def productos_mas_vendidos():
    return Gerente.mas_vendidos()

def clientes_top():
    return Gerente.clientes_con_mas_puntos()