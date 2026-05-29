from .ponto import Ponto
from .demanda import Demanda
from .parada import Parada
from .linha_onibus import LinhaOnibus

PontoTransporte = Ponto

__all__ = [
    "Ponto", 
    "PontoTransporte", 
    "Demanda", 
    "Parada", 
    "LinhaOnibus"
]
