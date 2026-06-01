#!/usr/bin/env python3
"""Ponto de entrada principal do Sistema de Transporte Publico.

Inicializa o MainIntegrador que configura a injecao de dependencias
e orquestra todos os componentes da camada de negocios e interface CLI.
"""

import os
import sys
from src.application.main_integrador import MainIntegrador


def _tem_display() -> bool:
    return bool(os.environ.get("DISPLAY"))


def _abrir_tela_grafica(integrador: MainIntegrador) -> None:
    from src.application.view.tela_entrada import TelaEntrada
    print("\nAbrindo o Painel de Cadastro Grafico...")
    tela = integrador.tela_entrada
    tela.deiconify()
    tela.update_idletasks()
    tela.update()


def _abrir_cli_cadastro(integrador: MainIntegrador) -> None:
    from src.application.cli_entrada import CliEntrada
    print("\nAbrindo o Painel de Cadastro via Terminal...")
    cli = CliEntrada(integrador.input_view_model)
    cli.executar()


def main() -> None:
    integrador = MainIntegrador()
    integrador.iniciar_aplicacao()
    print("Sistema de Transporte Publico inicializado com sucesso.")

    while True:
        print("\n--- SOUBUS-APO (PAINEL OPERACIONAL) ---")
        print("1. Abrir Tela de Cadastro")
        print("2. Sair do Sistema")

        opcao = input("Escolha uma opcao: ").strip()

        if opcao == "1":
            if _tem_display():
                _abrir_tela_grafica(integrador)
            else:
                _abrir_cli_cadastro(integrador)
        elif opcao == "2":
            print("\nDesligando sistema. Ate logo!")
            sys.exit(0)
        else:
            print("\nOpcao invalida! Digite 1 ou 2.")


if __name__ == "__main__":
    main()
