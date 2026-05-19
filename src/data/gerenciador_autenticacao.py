import hashlib
import json
import os
import secrets


class GerenciadorAutenticacao:
    CONFIG_PADRAO: dict = {
        "usuarios": [
            {
                "usuario": "admin",
                "hash_senha": "",
                "salt": "",
            }
        ]
    }

    def __init__(self, caminho_arquivo_config: str | None = None) -> None:
        if caminho_arquivo_config is None:
            static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
            caminho_arquivo_config = os.path.join(static_dir, "config_usuarios.json")
        self._caminho_arquivo_config = caminho_arquivo_config
        self._garantir_arquivo_config()

    def validar_credenciais(self, usuario: str, senha_plana: str) -> bool:
        config = self._carregar_config()
        for entrada in config.get("usuarios", []):
            if entrada.get("usuario") == usuario:
                hash_salvo = entrada.get("hash_senha", "")
                salt = entrada.get("salt", "")
                return self._validar_hash(senha_plana, hash_salvo, salt)
        return False

    def _validar_hash(self, senha_plana: str, hash_salvo: str, salt: str) -> bool:
        if not hash_salvo or not salt:
            return False
        hash_calculado = hashlib.pbkdf2_hmac(
            "sha256",
            senha_plana.encode("utf-8"),
            salt.encode("utf-8"),
            100_000,
        ).hex()
        return secrets.compare_digest(hash_calculado, hash_salvo)

    def _garantir_arquivo_config(self) -> None:
        if not os.path.exists(self._caminho_arquivo_config):
            self._salvar_config(self.CONFIG_PADRAO)

    def _carregar_config(self) -> dict:
        with open(self._caminho_arquivo_config, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)

    def _salvar_config(self, dados: dict) -> None:
        diretorio = os.path.dirname(self._caminho_arquivo_config)
        if diretorio:
            os.makedirs(diretorio, exist_ok=True)
        with open(self._caminho_arquivo_config, "w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, ensure_ascii=False, indent=2)
