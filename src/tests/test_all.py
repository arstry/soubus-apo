import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.domain.ponto import Ponto
from src.domain.demanda import Demanda
from src.domain.parada import Parada
from src.domain.linha_onibus import LinhaOnibus
from src.util.excecoes import ExcecaoValidacaoSeguranca
from src.application.processador_dados import ProcessadorDados
from src.application.view_model import InputViewModel, ResultadoViewModel
from src.application.main_integrador import MainIntegrador
from src.data.gerenciador_json_dados import GerenciadorJsonDados
from src.data.gerenciador_autenticacao import GerenciadorAutenticacao



class TestPonto(unittest.TestCase):
    def test_inicializacao_valores_padrao(self):
        p = Ponto()
        self.assertEqual(p.get_latitude(), 0.0)
        self.assertEqual(p.get_longitude(), 0.0)

    def test_inicializacao_com_valores(self):
        p = Ponto(latitude=-19.917, longitude=-43.934)
        self.assertEqual(p.get_latitude(), -19.917)
        self.assertEqual(p.get_longitude(), -43.934)

    def test_getters_e_setters(self):
        p = Ponto()
        p.set_latitude(-23.550)
        p.set_longitude(-46.633)
        self.assertEqual(p.get_latitude(), -23.550)
        self.assertEqual(p.get_longitude(), -46.633)

    def test_to_dict(self):
        p = Ponto(latitude=-19.917, longitude=-43.934)
        d = p.to_dict()
        self.assertEqual(d, {"latitude": -19.917, "longitude": -43.934})

    def test_from_dict(self):
        d = {"latitude": -23.550, "longitude": -46.633}
        p = Ponto.from_dict(d)
        self.assertEqual(p.get_latitude(), -23.550)
        self.assertEqual(p.get_longitude(), -46.633)


class TestDemanda(unittest.TestCase):
    def test_inicializacao_valores_padrao(self):
        d = Demanda()
        self.assertEqual(d.get_latitude(), 0.0)
        self.assertEqual(d.get_longitude(), 0.0)
        self.assertEqual(d.get_demanda(), 0)
        self.assertEqual(d.get_nome(), "")

    def test_inicializacao_com_valores(self):
        d = Demanda(latitude=-19.917, longitude=-43.934, demanda=150, nome="Centro")
        self.assertEqual(d.get_latitude(), -19.917)
        self.assertEqual(d.get_longitude(), -43.934)
        self.assertEqual(d.get_demanda(), 150)
        self.assertEqual(d.get_nome(), "Centro")

    def test_getters_e_setters(self):
        d = Demanda()
        d.set_demanda(300)
        d.set_nome("Estação Norte")
        self.assertEqual(d.get_demanda(), 300)
        self.assertEqual(d.get_nome(), "Estação Norte")

    def test_to_dict(self):
        d = Demanda(latitude=-19.917, longitude=-43.934, demanda=150, nome="Centro")
        dados = d.to_dict()
        self.assertEqual(dados["latitude"], -19.917)
        self.assertEqual(dados["longitude"], -43.934)
        self.assertEqual(dados["demanda"], 150)
        self.assertEqual(dados["nome"], "Centro")

    def test_from_dict(self):
        dados = {"latitude": -19.917, "longitude": -43.934, "demanda": 150, "nome": "Centro"}
        d = Demanda.from_dict(dados)
        self.assertEqual(d.get_latitude(), -19.917)
        self.assertEqual(d.get_longitude(), -43.934)
        self.assertEqual(d.get_demanda(), 150)
        # Nota: Este assert vai falhar no seu código atual (ver Avisos abaixo)
        self.assertEqual(d.get_nome(), "Centro")


