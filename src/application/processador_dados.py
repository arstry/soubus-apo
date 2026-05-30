import re
import unicodedata
from typing import List

from src.domain.ponto import Ponto
from src.domain.demanda import Demanda
from src.domain.linha_onibus import LinhaOnibus
from src.domain.parada import Parada
from src.util.excecoes import ExcecaoValidacaoSeguranca


class ProcessadorDados:
    PRECISAO_COORDENADAS: int = 6
    TAMANHO_MAXIMO_TEXTO: int = 200
    PADRAO_INJECAO: re.Pattern = re.compile(r"[;&|`$(){}\[\]<>!\\'\"]")

    def processar_demanda(self, dados_brutos: dict) -> Demanda:
        if not isinstance(dados_brutos, dict):
            raise ExcecaoValidacaoSeguranca("Dados brutos devem ser um dicionário.")

        # 1. Extração e validação de Coordenadas comuns
        lat, lon = self._processar_coordenadas_comuns(dados_brutos)

        # 2. Processamento específico de Demanda
        demanda = int(dados_brutos.get("demanda", 0))
        if demanda < 0:
            raise ExcecaoValidacaoSeguranca("Demanda não pode ser negativa.", "demanda")

        nome_raw = str(dados_brutos.get("nome", ""))
        nome = self._limpar_e_validar_texto(nome_raw, "nome")

        return Demanda(latitude=lat, longitude=lon, demanda=demanda, nome=nome)

    def processar_parada(self, dados_brutos: dict) -> Parada:
        if not isinstance(dados_brutos, dict):
            raise ExcecaoValidacaoSeguranca("Dados brutos devem ser um dicionário.")

        # 1. Extração e validação de Coordenadas comuns
        lat, lon = self._processar_coordenadas_comuns(dados_brutos)

        # 2. Processamento específico de Parada
        id_parada = int(dados_brutos.get("id", 0))
        estado = bool(dados_brutos.get("estado", False))
        
        linhas_raw = dados_brutos.get("linhas_onibus", "")
        linhas_filtradas = self._processar_lista_linhas_onibus(linhas_raw)

        return Parada(
            id=id_parada,
            latitude=lat,
            longitude=lon,
            linhas_onibus=linhas_filtradas,
            estado=estado
        )

    def processar_linha_onibus(self, dados_brutos: dict) -> LinhaOnibus:
        if not isinstance(dados_brutos, dict):
            raise ExcecaoValidacaoSeguranca("Dados brutos devem ser um dicionário.")

        # Linha de ônibus NÃO usa coordenadas, processa apenas dados textuais/numéricos
        nome_raw = str(dados_brutos.get("nome", ""))
        nome = self._limpar_e_validar_texto(nome_raw, "nome")

        capacidade = int(dados_brutos.get("capacidade", 0))
        if capacidade < 0:
            raise ExcecaoValidacaoSeguranca("Capacidade não pode ser negativa.", "capacidade")

        paradas_ids = dados_brutos.get("paradas_ids", [])
        if not isinstance(paradas_ids, list):
            paradas_ids = [int(paradas_ids)] if paradas_ids else []
        else:
            paradas_ids = [int(i) for i in paradas_ids]

        return LinhaOnibus(nome=nome, capacidade=capacidade, paradas_ids=paradas_ids)

    def _processar_coordenadas_comuns(self, dados: dict) -> tuple[float, float]:
        """Extrai, trunca e valida os limites geográficos padrão de qualquer ponto."""
        latitude = float(dados.get("latitude", 0.0))
        longitude = float(dados.get("longitude", 0.0))

        latitude = self.truncar_coordenadas(latitude)
        longitude = self.truncar_coordenadas(longitude)

        if not (-90.0 <= latitude <= 90.0):
            raise ExcecaoValidacaoSeguranca("Latitude fora do intervalo válido [-90, 90].", "latitude")
        if not (-180.0 <= longitude <= 180.0):
            raise ExcecaoValidacaoSeguranca("Longitude fora do intervalo válido [-180, 180].", "longitude")

        return latitude, longitude

    def _limpar_e_validar_texto(self, texto: str, nome_campo: str) -> str:
        """Centraliza a higienização de strings contra ataques e flood."""
        if self.detectar_flood_nonsense(texto):
            raise ExcecaoValidacaoSeguranca(f"Texto do campo '{nome_campo}' contém suspeita de flood.", nome_campo)
        
        texto_limpo = self.remover_acentos_e_maiusculo(texto)
        return self.neutralizar_injecao_comandos(texto_limpo)

    def _processar_lista_linhas_onibus(self, linhas_raw: str | list) -> List[str]:
        """Processa a string ou lista bruta de linhas associadas a uma parada."""
        linhas_extraidas = []
        if isinstance(linhas_raw, list):
            linhas_extraidas = [str(item).strip() for item in linhas_raw if str(item).strip()]
        elif isinstance(linhas_raw, str):
            partes = re.split(r"[,;\n]+", linhas_raw)
            linhas_extraidas = [p.strip() for p in partes if p.strip()]

        # Limpa e sanitiza cada linha extraída
        linhas_limpas = []
        for linha in linhas_extraidas:
            if not self.detectar_flood_nonsense(linha):
                linha_sanitizada = self.neutralizar_injecao_comandos(self.remover_acentos_e_maiusculo(linha))
                if linha_sanitizada:
                    linhas_limpas.append(linha_sanitizada)

        return linhas_limpas


    def remover_acentos_e_maiusculo(self, texto: str) -> str:
        texto_normalizado = unicodedata.normalize("NFKD", texto)
        texto_sem_acentos = "".join(
            c for c in texto_normalizado if not unicodedata.combining(c)
        )
        return texto_sem_acentos.upper().strip()

    def truncar_coordenadas(self, coord: float) -> float:
        fator = 10**self.PRECISAO_COORDENADAS
        return float(int(coord * fator)) / fator

    def neutralizar_injecao_comandos(self, texto: str) -> str:
        if len(texto) > self.TAMANHO_MAXIMO_TEXTO:
            texto = texto[: self.TAMANHO_MAXIMO_TEXTO]
        return self.PADRAO_INJECAO.sub("", texto)

    def detectar_flood_nonsense(self, texto: str) -> bool:
        if len(texto) > self.TAMANHO_MAXIMO_TEXTO:
            return True

        if len(texto) >= 10:
            char_unico = set(texto)
            if len(char_unico) <= 2:
                return True

            repeticoes = 1
            max_repeticoes = 1
            for i in range(1, len(texto)):
                if texto[i] == texto[i - 1]:
                    repeticoes += 1
                    max_repeticoes = max(max_repeticoes, repeticoes)
                else:
                    repeticoes = 1
            if max_repeticoes >= 5:
                return True

        return False