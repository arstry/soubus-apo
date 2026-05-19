import csv
import json
import os
from abc import ABC, abstractmethod
from typing import List

from src.application.estados import EstadosTelaEntrada, EstadosTelaResultado
from src.application.processador_dados import ProcessadorDados
from src.data.gerenciador_autenticacao import GerenciadorAutenticacao
from src.data.gerenciador_json_dados import GerenciadorJsonDados
from src.domain import Ponto, PontoTransporte
from src.util.excecoes import ExcecaoValidacaoSeguranca


class ViewModel(ABC):
    def __init__(self, repositorio: GerenciadorJsonDados) -> None:
        self._repositorio = repositorio


class InputViewModel(ViewModel):
    def __init__(
        self,
        repositorio: GerenciadorJsonDados,
        processador: ProcessadorDados,
    ) -> None:
        super().__init__(repositorio)
        self._processador = processador
        self.uiState = EstadosTelaEntrada.OCIOSO

    def submeter_dados(self, dados_brutos: dict) -> bool:
        self.uiState = EstadosTelaEntrada.VALIDANDO
        try:
            ponto = self._processador.processar(dados_brutos)
            self.uiState = EstadosTelaEntrada.ENVIANDO
            self._repositorio.salvar_registro(ponto)
            self.uiState = EstadosTelaEntrada.SUCESSO
            return True
        except ExcecaoValidacaoSeguranca:
            self.uiState = EstadosTelaEntrada.ERRO
            raise
        except Exception:
            self.uiState = EstadosTelaEntrada.ERRO
            raise


class ResultadoViewModel(ViewModel):
    def __init__(
        self,
        repositorio: GerenciadorJsonDados,
        autenticador: GerenciadorAutenticacao,
    ) -> None:
        super().__init__(repositorio)
        self._autenticador = autenticador
        self.uiState = EstadosTelaResultado.OCIOSO

    def realizar_login(self, usuario: str, senha_plana: str) -> bool:
        self.uiState = EstadosTelaResultado.AUTENTICANDO
        try:
            sucesso = self._autenticador.validar_credenciais(usuario, senha_plana)
            if sucesso:
                self.uiState = EstadosTelaResultado.AUTENTICADO
            else:
                self.uiState = EstadosTelaResultado.ERRO
            return sucesso
        except Exception:
            self.uiState = EstadosTelaResultado.ERRO
            raise

    def obter_dados_tabela(self) -> List[PontoTransporte]:
        self.uiState = EstadosTelaResultado.CARREGANDO
        try:
            registros = self._repositorio.carregar_registros()
            self.uiState = EstadosTelaResultado.AUTENTICADO
            return registros
        except Exception:
            self.uiState = EstadosTelaResultado.ERRO
            raise

    def processar_exportacao(
        self, formato: str, filtros_linhas: List[str] | None = None
    ) -> str:
        self.uiState = EstadosTelaResultado.EXPORTANDO
        try:
            registros = self._repositorio.carregar_registros()

            if filtros_linhas:
                filtros_normalizados = [f.upper().strip() for f in filtros_linhas]
                registros = [
                    r
                    for r in registros
                    if any(
                        filtro in " ".join(r.get_linhas_onibus()).upper()
                        for filtro in filtros_normalizados
                    )
                ]

            formato = formato.lower().strip()
            if formato == "csv":
                caminho = self._exportar_csv(registros)
            elif formato == "json":
                caminho = self._exportar_json(registros)
            else:
                raise ValueError(f"Formato de exportação não suportado: {formato}")

            self.uiState = EstadosTelaResultado.AUTENTICADO
            return caminho
        except Exception:
            self.uiState = EstadosTelaResultado.ERRO
            raise

    def _exportar_csv(self, registros: List[PontoTransporte]) -> str:
        caminho = "exportacao_pontos.csv"
        with open(caminho, "w", encoding="utf-8", newline="") as arquivo:
            escritor = csv.writer(arquivo)
            escritor.writerow(
                ["latitude", "longitude", "demanda", "linhas_onibus", "tipo_de_ponto"]
            )
            for ponto in registros:
                escritor.writerow(
                    [
                        ponto.get_latitude(),
                        ponto.get_longitude(),
                        ponto.get_demanda(),
                        ";".join(ponto.get_linhas_onibus()),
                        ponto.get_tipo_de_ponto(),
                    ]
                )
        return os.path.abspath(caminho)

    def _exportar_json(self, registros: List[PontoTransporte]) -> str:
        caminho = "exportacao_pontos.json"
        with open(caminho, "w", encoding="utf-8") as arquivo:
            json.dump(
                [r.to_dict() for r in registros],
                arquivo,
                ensure_ascii=False,
                indent=2,
            )
        return os.path.abspath(caminho)