class TestLinhaOnibus(unittest.TestCase):
    def test_inicializacao_valores_padrao(self):
        l = LinhaOnibus()
        self.assertEqual(l.get_nome(), "")
        self.assertEqual(l.get_capacidade(), 0)
        self.assertEqual(l.get_paradas_ids(), [])

    def test_inicializacao_com_valores(self):
        l = LinhaOnibus(nome="A10", capacidade=80, paradas_ids=[1, 2, 3])
        self.assertEqual(l.get_nome(), "A10")
        self.assertEqual(l.get_capacidade(), 80)
        self.assertEqual(l.get_paradas_ids(), [1, 2, 3])

    def test_getters_e_setters(self):
        l = LinhaOnibus()
        l.set_nome("B20")
        l.set_capacidade(50)
        l.set_paradas_ids([10, 20])
        self.assertEqual(l.get_nome(), "B20")
        self.assertEqual(l.get_capacidade(), 50)
        self.assertEqual(l.get_paradas_ids(), [10, 20])

    def test_to_dict(self):
        l = LinhaOnibus(nome="A10", capacidade=80, paradas_ids=[1, 2, 3])
        dados = l.to_dict()
        self.assertEqual(dados, {"nome": "A10", "capacidade": 80, "paradas_ids": [1, 2, 3]})

    def test_from_dict(self):
        dados = {"nome": "A10", "capacidade": 80, "paradas_ids": [1, 2, 3]}
        l = LinhaOnibus.from_dict(dados)
        self.assertEqual(l.get_nome(), "A10")
        self.assertEqual(l.get_paradas_ids(), [1, 2, 3])
        # Nota: Este assert vai falhar no seu código atual (ver Avisos abaixo)
        self.assertEqual(l.get_capacidade(), 80)


class TestParada(unittest.TestCase):
    def test_inicializacao_valores_padrao(self):
        p = Parada()
        self.assertEqual(p.get_id(), 0)
        self.assertEqual(p.get_latitude(), 0.0)
        self.assertEqual(p.get_longitude(), 0.0)
        self.assertEqual(p.get_linhas_onibus(), [])
        self.assertFalse(p.get_estado())

    def test_inicializacao_com_valores(self):
        p = Parada(id=5, latitude=-19.9, longitude=-43.9, linhas_onibus=["A10", "B20"], estado=True)
        self.assertEqual(p.get_id(), 5)
        self.assertEqual(p.get_latitude(), -19.9)
        self.assertEqual(p.get_longitude(), -43.9)
        self.assertEqual(p.get_linhas_onibus(), ["A10", "B20"])
        self.assertTrue(p.get_estado())

    def test_getters_e_setters(self):
        p = Parada()
        p.set_linhas_onibus(["C30"])
        p.set_estado(True)
        self.assertEqual(p.get_linhas_onibus(), ["C30"])
        self.assertTrue(p.get_estado())

    def test_to_dict(self):
        p = Parada(id=5, latitude=-19.9, longitude=-43.9, linhas_onibus=["A10"], estado=True)
        # Nota: Esta chamada vai falhar no seu código atual (ver Avisos abaixo)
        dados = p.to_dict()
        self.assertEqual(dados["id"], 5)
        self.assertEqual(dados["latitude"], -19.9)
        self.assertEqual(dados["linhas_onibus"], ["A10"])
        self.assertTrue(dados["estado"])


class TestExcecaoValidacaoSeguranca(unittest.TestCase):
    def test_mensagem_simples(self):
        exc = ExcecaoValidacaoSeguranca("Erro de validação")
        self.assertEqual(str(exc), "Erro de validação")

    def test_mensagem_com_campo(self):
        exc = ExcecaoValidacaoSeguranca("Valor inválido", campo="latitude")
        self.assertIn("latitude", str(exc))
        self.assertIn("Valor inválido", str(exc))


