#!/usr/bin/env python3
"""Ponto de entrada principal do Sistema de Transporte Público.

Inicializa o MainIntegrador que configura a injeção de dependências
e orquestra todos os componentes da camada de negócios.
"""

from src.application.main_integrador import MainIntegrador


def main() -> None:
    integrador = MainIntegrador()
    integrador.iniciar_aplicacao()
    print("Sistema de Transporte Público inicializado com sucesso.")


if __name__ == "__main__":
    main()
