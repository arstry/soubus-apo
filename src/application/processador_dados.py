import re
import unicodedata
from typing import List

from src.domain.ponto import Ponto
from src.util.excecoes import ExcecaoValidacaoSeguranca


class ProcessadorDados:
    PRECISAO_COORDENADAS: int = 6
    TAMANHO_MAXIMO_TEXTO: int = 200
    PADRAO_INJECAO: re.Pattern = re.compile(r"[;&|`$(){}\[\]<>!\\'\"]")

    def processar(self, dados_brutos: dict) -> Ponto:
        if not isinstance(dados_brutos, dict):
            raise ExcecaoValidacaoSeguranca("Dados brutos devem ser um dicionário.")

        latitude = float(dados_brutos.get("latitude", 0.0))
        longitude = float(dados_brutos.get("longitude", 0.0))
        demanda = int(dados_brutos.get("demanda", 0))
        linhas_onibus_raw = dados_brutos.get("linhas_onibus", "")
        tipo_de_ponto = str(dados_brutos.get("tipo_de_ponto", ""))

        linhas_onibus = self._processar_linhas_onibus(linhas_onibus_raw)
        tipo_de_ponto = self.remover_acentos_e_maiusculo(tipo_de_ponto)
        tipo_de_ponto = self.neutralizar_injecao_comandos(tipo_de_ponto)

        if self.detectar_flood_nonsense(tipo_de_ponto):
            raise ExcecaoValidacaoSeguranca(
                "Texto do tipo de ponto contém padrão suspeito de flood.", "tipo_de_ponto"
            )

        linhas_onibus = [
            self.neutralizar_injecao_comandos(
                self.remover_acentos_e_maiusculo(linha)
            )
            for linha in linhas_onibus
        ]
        linhas_onibus = [
            linha for linha in linhas_onibus if not self.detectar_flood_nonsense(linha)
        ]

        if demanda < 0:
            raise ExcecaoValidacaoSeguranca("Demanda não pode ser negativa.", "demanda")

        latitude = self.truncar_coordenadas(latitude)
        longitude = self.truncar_coordenadas(longitude)

        if not (-90.0 <= latitude <= 90.0):
            raise ExcecaoValidacaoSeguranca(
                "Latitude fora do intervalo válido [-90, 90].", "latitude"
            )
        if not (-180.0 <= longitude <= 180.0):
            raise ExcecaoValidacaoSeguranca(
                "Longitude fora do intervalo válido [-180, 180].", "longitude"
            )

        return Ponto(
            latitude=latitude,
            longitude=longitude,
            demanda=demanda,
            linhas_onibus=linhas_onibus,
            tipo_de_ponto=tipo_de_ponto,
        )

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

    def _processar_linhas_onibus(self, linhas_raw: str | list) -> List[str]:
        if isinstance(linhas_raw, list):
            return [str(item).strip() for item in linhas_raw if str(item).strip()]
        if isinstance(linhas_raw, str):
            partes = re.split(r"[,;\n]+", linhas_raw)
            return [p.strip() for p in partes if p.strip()]
        return []
