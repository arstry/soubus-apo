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


def _abrir_tela_cadastro(integrador: MainIntegrador) -> None:
    if _tem_display():
        from src.application.view.tela_entrada import TelaEntrada
        print("\nAbrindo o Painel de Cadastro Grafico...")
        tela = integrador.tela_entrada
        tela.deiconify()
        tela.update_idletasks()
        tela.update()
    else:
        from src.application.cli_entrada import CliEntrada
        print("\nAbrindo o Painel de Cadastro via Terminal...")
        cli = CliEntrada(integrador.input_view_model)
        cli.executar()


def _abrir_tela_resultados(integrador: MainIntegrador) -> None:
    print("\nAbrindo o Painel de Resultados Grafico...")
    dados = integrador.resultado_view_model.obter_dados_tabela()
    tela = integrador.tela_resultados
    tela.exibir_dados(dados)
    tela.deiconify()
    tela.update_idletasks()
    tela.update()


def main() -> None:
    integrador = MainIntegrador()
    integrador.iniciar_aplicacao()
    print("Sistema de Transporte Publico inicializado com sucesso.")

    while True:
        print("\n--- SOUBUS-APO (PAINEL OPERACIONAL) ---")
        print("1. Abrir Tela de Cadastro")
        print("2. Abrir Tela de Resultados")
        print("3. Sair do Sistema")

        opcao = input("Escolha uma opcao: ").strip()

        if opcao == "1":
            _abrir_tela_cadastro(integrador)
        elif opcao == "2":
            _abrir_tela_resultados(integrador)
        elif opcao == "3":
            print("\nDesligando sistema. Ate logo!")
            sys.exit(0)
        else:
            print("\nOpcao invalida! Digite 1, 2 ou 3.")


if __name__ == "__main__":
    main()