class TestProcessadorDados(unittest.TestCase):
    def setUp(self):
        self.processador = ProcessadorDados()

    def test_processar_dados_validos(self):
        dados = {
            "latitude": -19.917,
            "longitude": -43.934,
            "demanda": 150,
            "linhas_onibus": ["5102", "8103"],
            "tipo_de_ponto": "Ponto de Ônibus",
        }
        ponto = self.processador.processar(dados)
        self.assertEqual(ponto.get_latitude(), -19.917)
        self.assertEqual(ponto.get_longitude(), -43.934)
        self.assertEqual(ponto.get_demanda(), 150)
        self.assertEqual(ponto.get_tipo_de_ponto(), "PONTO DE ONIBUS")

    def test_processar_demanda_negativa_lanca_excecao(self):
        dados = {"latitude": -19.917, "longitude": -43.934, "demanda": -1,
                 "linhas_onibus": "5102", "tipo_de_ponto": "TERMINAL"}
        with self.assertRaises(ExcecaoValidacaoSeguranca):
            self.processador.processar(dados)

    def test_processar_latitude_invalida(self):
        dados = {"latitude": 100.0, "longitude": -43.934, "demanda": 10,
                 "linhas_onibus": "5102", "tipo_de_ponto": "TERMINAL"}
        with self.assertRaises(ExcecaoValidacaoSeguranca):
            self.processador.processar(dados)

    def test_processar_longitude_invalida(self):
        dados = {"latitude": -19.917, "longitude": -200.0, "demanda": 10,
                 "linhas_onibus": "5102", "tipo_de_ponto": "TERMINAL"}
        with self.assertRaises(ExcecaoValidacaoSeguranca):
            self.processador.processar(dados)

    def test_remover_acentos_e_maiusculo(self):
        resultado = self.processador.remover_acentos_e_maiusculo("Ponto de Ônibus")
        self.assertEqual(resultado, "PONTO DE ONIBUS")

    def test_truncar_coordenadas(self):
        resultado = self.processador.truncar_coordenadas(-19.917456789)
        self.assertEqual(resultado, -19.917456)

    def test_neutralizar_injecao_comandos(self):
        resultado = self.processador.neutralizar_injecao_comandos("texto; rm -rf /")
        self.assertEqual(resultado, "texto rm -rf /")

    def test_neutralizar_injecao_trunca_texto_longo(self):
        texto_longo = "A" * 300
        resultado = self.processador.neutralizar_injecao_comandos(texto_longo)
        self.assertEqual(len(resultado), 200)

    def test_detectar_flood_caractere_unico(self):
        self.assertTrue(self.processador.detectar_flood_nonsense("aaaaaaaaaa"))

    def test_detectar_flood_repeticoes(self):
        self.assertTrue(self.processador.detectar_flood_nonsense("abaaaaaacd"))

    def test_detectar_flood_texto_normal(self):
        self.assertFalse(self.processador.detectar_flood_nonsense("PONTO DE ONIBUS"))

    def test_processar_linhas_onibus_por_string(self):
        resultado = self.processador._processar_linhas_onibus("5102, 8103, 9104")
        self.assertEqual(resultado, ["5102", "8103", "9104"])

    def test_processar_dados_brutos_nao_dict(self):
        with self.assertRaises(ExcecaoValidacaoSeguranca):
            self.processador.processar("não é um dict")


class TestGerenciadorJsonDados(unittest.TestCase):
    def setUp(self):
        self.arquivo_teste = "test_dados_pontos.json"
        self.gerenciador = GerenciadorJsonDados(caminho_arquivo=self.arquivo_teste)

    def tearDown(self):
        if os.path.exists(self.arquivo_teste):
            os.remove(self.arquivo_teste)

    def test_inicializacao_cria_arquivo(self):
        self.assertTrue(os.path.exists(self.arquivo_teste))

    def test_salvar_e_carregar_registros(self):
        ponto = Ponto(-19.917, -43.934, 100, ["5102"], "TERMINAL")
        self.gerenciador.salvar_registro(ponto)

        registros = self.gerenciador.carregar_registros()
        self.assertEqual(len(registros), 1)
        self.assertEqual(registros[0], ponto)

    def test_carregar_arquivo_vazio_retorna_lista_vazia(self):
        registros = self.gerenciador.carregar_registros()
        self.assertEqual(registros, [])

    def test_multiplos_registros(self):
        pontos = [
            Ponto(-19.917, -43.934, 100, ["5102"], "TERMINAL"),
            Ponto(-19.920, -43.940, 50, ["8103"], "PONTO DE ONIBUS"),
        ]
        for p in pontos:
            self.gerenciador.salvar_registro(p)

        registros = self.gerenciador.carregar_registros()
        self.assertEqual(len(registros), 2)
        self.assertEqual(registros[0], pontos[0])
        self.assertEqual(registros[1], pontos[1])


class TestGerenciadorAutenticacao(unittest.TestCase):
    def setUp(self):
        self.arquivo_teste = "test_config_usuarios.json"
        self.gerenciador = GerenciadorAutenticacao(caminho_arquivo_config=self.arquivo_teste)

    def tearDown(self):
        if os.path.exists(self.arquivo_teste):
            os.remove(self.arquivo_teste)

    def test_inicializacao_cria_arquivo(self):
        self.assertTrue(os.path.exists(self.arquivo_teste))

    def test_credenciais_invalidas_sem_hash(self):
        resultado = self.gerenciador.validar_credenciais("admin", "senha123")
        self.assertFalse(resultado)

    def test_usuario_inexistente(self):
        resultado = self.gerenciador.validar_credenciais("usuario_falso", "senha")
        self.assertFalse(resultado)


