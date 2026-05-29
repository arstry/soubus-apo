from typing import List

class LinhaOnibus:
    def __init__(
        self,
        nome: str = "",
        capacidade: int = 0,
        paradas_ids: List[int] | None = None,
    ) -> None:
        self._nome = nome
        self._capacidade = capacidade
        self._paradas_ids = paradas_ids if paradas_ids is not None else []

    def get_nome(self) -> str:
        return self._nome

    def get_capacidade(self) -> int:
        return self._capacidade

    def set_capacidade(self, valor: int) -> None:
        self._capacidade = valor

    def set_nome(self, valor: str) -> None:
        self._nome = valor

    def get_paradas_ids(self) -> List[int]:
        return self._paradas_ids

    def set_paradas_ids(self, valor: List[int]) -> None:
        self._paradas_ids = valor

    def to_dict(self) -> dict:
        return {
            "nome": self._nome,
            "capacidade": self._capacidade,
            "paradas_ids": self._paradas_ids,
        }

    @classmethod
    def from_dict(cls, dados: dict) -> "LinhaOnibus":
        return cls(
            capacidade=int(dados.get("capacidade", 0)),
            nome=str(dados.get("nome", "")),
            paradas_ids=list(dados.get("paradas_ids", [])),
        )