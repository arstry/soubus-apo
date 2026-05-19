import json
import os
from typing import List

from src.domain.ponto import Ponto


class GerenciadorJsonDados:
    ESQUEMA_PADRAO: dict = {"registros": []}

    def __init__(self, caminho_arquivo: str | None = None) -> None:
        if caminho_arquivo is None:
            static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
            caminho_arquivo = os.path.join(static_dir, "dados_pontos.json")
        self._caminho_arquivo = caminho_arquivo
        self._garantir_integridade_esquema()

    def salvar_registro(self, ponto: Ponto) -> None:
        dados = self._carregar_arquivo()
        dados["registros"].append(ponto.to_dict())
        self._salvar_arquivo(dados)

    def carregar_registros(self) -> List[Ponto]:
        dados = self._carregar_arquivo()
        return [Ponto.from_dict(registro) for registro in dados["registros"]]

    def _garantir_integridade_esquema(self) -> None:
        if not os.path.exists(self._caminho_arquivo):
            self._salvar_arquivo(self.ESQUEMA_PADRAO)
            return

        try:
            dados = self._carregar_arquivo()
            if not isinstance(dados, dict) or "registros" not in dados:
                self._salvar_arquivo(self.ESQUEMA_PADRAO)
                return
            if not isinstance(dados["registros"], list):
                self._salvar_arquivo(self.ESQUEMA_PADRAO)
        except (json.JSONDecodeError, OSError):
            self._salvar_arquivo(self.ESQUEMA_PADRAO)

    def _carregar_arquivo(self) -> dict:
        with open(self._caminho_arquivo, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)

    def _salvar_arquivo(self, dados: dict) -> None:
        diretorio = os.path.dirname(self._caminho_arquivo)
        if diretorio:
            os.makedirs(diretorio, exist_ok=True)
        with open(self._caminho_arquivo, "w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, ensure_ascii=False, indent=2)
