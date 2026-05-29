from typing import List


class Ponto:
    def __init__(
        self,
        latitude: float = 0.0,
        longitude: float = 0.0,
    ) -> None:
        self._latitude = latitude
        self._longitude = longitude

    def get_latitude(self) -> float:
        return self._latitude

    def set_latitude(self, valor: float) -> None:
        self._latitude = valor

    def get_longitude(self) -> float:
        return self._longitude

    def set_longitude(self, valor: float) -> None:
        self._longitude = valor

    
    def to_dict(self) -> dict:
        return {
            "latitude": self._latitude,
            "longitude": self._longitude,
        }

    @classmethod
    def from_dict(cls, dados: dict) -> "Ponto":
        return cls(
            latitude=float(dados.get("latitude", 0.0)),
            longitude=float(dados.get("longitude", 0.0)),
        )

    def __repr__(self) -> str:
        return (
            f"Ponto(lat={self._latitude}, lon={self._longitude}, "
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Ponto):
            return NotImplemented
        return (
            self._latitude == other._latitude
            and self._longitude == other._longitude
        )
