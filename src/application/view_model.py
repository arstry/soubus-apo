import csv
import json
import os
from abc import ABC, abstractmethod
from typing import List

from src.application.estados import EstadosTelaEntrada, EstadosTelaResultado
from src.application.processador_dados import ProcessadorDados
from src.data.gerenciador_autenticacao import GerenciadorAutenticacao
from src.data.gerenciador_json_dados import GerenciadorJsonDados
from src.util.excecoes import ExcecaoValidacaoSeguranca
from src.domain.ponto import Ponto
from src.domain.demanda import Demanda
from src.domain.linha_onibus import LinhaOnibus
from src.domain.parada import Parada


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

    def submeter_demanda(self, dados_brutos: dict) -> bool:
        """Processa e salva um novo registro de Demanda."""
        self.uiState = EstadosTelaEntrada.VALIDANDO
        try:
            demanda = self._processador.processar_demanda(dados_brutos)
            self.uiState = EstadosTelaEntrada.ENVIANDO
            self._repositorio.salvar_registro_demanda(demanda)
            self.uiState = EstadosTelaEntrada.SUCESSO
            return True
        except ExcecaoValidacaoSeguranca:
            self.uiState = EstadosTelaEntrada.ERRO
            raise
        except Exception:
            self.uiState = EstadosTelaEntrada.ERRO
            raise

    def submeter_parada(self, dados_brutos: dict) -> bool:
        """Processa e salva um novo registro de Parada de ônibus."""
        self.uiState = EstadosTelaEntrada.VALIDANDO
        try:
            parada = self._processador.processar_parada(dados_brutos)
            self.uiState = EstadosTelaEntrada.ENVIANDO
            self._repositorio.salvar_registro_parada(parada)
            self.uiState = EstadosTelaEntrada.SUCESSO
            return True
        except ExcecaoValidacaoSeguranca:
            self.uiState = EstadosTelaEntrada.ERRO
            raise
        except Exception:
            self.uiState = EstadosTelaEntrada.ERRO
            raise

    def submeter_linha_onibus(self, dados_brutos: dict) -> bool:
        """Processa e salva um novo registro de Linha de Ônibus."""
        self.uiState = EstadosTelaEntrada.VALIDANDO
        try:
            linha = self._processador.processar_linha_onibus(dados_brutos)
            self.uiState = EstadosTelaEntrada.ENVIANDO
            self._repositorio.salvar_registro_linha_onibus(linha)
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

    def obter_dados_tabela(self) -> List[Ponto]:
        """Retorna a lista polimórfica combinada de Demandas e Paradas para o mapa/tabela."""
        self.uiState = EstadosTelaResultado.CARREGANDO
        try:
            registros = self._repositorio.carregar_todos_os_pontos()
            self.uiState = EstadosTelaResultado.AUTENTICADO
            return registros
        except Exception:
            self.uiState = EstadosTelaResultado.ERRO
            raise
    
    def tratar_dados(self, dados_json: dict) -> dict:
        """
        Garante a integridade do dicionário de dados da malha logística.
        Normaliza campos nulos, tipos de dados e chaves obrigatórias.
        """
        if not dados_json:
            return {"demandas": [], "paradas": [], "linhas_onibus": []}

        dados_tratados = {
            # Garante que 'demandas' sempre será uma lista de dicionários válidos
            "demandas": [
                {
                    "latitude": float(d["latitude"]),
                    "longitude": float(d["longitude"]),
                    "demanda": int(d["demanda"]),
                    "nome": str(d.get("nome", "Demanda Sem Nome")).upper()
                }
                for d in dados_json.get("demandas", [])
                if "latitude" in d and "longitude" in d
            ],
            
            # Garante que 'paradas' mantém os IDs numéricos e o estado booleano correto
            "paradas": [
                {
                    "latitude": float(p["latitude"]),
                    "longitude": float(p["longitude"]),
                    "id": int(p["id"]),
                    "linhas_onibus": [str(l) for l in p.get("linhas_onibus", [])],
                    "estado": bool(p.get("estado", True))
                }
                for p in dados_json.get("paradas", [])
                if "latitude" in p and "longitude" in p and "id" in p
            ],
            
            # Mapeia as rotas para o NetworkX saber quais paradas conectar por linhas retas
            "linhas_onibus": [
                {
                    "nome": str(l["nome"]),
                    "capacidade": int(l.get("capacidade", 0)),
                    "paradas_ids": [int(pid) for pid in l.get("paradas_ids", [])]
                }
                for l in dados_json.get("linhas_onibus", [])
                if "nome" in l and "paradas_ids" in l
            ]
        }
        
        return dados_tratados
    def obter_linhas_onibus(self) -> List[LinhaOnibus]:
        """Retorna todas as linhas de ônibus cadastradas no sistema.
        
        Útil para preencher componentes visuais como Combobox, listas de filtros, etc.
        """
        self.uiState = EstadosTelaResultado.CARREGANDO
        try:
            linhas = self._repositorio.carregar_registros_linha_onibus()
            self.uiState = EstadosTelaResultado.AUTENTICADO
            return linhas
        except Exception:
            self.uiState = EstadosTelaResultado.ERRO
            raise

    def processar_exportacao(
        self, formato: str, filtros_linhas: List[str] | None = None
    ) -> str:
        self.uiState = EstadosTelaResultado.EXPORTANDO
        try:
            # Carrega a lista polimórfica contendo tanto Demandas quanto Paradas
            registros = self._repositorio.carregar_todos_os_pontos()

            # Aplica o filtro de linhas de ônibus apenas em objetos do tipo Parada
            if filtros_linhas:
                filtros_normalizados = [f.upper().strip() for f in filtros_linhas]
                registros_filtrados = []
                for r in registros:
                    if isinstance(r, Parada):
                        # Se for Parada, verifica se ela atende a alguma das linhas do filtro
                        linhas_da_parada = [l.upper().strip() for l in r.get_linhas_onibus()]
                        if any(f in linhas_da_parada for f in filtros_normalizados):
                            registros_filtrados.append(r)
                    elif isinstance(r, Demanda):
                        # Dependendo da regra de negócio: mantemos demandas no arquivo filtrado 
                        # ou ignoramos. Aqui vamos mantê-las para não sumirem do relatório geral.
                        registros_filtrados.append(r)
                registros = registros_filtrados

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

    def _exportar_csv(self, registros: List[Ponto]) -> str:
        caminho = "exportacao_pontos.csv"
        with open(caminho, "w", encoding="utf-8", newline="") as arquivo:
            escritor = csv.writer(arquivo)
            escritor.writerow(
                ["latitude", "longitude", "demanda", "linhas_onibus", "nome_demanda", "tipo_de_ponto"]
            )
            for ponto in registros:
                if isinstance(ponto, Demanda):
                    demanda_valor = ponto.get_demanda()
                    linhas_formatadas = ""
                    nome_demanda = ponto.get_nome()
                    tipo_texto = "DEMANDA"
                elif isinstance(ponto, Parada):
                    demanda_valor = 0
                    linhas_formatadas = ";".join(ponto.get_linhas_onibus())
                    nome_demanda = ""
                    tipo_texto = f"PARADA (ID: {ponto.get_id()})"
                else:
                    demanda_valor = 0
                    linhas_formatadas = ""
                    nome_demanda = ""
                    tipo_texto = "PONTO_GENERICO"

                escritor.writerow(
                    [
                        ponto.get_latitude(),
                        ponto.get_longitude(),
                        demanda_valor,
                        linhas_formatadas,
                        nome_demanda,
                        tipo_texto,
                    ]
                )
        return os.path.abspath(caminho)

    def _exportar_json(self, registros: List[Ponto]) -> str:
        caminho = "exportacao_pontos.json"
        with open(caminho, "w", encoding="utf-8") as arquivo:
            json.dump(
                [r.to_dict() for r in registros],
                arquivo,
                ensure_ascii=False,
                indent=2,
            )
        return os.path.abspath(caminho)
    