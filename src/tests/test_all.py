import os
import sys
import unittest
import json

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
from src.application.estados import EstadosTelaEntrada, EstadosTelaResultado


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

class TestGerenciadorJsonDados(unittest.TestCase):
    def setUp(self):
        # Usamos um arquivo temporário exclusivo para os testes
        self.arquivo_teste = "test_dados_sistema.json"
        self.gerenciador = GerenciadorJsonDados(caminho_arquivo=self.arquivo_teste)

    def tearDown(self):
        # Limpa o ambiente removendo o arquivo criado após cada teste
        if os.path.exists(self.arquivo_teste):
            os.remove(self.arquivo_teste)

    def test_inicializacao_cria_esquema_padrao_correto(self):
        """Testa se o arquivo é criado com a nova estrutura de três listas."""
        self.assertTrue(os.path.exists(self.arquivo_teste))
        
        # Carrega o arquivo puro para validar as chaves estruturais
        dados = self.gerenciador._carregar_arquivo()
        self.assertIn("demandas", dados)
        self.assertIn("paradas", dados)
        self.assertIn("linhas_onibus", dados)
        self.assertEqual(dados["demandas"], [])

    def test_salvar_e_carregar_todos_os_pontos_misturados(self):
        """Testa o comportamento polimórfico: salva entidades em caixas separadas

        e recupera tudo junto como instâncias corretas na ordem especificada.
        """
        demanda = Demanda(latitude=-19.917, longitude=-43.934, demanda=150, nome="Centro")
        parada = Parada(id=1, latitude=-19.920, longitude=-43.940, linhas_onibus=["5102", "3054"])

        # Salva utilizando os métodos específicos correspondentes
        self.gerenciador.salvar_registro_demanda(demanda)
        self.gerenciador.salvar_registro_parada(parada)

        # Carrega a lista unificada de pontos geográficos
        pontos = self.gerenciador.carregar_todos_os_pontos()

        self.assertEqual(len(pontos), 2)
        
        # Garante que os objetos retornados mantiveram seus tipos e dados originais
        self.assertIsInstance(pontos[0], Demanda)
        self.assertEqual(pontos[0].get_demanda(), 150)
        self.assertEqual(pontos[0].get_nome(), "Centro")

        self.assertIsInstance(pontos[1], Parada)
        self.assertEqual(pontos[1].get_id(), 1)
        self.assertIn("5102", pontos[1].get_linhas_onibus())

    def test_salvar_e_carregar_linhas_onibus_isoladas(self):
        """Testa se as linhas de ônibus estão sendo isoladas corretamente das coordenadas de pontos."""
        linha = LinhaOnibus(nome="8103", capacidade=80, paradas_ids=[1, 2, 3])
        
        self.gerenciador.salvar_registro_linha_onibus(linha)
        
        # Verifica se as linhas de ônibus não vazam para a lista de pontos geográficos
        pontos = self.gerenciador.carregar_todos_os_pontos()
        self.assertEqual(len(pontos), 0)

        # Verifica se conseguimos carregar a linha de ônibus isoladamente
        linhas = self.gerenciador.carregar_registros_linha_onibus()
        self.assertEqual(len(linhas), 1)
        self.assertEqual(linhas[0].get_nome(), "8103")
        self.assertEqual(linhas[0].get_capacidade(), 80)

    def test_garantir_integridade_corrige_estrutura_antiga_ou_invalida(self):
        """Testa se o validador limpa e regenera o arquivo caso encontre um JSON corrompido

        ou no formato do sistema antigo (com a chave 'registros').
        """
        # Força a escrita de um layout inválido/antigo no arquivo
        dados_corrompidos = {"registros": [{"latitude": 0.0, "longitude": 0.0}]}
        self.gerenciador._salvar_arquivo(dados_corrompidos)

        # Dispara manualmente o validador (que também roda no __init__)
        self.gerenciador._garantir_integridade_esquema()

        # O arquivo deve ter sido resetado para o esquema padrão seguro
        dados_corrigidos = self.gerenciador._carregar_arquivo()
        self.assertNotIn("registros", dados_corrigidos)
        self.assertIn("demandas", dados_corrigidos)

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

    def test_processar_demanda_valida(self):
        """Testa o processamento específico de um dicionário de Demanda."""
        dados = {
            "latitude": -19.9174567,
            "longitude": -43.9341234,
            "demanda": 150,
            "nome": "Estação Central",
        }
        demanda = self.processador.processar_demanda(dados)
        
        self.assertIsInstance(demanda, Demanda)
        self.assertEqual(demanda.get_latitude(), -19.917456)  
        self.assertEqual(demanda.get_longitude(), -43.934123)
        self.assertEqual(demanda.get_demanda(), 150)
        self.assertEqual(demanda.get_nome(), "ESTACAO CENTRAL")  

    def test_processar_parada_valida(self):
        """Testa o processamento específico de um dicionário de Parada."""
        dados = {
            "id": 42,
            "latitude": -19.920,
            "longitude": -43.940,
            "linhas_onibus": "5102, 8103; 9104\n3054",
            "estado": True,
        }
        parada = self.processador.processar_parada(dados)

        self.assertIsInstance(parada, Parada)
        self.assertEqual(parada.get_id(), 42)
        self.assertEqual(parada.get_estado(), True)
        self.assertEqual(parada.get_linhas_onibus(), ["5102", "8103", "9104", "3054"])

    def test_processar_linha_onibus_valida(self):
        """Testa o processamento específico de uma linha de ônibus (sem coordenadas)."""
        dados = {
            "nome": "Linha Trólebus 10",
            "capacidade": 80,
            "paradas_ids": [1, 2, 3]
        }
        linha = self.processador.processar_linha_onibus(dados)

        self.assertIsInstance(linha, LinhaOnibus)
        self.assertEqual(linha.get_nome(), "LINHA TROLEBUS 10")
        self.assertEqual(linha.get_capacidade(), 80)
        self.assertEqual(linha.get_paradas_ids(), [1, 2, 3])

    def test_processar_linha_onibus_capacidade_negativa_lanca_excecao(self):
        """Garante que capacidades inválidas para linhas disparem erro de segurança."""
        dados = {"nome": "9106", "capacidade": -5, "paradas_ids": []}
        with self.assertRaises(ExcecaoValidacaoSeguranca):
            self.processador.processar_linha_onibus(dados)

    def test_processar_dados_brutos_nao_dict_lanca_excecao(self):
        """Garante que entradas malformadas sejam rejeitadas em todos os métodos."""
        with self.assertRaises(ExcecaoValidacaoSeguranca):
            self.processador.processar_demanda("não é um dict")
        with self.assertRaises(ExcecaoValidacaoSeguranca):
            self.processador.processar_parada([])

    def test_processar_demanda_negativa_lanca_excecao(self):
        dados = {"latitude": -19.917, "longitude": -43.934, "demanda": -1, "nome": "Teste"}
        with self.assertRaises(ExcecaoValidacaoSeguranca):
            self.processador.processar_demanda(dados)

    def test_processar_latitude_invalida(self):
        dados = {"latitude": 100.0, "longitude": -43.934, "demanda": 10, "nome": "Teste"}
        with self.assertRaises(ExcecaoValidacaoSeguranca):
            self.processador.processar_demanda(dados)

    def test_processar_longitude_invalida(self):
        dados = {"latitude": -19.917, "longitude": -200.0, "demanda": 10, "nome": "Teste"}
        with self.assertRaises(ExcecaoValidacaoSeguranca):
            self.processador.processar_demanda(dados)


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
        resultado = self.processador._processar_lista_linhas_onibus("5102, 8103, 9104")
        self.assertEqual(resultado, ["5102", "8103", "9104"])


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

    def test_submeter_demanda_valida(self):
        """Testa o fluxo completo de sucesso ao submeter uma Demanda."""
        dados = {
            "latitude": -19.917,
            "longitude": -43.934,
            "demanda": 100,
            "nome": "Terminal Central",
        }
        resultado = self.vm.submeter_demanda(dados)
        self.assertTrue(resultado)
        self.assertEqual(self.vm.uiState, EstadosTelaEntrada.SUCESSO)

        # Garante que foi persistido corretamente no banco de dados
        registros = self.repositorio.carregar_todos_os_pontos()
        self.assertEqual(len(registros), 1)
        self.assertIsInstance(registros[0], Demanda)

    def test_submeter_parada_valida(self):
        """Testa o fluxo completo de sucesso ao submeter uma Parada de ônibus."""
        dados = {
            "id": 10,
            "latitude": -19.920,
            "longitude": -43.940,
            "linhas_onibus": "5102, 8103",
            "estado": True,
        }
        resultado = self.vm.submeter_parada(dados)
        self.assertTrue(resultado)
        self.assertEqual(self.vm.uiState, EstadosTelaEntrada.SUCESSO)

        registros = self.repositorio.carregar_todos_os_pontos()
        self.assertEqual(len(registros), 1)
        self.assertIsInstance(registros[0], Parada)

    def test_submeter_linha_onibus_valida(self):
        """Testa a submissão de uma linha operacional de ônibus (sem coordenadas)."""
        dados = {
            "nome": "Move 51",
            "capacidade": 120,
            "paradas_ids": [10, 11, 12]
        }
        resultado = self.vm.submeter_linha_onibus(dados)
        self.assertTrue(resultado)
        self.assertEqual(self.vm.uiState, EstadosTelaEntrada.SUCESSO)

        # Verifica se foi armazenado na gaveta isolada de linhas de ônibus
        linhas = self.repositorio.carregar_registros_linha_onibus()
        self.assertEqual(len(linhas), 1)
        self.assertEqual(linhas[0].get_nome(), "MOVE 51")

    def test_submeter_demanda_invalidas_altera_estado_para_erro(self):
        """Garante que falhas de validação alterem o uiState para ERRO e relancem a exceção."""
        dados = {
            "latitude": -19.917,
            "longitude": -43.934,
            "demanda": -50,  # Demanda inválida
            "nome": "Erro",
        }
        with self.assertRaises(ExcecaoValidacaoSeguranca):
            self.vm.submeter_demanda(dados)
        self.assertEqual(self.vm.uiState, EstadosTelaEntrada.ERRO)

