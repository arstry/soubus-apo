from typing import List


class Ponto:
    def __init__(
        self,
        latitude: float = 0.0,
        longitude: float = 0.0,
        demanda: int = 0,
        linhas_onibus: List[str] | None = None,
        tipo_de_ponto: str = "",
    ) -> None:
        self._latitude = latitude
        self._longitude = longitude
        self._demanda = demanda
        self._linhas_onibus = linhas_onibus if linhas_onibus is not None else []
        self._tipo_de_ponto = tipo_de_ponto

    def get_latitude(self) -> float:
        return self._latitude

    def set_latitude(self, valor: float) -> None:
        self._latitude = valor

    def get_longitude(self) -> float:
        return self._longitude

    def set_longitude(self, valor: float) -> None:
        self._longitude = valor

    def get_demanda(self) -> int:
        return self._demanda

    def set_demanda(self, valor: int) -> None:
        self._demanda = valor

    def get_linhas_onibus(self) -> List[str]:
        return self._linhas_onibus

    def set_linhas_onibus(self, valor: List[str]) -> None:
        self._linhas_onibus = valor

    def get_tipo_de_ponto(self) -> str:
        return self._tipo_de_ponto

    def set_tipo_de_ponto(self, valor: str) -> None:
        self._tipo_de_ponto = valor

    def to_dict(self) -> dict:
        return {
            "latitude": self._latitude,
            "longitude": self._longitude,
            "demanda": self._demanda,
            "linhas_onibus": self._linhas_onibus,
            "tipo_de_ponto": self._tipo_de_ponto,
        }

    @classmethod
    def from_dict(cls, dados: dict) -> "Ponto":
        return cls(
            latitude=float(dados.get("latitude", 0.0)),
            longitude=float(dados.get("longitude", 0.0)),
            demanda=int(dados.get("demanda", 0)),
            linhas_onibus=list(dados.get("linhas_onibus", [])),
            tipo_de_ponto=str(dados.get("tipo_de_ponto", "")),
        )

    def __repr__(self) -> str:
        return (
            f"Ponto(lat={self._latitude}, lon={self._longitude}, "
            f"demanda={self._demanda}, linhas={self._linhas_onibus}, "
            f"tipo={self._tipo_de_ponto!r})"
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Ponto):
            return NotImplemented
        return (
            self._latitude == other._latitude
            and self._longitude == other._longitude
            and self._demanda == other._demanda
            and self._linhas_onibus == other._linhas_onibus
            and self._tipo_de_ponto == other._tipo_de_ponto
        )
