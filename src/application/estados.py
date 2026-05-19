from enum import Enum, auto


class EstadosTelaEntrada(Enum):
    OCIOSO = auto()
    VALIDANDO = auto()
    ENVIANDO = auto()
    SUCESSO = auto()
    ERRO = auto()


class EstadosTelaResultado(Enum):
    OCIOSO = auto()
    AUTENTICANDO = auto()
    AUTENTICADO = auto()
    CARREGANDO = auto()
    EXPORTANDO = auto()
    ERRO = auto()