class TestResultadoViewModel(unittest.TestCase):
    def setUp(self):
        self.arquivo_dados = "test_vm2_dados.json"
        self.arquivo_config = "test_vm2_config.json"
        self.repositorio = GerenciadorJsonDados(caminho_arquivo=self.arquivo_dados)
        self.autenticador = GerenciadorAutenticacao(
            caminho_arquivo_config=self.arquivo_config
        )
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
        self.assertEqual(self.vm.uiState, EstadosTelaResultado.ERRO)

    def test_obter_dados_tabela_vazia(self):
        registros = self.vm.obter_dados_tabela()
        self.assertEqual(registros, [])
        self.assertEqual(self.vm.uiState, EstadosTelaResultado.AUTENTICADO)

    def test_obter_linhas_onibus_cadastradas(self):
        """Garante que a ViewModel busca corretamente as linhas operacionais armazenadas."""
        linha = LinhaOnibus(nome="8103", capacidade=70)
        self.repositorio.salvar_registro_linha_onibus(linha)

        linhas_recuperadas = self.vm.obter_linhas_onibus()
        self.assertEqual(len(linhas_recuperadas), 1)
        self.assertEqual(linhas_recuperadas[0].get_nome(), "8103")

    def test_processar_exportacao_csv_polimorfico(self):
        """Valida se a exportação em CSV processa com segurança objetos mistos (Demanda e Parada)."""
        demanda = Demanda(
            latitude=-19.917, longitude=-43.934, demanda=100, nome="Centro"
        )
        parada = Parada(
            id=1, latitude=-19.920, longitude=-43.940, linhas_onibus=["5102"]
        )

        self.repositorio.salvar_registro_demanda(demanda)
        self.repositorio.salvar_registro_parada(parada)

        caminho = self.vm.processar_exportacao("csv")
        self.assertTrue(os.path.exists(caminho))
        self.assertEqual(self.vm.uiState, EstadosTelaResultado.AUTENTICADO)

    def test_processar_exportacao_json_com_filtros(self):
        """Testa o isolamento de filtros textuais ao gerar uma exportação parcial em JSON."""
        parada_com_linha = Parada(
            id=1, latitude=-19.920, longitude=-43.940, linhas_onibus=["5102"]
        )
        parada_sem_linha = Parada(
            id=2, latitude=-19.930, longitude=-43.950, linhas_onibus=["9106"]
        )

        self.repositorio.salvar_registro_parada(parada_com_linha)
        self.repositorio.salvar_registro_parada(parada_sem_linha)

        # Filtra a exportação exigindo a correspondência com a linha "5102"
        caminho = self.vm.processar_exportacao("json", filtros_linhas=["5102"])
        self.assertTrue(os.path.exists(caminho))

        with open(caminho, "r", encoding="utf-8") as f:
            dados_exportados = json.load(f)
            # A parada que atende à linha procurada deve persistir
            self.assertTrue(
                any(d.get("id") == 1 for d in dados_exportados if "id" in d)
            )
            # A parada sem vinculação à linha deve ser removida pelo filtro
            self.assertFalse(
                any(d.get("id") == 2 for d in dados_exportados if "id" in d)
            )

    def test_processar_exportacao_formato_invalido(self):
        """Garante que formatos não mapeados lancem erro e alterem o estado visual."""
        with self.assertRaises(ValueError):
            self.vm.processar_exportacao("xml")
        self.assertEqual(self.vm.uiState, EstadosTelaResultado.ERRO)


    def test_processar_exportacao_preserva_demandas_sob_filtros_de_linha(self):
        """Garante que instâncias de Demanda não sejam expurgadas por filtros direcionados a Paradas."""
        demanda = Demanda(
            latitude=-19.915, longitude=-43.930, demanda=80, nome="Hospital"
        )
        parada = Parada(
            id=3, latitude=-19.922, longitude=-43.944, linhas_onibus=["8103"]
        )

        self.repositorio.salvar_registro_demanda(demanda)
        self.repositorio.salvar_registro_parada(parada)

        # Aplica filtro para uma linha que a parada não possui
        caminho = self.vm.processar_exportacao("json", filtros_linhas=["5102"])

        with open(caminho, "r", encoding="utf-8") as f:
            dados_exportados = json.load(f)
            # A parada id=3 deve sumir pois não atende à linha "5102"
            self.assertFalse(
                any(d.get("id") == 3 for d in dados_exportados if "id" in d)
            )
            # A Demanda geral deve continuar no relatório consolidado
            self.assertTrue(
                any(d.get("nome").upper() == "HOSPITAL" for d in dados_exportados if "nome" in d)
            )

    def test_falha_no_repositorio_atualiza_estado_para_erro(self):
        """Força uma quebra de persistência para validar a resiliência do uiState."""
        # CORREÇÃO: Uma função que realmente LANÇA a exceção com raise
        def simular_falha():
            raise RuntimeError("Simulação de Falha Crítica")
            
        self.repositorio.carregar_todos_os_pontos = simular_falha

        with self.assertRaises(Exception):
            self.vm.obter_dados_tabela()

        self.assertEqual(self.vm.uiState, EstadosTelaResultado.ERRO)

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
