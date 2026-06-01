from typing import List
from src.application.view_model import InputViewModel
from src.util.excecoes import ExcecaoValidacaoSeguranca


class CliEntrada:
    def __init__(self, input_view_model: InputViewModel) -> None:
        self._view_model = input_view_model

    def executar(self) -> None:
        while True:
            print("\n--- CADASTRO VIA TERMINAL ---")
            print("1. Cadastrar Ponto de Demanda")
            print("2. Cadastrar Parada de Onibus")
            print("3. Cadastrar Linha de Onibus")
            print("4. Voltar ao menu principal")

            opcao = input("Escolha uma opcao: ").strip()

            if opcao == "1":
                self._cadastrar_demanda()
            elif opcao == "2":
                self._cadastrar_parada()
            elif opcao == "3":
                self._cadastrar_linha_onibus()
            elif opcao == "4":
                break
            else:
                print("Opcao invalida!")

    def _cadastrar_demanda(self) -> None:
        print("\n--- CADASTRO DE DEMANDA ---")
        try:
            latitude = float(input("Latitude: ").strip())
            longitude = float(input("Longitude: ").strip())
            demanda = int(input("Demanda (valor inteiro): ").strip())
            nome = input("Nome (opcional): ").strip()

            dados = {
                "latitude": latitude,
                "longitude": longitude,
                "demanda": demanda,
                "nome": nome,
            }
            self._view_model.submeter_demanda(dados)
            print("Demanda cadastrada com sucesso!")
        except ExcecaoValidacaoSeguranca as e:
            print(f"Erro de validacao: {e}")
        except ValueError:
            print("Erro: valor numerico invalido.")
        except Exception as e:
            print(f"Erro inesperado: {e}")

    def _cadastrar_parada(self) -> None:
        print("\n--- CADASTRO DE PARADA ---")
        try:
            id_ = int(input("ID da parada: ").strip())
            latitude = float(input("Latitude: ").strip())
            longitude = float(input("Longitude: ").strip())
            linhas_str = input("Linhas de onibus (separadas por virgula): ").strip()
            estado = input("Estado (1-Ativa / 0-Inativa): ").strip()

            dados = {
                "id": id_,
                "latitude": latitude,
                "longitude": longitude,
                "linhas_onibus": linhas_str,
                "estado": estado == "1",
            }
            self._view_model.submeter_parada(dados)
            print("Parada cadastrada com sucesso!")
        except ExcecaoValidacaoSeguranca as e:
            print(f"Erro de validacao: {e}")
        except ValueError:
            print("Erro: valor numerico invalido.")
        except Exception as e:
            print(f"Erro inesperado: {e}")

    def _cadastrar_linha_onibus(self) -> None:
        print("\n--- CADASTRO DE LINHA DE ONIBUS ---")
        try:
            nome = input("Nome da linha: ").strip()
            capacidade = int(input("Capacidade: ").strip())
            paradas_ids_str = input("IDs das paradas (separados por virgula): ").strip()
            paradas_ids: List[int] = []
            if paradas_ids_str:
                paradas_ids = [int(x.strip()) for x in paradas_ids_str.split(",") if x.strip()]

            dados = {
                "nome": nome,
                "capacidade": capacidade,
                "paradas_ids": paradas_ids,
            }
            self._view_model.submeter_linha_onibus(dados)
            print("Linha de onibus cadastrada com sucesso!")
        except ExcecaoValidacaoSeguranca as e:
            print(f"Erro de validacao: {e}")
        except ValueError:
            print("Erro: valor numerico invalido.")
        except Exception as e:
            print(f"Erro inesperado: {e}")
