from typing import List
from .ponto import Ponto

class Demanda(Ponto):
    def __init__(
        self,
        latitude: float = 0.0,
        longitude: float = 0.0,
        demanda: int = 0,
        nome: str = "",
    ) -> None:
        super().__init__(latitude, longitude)

        self._demanda = demanda
        self._nome = nome

    def get_demanda(self) -> int:
        return self._demanda

    def set_demanda(self, valor: int) -> None:
        self._demanda = valor

    def get_nome(self) -> str:
        return self._nome

    def set_nome(self, valor: str) -> None:
        self._nome = valor

    def to_dict(self) -> dict:
        return {
            **super().to_dict(),
            "demanda": self._demanda,
            "nome": self._nome,
        }

    @classmethod
    def from_dict(cls, dados: dict) -> "Demanda":
        return cls(
            nome=str(dados.get("nome", "")),
            latitude=dados.get("latitude", 0.0),
            longitude=dados.get("longitude", 0.0),
            demanda=dados.get("demanda", 0),
        )