class TestInputViewModel(unittest.TestCase):
    def setUp(self):
        self.arquivo_teste = "test_vm_dados.json"
        self.repositorio = GerenciadorJsonDados(caminho_arquivo=self.arquivo_teste)
        self.processador = ProcessadorDados()
        self.vm = InputViewModel(
            repositorio=self.repositorio, processador=self.processador
        )

    def tearDown(self):
        if os.path.exists(self.arquivo_teste):
            os.remove(self.arquivo_teste)

    def test_submeter_dados_validos(self):
        dados = {"latitude": -19.917, "longitude": -43.934, "demanda": 100,
                 "linhas_onibus": "5102", "tipo_de_ponto": "TERMINAL"}
        resultado = self.vm.submeter_dados(dados)
        self.assertTrue(resultado)
        from src.application.estados import EstadosTelaEntrada
        self.assertEqual(self.vm.uiState, EstadosTelaEntrada.SUCESSO)

    def test_submeter_dados_invalidos_lanca_excecao(self):
        dados = {"latitude": -19.917, "longitude": -43.934, "demanda": -1,
                 "linhas_onibus": "5102", "tipo_de_ponto": "TERMINAL"}
        with self.assertRaises(ExcecaoValidacaoSeguranca):
            self.vm.submeter_dados(dados)


class TestResultadoViewModel(unittest.TestCase):
    def setUp(self):
        self.arquivo_dados = "test_vm2_dados.json"
        self.arquivo_config = "test_vm2_config.json"
        self.repositorio = GerenciadorJsonDados(caminho_arquivo=self.arquivo_dados)
        self.autenticador = GerenciadorAutenticacao(caminho_arquivo_config=self.arquivo_config)
        self.vm = ResultadoViewModel(
            repositorio=self.repositorio, autenticador=self.autenticador
        )

    def tearDown(self):
        for f in [self.arquivo_dados, self.arquivo_config]:
            if os.path.exists(f):
                os.remove(f)
        for f in ["exportacao_pontos.csv", "exportacao_pontos.json"]:
            if os.path.exists(f):
                os.remove(f)

    def test_realizar_login_credenciais_invalidas(self):
        resultado = self.vm.realizar_login("admin", "senha_errada")
        self.assertFalse(resultado)

    def test_obter_dados_tabela_vazia(self):
        registros = self.vm.obter_dados_tabela()
        self.assertEqual(registros, [])

    def test_processar_exportacao_csv(self):
        ponto = Ponto(-19.917, -43.934, 100, ["5102"], "TERMINAL")
        self.repositorio.salvar_registro(ponto)
        caminho = self.vm.processar_exportacao("csv")
        self.assertTrue(os.path.exists(caminho))

    def test_processar_exportacao_json(self):
        ponto = Ponto(-19.917, -43.934, 100, ["5102"], "TERMINAL")
        self.repositorio.salvar_registro(ponto)
        caminho = self.vm.processar_exportacao("json")
        self.assertTrue(os.path.exists(caminho))

    def test_processar_exportacao_formato_invalido(self):
        with self.assertRaises(ValueError):
            self.vm.processar_exportacao("xml")


class TestMainIntegrador(unittest.TestCase):
    def test_iniciar_aplicacao(self):
        integrador = MainIntegrador()
        integrador.iniciar_aplicacao()

        self.assertIsNotNone(integrador.input_view_model)
        self.assertIsNotNone(integrador.resultado_view_model)

        from src.application.estados import EstadosTelaEntrada, EstadosTelaResultado
        self.assertEqual(integrador.input_view_model.uiState,
                         EstadosTelaEntrada.OCIOSO)
        self.assertEqual(integrador.resultado_view_model.uiState,
                         EstadosTelaResultado.OCIOSO)

    def test_acesso_sem_inicializar_lanca_excecao(self):
        integrador = MainIntegrador()
        with self.assertRaises(RuntimeError):
            _ = integrador.input_view_model
        with self.assertRaises(RuntimeError):
            _ = integrador.resultado_view_model

    def tearDown(self):
        for f in ["dados_pontos.json", "config_usuarios.json"]:
            if os.path.exists(f):
                os.remove(f)


if __name__ == "__main__":
    unittest.main()
