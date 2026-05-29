from typing import List
from .linha_onibus import LinhaOnibus
from .ponto import Ponto

class Parada(Ponto):
    def __init__(
        self,
        id: int = 0,
        latitude: float = 0.0,
        longitude: float = 0.0,
        linhas_onibus: List[str] | None = None,
        estado: bool = False,
    ) -> None:
        super().__init__(latitude, longitude)

        self._id = id
        self._linhas_onibus = linhas_onibus if linhas_onibus is not None else []
        self._estado = estado

    def get_id(self) -> int:
        return self._id

    def get_linhas_onibus(self) -> List[str]:
        return self._linhas_onibus

    def set_linhas_onibus(self, valor: List[str]) -> None:
        self._linhas_onibus = valor

    def get_estado(self) -> bool:
        return self._estado

    def set_estado(self, valor: bool) -> None:
        self._estado = valor

    def to_dict(self) -> dict:
        return {
            **super().to_dict(),
            "id": self._id,
            "linhas_onibus": self._linhas_onibus,
            "estado": self._estado,
        }

    @classmethod
    def from_dict(cls, dados: dict) -> "Parada":
        return cls(
            id=dados.get("id", 0),
            latitude=dados.get("latitude", 0.0),
            longitude=dados.get("longitude", 0.0),
            linhas_onibus=dados.get("linhas_onibus", []),
            estado=dados.get("estado", False),
        )
    