#!/usr/bin/env python3
"""Ponto de entrada principal do Sistema de Transporte Publico.

Inicializa o MainIntegrador que configura a injecao de dependencias
e orquestra todos os componentes da camada de negocios e interface CLI.
"""

import os
import sys
from src.application.main_integrador import MainIntegrador
from src.util.excecoes import ExcecaoValidacaoSeguranca

#* Menus de cadastro para cada entidade (Parada, Demanda, Linha de Ônibus) *
# Código temporário para coleta de dados do usuário, validação básica e chamadas ao ViewModel para persistência 

def menu_criar_parada(integrador: MainIntegrador) -> None:
    print("\n" + "=" * 40)
    print("      CADASTRAR NOVA PARADA DE ÔNIBUS")
    print("=" * 40)

    try:
        id_parada = input("Digite o ID da parada (inteiro): ").strip()
        coordenadas_input = input("Digite as Coordenadas (ex: -19.920, -43.940): ").strip()

        if "," not in coordenadas_input:
            print("\n❌ Erro: Formato inválido! Separe a latitude e a longitude por uma vírgula.")
            return

        lat_str, lon_str = coordenadas_input.split(",", 1)
        latitude = float(lat_str.strip())
        longitude = float(lon_str.strip())
        linhas = input("Digite as linhas atendidas (separadas por vírgula): ").strip()

        estado_input = (
            input("A parada está ativa agora? (S/N): ").strip().upper()
        )
        estado = True if estado_input == "S" else False

        dados_brutos = {
            "id": int(id_parada) if id_parada.isdigit() else id_parada,
            "latitude": float(latitude) if latitude else 0.0,
            "longitude": float(longitude) if longitude else 0.0,
            "linhas_onibus": linhas,
            "estado": estado,
        }

        print("\n[Status]: Validando regras e persistindo Parada...")
        sucesso = integrador.input_view_model.submeter_parada(dados_brutos)

        if sucesso:
            print("\n✅ Parada gravada com sucesso no arquivo JSON!")

    except ValueError:
        print("\n❌ Erro: ID precisa ser um número inteiro. Coordenadas devem ser decimais.")
    except ExcecaoValidacaoSeguranca as e:
        print(f"\n❌ Bloqueado por validação de segurança: {e}")
    except Exception as e:
        print(f"\n💥 Ocorreu um erro inesperado: {e}")


def menu_criar_demanda(integrador: MainIntegrador) -> None:
    print("\n" + "=" * 40)
    print("      CADASTRAR NOVO PONTO DE DEMANDA")
    print("=" * 40)

    try:
        nome_demanda = input("Nome do local/ponto de interesse (ex: Hospital Central): ").strip()
        coordenadas_input = input("Digite as Coordenadas (ex: -19.920, -43.940): ").strip()

        if "," not in coordenadas_input:
            print("\n❌ Erro: Formato inválido! Separe a latitude e a longitude por uma vírgula.")
            return

        lat_str, lon_str = coordenadas_input.split(",", 1)
        latitude = float(lat_str.strip())
        longitude = float(lon_str.strip())
        demanda_valor = input("Quantidade de passageiros estimada (demanda): ").strip()

        dados_brutos = {
            "nome": nome_demanda,
            "latitude": float(latitude) if latitude else 0.0,
            "longitude": float(longitude) if longitude else 0.0,
            "demanda": int(demanda_valor) if demanda_valor.isdigit() else demanda_valor,
        }

        print("\n[Status]: Validando regras e persistindo Demanda...")
        sucesso = integrador.input_view_model.submeter_demanda(dados_brutos)

        if sucesso:
            print("\n✅ Ponto de Demanda gravado com sucesso no arquivo JSON!")

    except ValueError:
        print("\n❌ Erro: Coordenadas e valor de demanda devem ser números válidos.")
    except ExcecaoValidacaoSeguranca as e:
        print(f"\n❌ Bloqueado por validação de segurança: {e}")
    except Exception as e:
        print(f"\n💥 Ocorreu um erro inesperado: {e}")


def menu_criar_linha_onibus(integrador: MainIntegrador) -> None:
    print("\n" + "=" * 40)
    print("      CADASTRAR NOVA LINHA DE ÔNIBUS")
    print("=" * 40)

    try:
        nome_linha = input("Nome/Número da Linha (ex: Move 51 ou 5102): ").strip()
        capacidade = input("Capacidade máxima do veículo (ex: 80): ").strip()
        paradas_input = input("IDs das paradas associadas (separados por vírgula, ex: 10,11,12): ").strip()

        # Converte a string de paradas em uma lista de IDs inteiros de forma segura
        lista_ids = []
        if paradas_input:
            lista_ids = [int(p.strip()) for p in paradas_input.split(",") if p.strip().isdigit()]

        dados_brutos = {
            "nome": nome_linha,
            "capacidade": int(capacidade) if capacidade.isdigit() else capacidade,
            "paradas_ids": lista_ids,
        }

        print("\n[Status]: Validando regras e persistindo Linha de Ônibus...")
        sucesso = integrador.input_view_model.submeter_linha_onibus(dados_brutos)

        if sucesso:
            print("\n✅ Linha de Ônibus gravada com sucesso no arquivo JSON!")

    except ValueError:
        print("\n❌ Erro: Capacidade e IDs de paradas devem conter apenas números válidos.")
    except ExcecaoValidacaoSeguranca as e:
        print(f"\n❌ Bloqueado por validação de segurança: {e}")
    except Exception as e:
        print(f"\n💥 Ocorreu um erro inesperado: {e}")


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
    # Inicializa e configura toda a injeção de dependências
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

    # Loop de controle do terminal CLI
    while True:
        print("\n--- SOUBUS-APO (PAINEL OPERACIONAL) ---")
        print("1. Cadastrar Ponto de Parada")
        print("2. Cadastrar Ponto de Demanda")
        print("3. Cadastrar Linha de Ônibus")
        print("4. Mostrar tela de resultados")
        print("5. Sair do Sistema")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            menu_criar_parada(integrador)
        elif opcao == "2":
            menu_criar_demanda(integrador)
        elif opcao == "3":
            menu_criar_linha_onibus(integrador)
        elif opcao == "4":
            print("\n🔄 Abrindo o Painel de Controle Visual...")
            
            # Recupera a instância da janela
            tela = integrador.tela_resultados
            
            # Passa os dados para ela processar
            tela.exibir_dados(integrador.resultado_view_model.obter_dados_tabela())
            
            tela.deiconify() 

            tela.update_idletasks()
            tela.update()
            
        elif opcao == "5":
            print("\nDesligando sistema. Até logo!")
            sys.exit(0)
        else:
            print("\nOpção inválida! Digite uma opção entre 1 e 4.")


if __name__ == "__main__":
    main()