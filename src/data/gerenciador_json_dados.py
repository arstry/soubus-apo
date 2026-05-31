import json
import os
from typing import List

from src.domain.ponto import Ponto
from src.domain.demanda import Demanda
from src.domain.linha_onibus import LinhaOnibus
from src.domain.parada import Parada


class GerenciadorJsonDados:
    # Mudamos o esquema padrão para separar as caixas
    ESQUEMA_PADRAO: dict = {
        "demandas": [],
        "paradas": [],
        "linhas_onibus": []
    }

    def __init__(self, caminho_arquivo: str | None = None) -> None:
        if caminho_arquivo is None:
            static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
            caminho_arquivo = os.path.join(static_dir, "dados_sistema.json")
        self._caminho_arquivo = caminho_arquivo
        self._garantir_integridade_esquema()


    def salvar_registro_demanda(self, demanda: Demanda) -> None:
        dados = self._carregar_arquivo()
        dados["demandas"].append(demanda.to_dict())
        self._salvar_arquivo(dados)
    
    def salvar_registro_parada(self, parada: Parada) -> None:
        dados = self._carregar_arquivo()
        dados["paradas"].append(parada.to_dict())
        self._salvar_arquivo(dados)

    def salvar_registro_linha_onibus(self, linha: LinhaOnibus) -> None:
        dados = self._carregar_arquivo()
        dados["linhas_onibus"].append(linha.to_dict())
        self._salvar_arquivo(dados)

    def carregar_todos_os_pontos(self) -> List[Ponto]:
        """
        Lê as chaves separadas do JSON e reconstrói as respectivas instâncias,
        retornando uma lista única com todas as Demandas e Paradas juntas.
        """
        dados = self._carregar_arquivo()
        pontos: List[Ponto] = []
        
        # Reconstrói as demandas
        for reg in dados.get("demandas", []):
            pontos.append(Demanda.from_dict(reg))
            
        # Reconstrói as paradas
        for reg in dados.get("paradas", []):
            pontos.append(Parada.from_dict(reg))
            
        return pontos

    def carregar_registros_linha_onibus(self) -> List[LinhaOnibus]:
        """Como linhas de ônibus não são pontos, elas continuam isoladas aqui."""
        dados = self._carregar_arquivo()
        return [LinhaOnibus.from_dict(reg) for reg in dados.get("linhas_onibus", [])]


    def _garantir_integridade_esquema(self) -> None:
        if not os.path.exists(self._caminho_arquivo):
            self._salvar_arquivo(self.ESQUEMA_PADRAO)
            return

        try:
            dados = self._carregar_arquivo()
            if not isinstance(dados, dict):
                self._salvar_arquivo(self.ESQUEMA_PADRAO)
                return
            
            # Valida se todas as chaves obrigatórias do novo esquema existem e são listas
            chaves_obrigatorias = ["demandas", "paradas", "linhas_onibus"]
            for chave in chaves_obrigatorias:
                if chave not in dados or not isinstance(dados[chave], list):
                    self._salvar_arquivo(self.ESQUEMA_PADRAO)
                    return
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
