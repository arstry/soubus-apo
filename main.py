#!/usr/bin/env python3
"""Ponto de entrada principal do Sistema de Transporte Publico.

Inicializa o MainIntegrador que configura a injecao de dependencias
e orquestra todos os componentes da camada de negocios e interface CLI.
"""

import sys
from src.application.main_integrador import MainIntegrador


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
            print("\nAbrindo o Painel de Cadastro...")
            tela = integrador.tela_entrada
            tela.deiconify()
            tela.update_idletasks()
            tela.update()
        elif opcao == "2":
            print("\nDesligando sistema. Ate logo!")
            sys.exit(0)
        else:
            print("\nOpcao invalida! Digite 1 ou 2.")


if __name__ == "__main__":
    main()
