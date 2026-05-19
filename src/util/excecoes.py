class ExcecaoValidacaoSeguranca(Exception):
    def __init__(self, mensagem: str, campo: str | None = None) -> None:
        self.mensagem = mensagem
        self.campo = campo
        super().__init__(self.mensagem)

    def __str__(self) -> str:
        if self.campo:
            return f"[{self.campo}] {self.mensagem}"
        return self.mensagem
