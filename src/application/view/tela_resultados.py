import customtkinter as ctk
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from src.application.view.components.janela_selecao_formato import JanelaSelecaoFormato
from src.application.view_model import ResultadoViewModel
from src.application.view.components.modal import exibir_modal

# Configurações de tema do CustomTkinter
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class TelaResultados(ctk.CTk):
    def __init__(self, view_model: ResultadoViewModel) -> None:
        super().__init__()
        
        self._view_model = view_model

        self.title("SouBus - Painel de Controle e Resultados")
        self.geometry("1200x750")
        self.minsize(900, 600)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._canvas = None

        self._criar_menu_lateral()
        self._criar_area_grafico()

        self.protocol("WM_DELETE_WINDOW", self._ao_fechar_janela)

    def _criar_menu_lateral(self) -> None:
        """Configura a barra lateral esquerda com títulos e botões de comando."""
        self.menu_lateral = ctk.CTkFrame(self, width=260, corner_radius=0)
        self.menu_lateral.grid(row=0, column=0, sticky="nsew")
        self.menu_lateral.grid_propagate(False)

        self.lbl_titulo = ctk.CTkLabel(
            self.menu_lateral, 
            text="SouBus", 
            font=ctk.CTkFont(size=22, weight="bold")
        )
        self.lbl_titulo.pack(padx=20, pady=(30, 5))

        self.lbl_subtitulo = ctk.CTkLabel(
            self.menu_lateral, 
            text="Análise de Malha Logística", 
            font=ctk.CTkFont(size=12, slant="italic"),
            text_color="gray"
        )
        self.lbl_subtitulo.pack(padx=20, pady=(0, 35))

        # Separador Visual
        self.separador = ctk.CTkFrame(self.menu_lateral, height=2, fg_color="gray30")
        self.separador.pack(fill="x", padx=20, pady=10)

        # Botão para Processar/Atualizar o Grafo
        self.btn_atualizar = ctk.CTkButton(
            self.menu_lateral, 
            text="Atualizar Grafo", 
            font=ctk.CTkFont(weight="bold"),
            command=self._ao_clicar_atualizar
        )
        self.btn_atualizar.pack(padx=20, pady=15, fill="x")

        self.btn_exportar = ctk.CTkButton(
            self.menu_lateral, 
            text="Exportar Dados", 
            font=ctk.CTkFont(weight="bold"),
            command=self._ao_clicar_exportar
        )
        self.btn_exportar.pack(padx=20, pady=15, fill="x")
        # Caixa de Texto para Informações ou Legenda
        self.txt_legenda = ctk.CTkTextbox(self.menu_lateral, height=180, activate_scrollbars=False)
        self.txt_legenda.pack(padx=20, pady=(20, 10), fill="x")
        self.txt_legenda.insert("0.0", "Legenda Operacional:\n\n"
                                       "🟠 Laranja: Ponto de Demanda\n"
                                       "🟢 Verde: Parada Ativa\n"
                                       "⚪ Cinza: Parada Inativa\n\n"
                                       "🔵 Linhas Azuis: Itinerários")
        self.txt_legenda.configure(state="disabled")

    def _criar_area_grafico(self) -> None:
        """Configura o container à direita que receberá o plot do NetworkX."""
        self.area_grafico = ctk.CTkFrame(self, corner_radius=15)
        self.area_grafico.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        
        self.area_grafico.grid_columnconfigure(0, weight=1)
        self.area_grafico.grid_rowconfigure(0, weight=1)

        # Label temporário indicando que o sistema está aguardando dados
        self.lbl_status_inicial = ctk.CTkLabel(
            self.area_grafico, 
            text="Clique em 'Atualizar Grafo' para renderizar a malha de transporte.",
            font=ctk.CTkFont(size=14)
        )
        self.lbl_status_inicial.grid(row=0, column=0, sticky="nsew")

    def _ao_clicar_atualizar(self) -> None:
        """Busca os dados mais recentes da ViewModel e atualiza o display."""
        dados_atuais = self._view_model.obter_dados_tabela()
        self.exibir_dados(dados_atuais)

    def _ao_clicar_exportar(self) -> None:
        """Abre uma janela de botões para o usuário selecionar o formato de exportação."""
        # 1. Instancia a nossa janela de botões customizada
        janela_formato = JanelaSelecaoFormato(self)
        
        # Faz o código da TelaResultados esperar até que esta janela seja fechada/destruída
        self.wait_window(janela_formato)

        # 2. Captura qual formato foi clicado pelo usuário
        formato_escolhido = janela_formato.resultado

        # Se o usuário fechou no "X" sem clicar em nenhum botão, interrompe o fluxo de forma segura
        if not formato_escolhido:
            return

        try:
            # 3. Dispara a lógica de exportação na ViewModel
            caminho_arquivo = self._view_model.processar_exportacao(
                formato=formato_escolhido, 
                filtros_linhas=None
            )

            # 4. Mostra a mensagem de sucesso limpa na tela
            mensagem_sucesso = (
                f"Dados exportados com sucesso!\n\n"
                f"Salvo em:\n{caminho_arquivo}"
            )
            exibir_modal(self, mensagem_sucesso)

        except Exception as e:
            exibir_modal(self, f"Falha ao exportar os dados:\n{str(e)}")


    def exibir_dados(self, dados) -> None:
        """Processa os dados de forma agnóstica a objetos ou dicionários e monta o grafo."""
        try:
            if not dados:
                exibir_modal(self, "Nenhum resultado encontrado para os critérios selecionados.")
                return

            # Se vier dentro de um dicionário envelopado pela ViewModel, extrai a lista
            if isinstance(dados, dict) and "paradas" not in dados:
                dados = list(dados.values())[0] if dados else []

            # Normaliza para lista se for um único objeto
            lista_elementos = dados if isinstance(dados, list) else [dados]

            if self.lbl_status_inicial.winfo_exists():
                self.lbl_status_inicial.destroy()

            if self._canvas:
                self._canvas.get_tk_widget().destroy()

            G = nx.DiGraph()
            pos = {}
            node_colors = []
            node_sizes = []
            labels = {}
            paradas_ids_detectados = []

            def extrair(obj, chaves_possiveis, padrao=None):
                if isinstance(obj, dict):
                    for c in chaves_possiveis:
                        if c in obj: return obj[c]
                else:
                    for c in chaves_possiveis:
                        if hasattr(obj, c): return getattr(obj, c)
                        if hasattr(obj, f"_{c}"): return getattr(obj, f"_{c}")
                return padrao

            for elemento in lista_elementos:
                lat = extrair(elemento, ["latitude", "lat", "y"])
                lat = extrair(elemento, ["latitude", "lat", "y"])
                lon = extrair(elemento, ["longitude", "long", "lon", "x"])

                if lat is None or lon is None:
                    continue  # Pula elementos sem coordenadas válidas

                # Tenta mapear se é um Ponto de Demanda
                valor_demanda = extrair(elemento, ["demanda", "volume", "qtd"])
                
                if valor_demanda is not None:
                    nome_no = extrair(elemento, ["nome", "descricao"], "Demanda")
                    pos[nome_no] = (float(lon), float(lat))
                    G.add_node(nome_no)
                    node_colors.append("#FF5733")  # Laranja
                    node_sizes.append(500)
                    labels[nome_no] = f"{nome_no}\n({valor_demanda})"
                
                # Caso contrário, trata como Ponto de Parada
                else:
                    id_parada = extrair(elemento, ["id", "codigo", "num"])
                    if id_parada is not None:
                        id_no = f"Parada {id_parada}"
                        pos[id_no] = (float(lon), float(lat))
                        G.add_node(id_no)
                        
                        estado = extrair(elemento, ["estado", "ativo", "status"], True)
                        cor = "#2ECC71" if estado else "#7F8C8D"  # Verde ou Cinza
                        
                        node_colors.append(cor)
                        node_sizes.append(250)
                        labels[id_no] = f"P{id_parada}"
                        paradas_ids_detectados.append(id_parada)

            # Se o grafo ainda estiver vazio, tenta plotar como dicionário puro do JSON
            if G.number_of_nodes() == 0 and isinstance(dados, dict):
                # Fallback para o caso de receber o dicionário cru tratado do JSON
                self._renderizar_fallback_dicionario(dados, G, pos, node_colors, node_sizes, labels, paradas_ids_detectados)

            # Se mesmo após o fallback continuar zerado, aciona a modal descritiva
            if G.number_of_nodes() == 0:
                exibir_modal(self, "Não foi possível extrair coordenadas válidas dos objetos recebidos.")
                return

            # Conectando as arestas das linhas de ônibus de forma sequencial (Fallback visual)
            if len(paradas_ids_detectados) > 1:
                paradas_ids_detectados.sort()
                for i in range(len(paradas_ids_detectados) - 1):
                    origem = f"Parada {paradas_ids_detectados[i]}"
                    destino = f"Parada {paradas_ids_detectados[i+1]}"
                    G.add_edge(origem, destino)

            # 4. Desenho e plotagem no Matplotlib
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.set_title("Malha Logística de Transporte", fontsize=12, fontweight="bold")
            ax.set_xlabel("Longitude")
            ax.set_ylabel("Latitude")
            ax.grid(True, linestyle="--", alpha=0.3)

            nx.draw_networkx_edges(G, pos, ax=ax, edge_color="#3498DB", width=2.5, arrowsize=16)
            nx.draw_networkx_nodes(G, pos, ax=ax, node_color=node_colors, node_size=node_sizes)
            nx.draw_networkx_labels(G, pos, labels=labels, ax=ax, font_size=8, font_weight="bold", verticalalignment="bottom")

            plt.tight_layout()

            # 5. Acoplamento no frame do CustomTkinter
            self._canvas = FigureCanvasTkAgg(fig, master=self.area_grafico)
            self._canvas.draw()
            self._canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew", padx=15, pady=15)

        except Exception as e:
            exibir_modal(self, f"Ocorreu um erro inesperado ao renderizar:\n{str(e)}")

    def _renderizar_fallback_dicionario(self, dados, G, pos, node_colors, node_sizes, labels, paradas_ids_detectados):
        """Mapeia chaves brutas de dicionário caso a estrutura seja o JSON bruto."""
        for dem in dados.get("demandas", []):
            nome = dem.get("nome", "Demanda")
            pos[nome] = (float(dem["longitude"]), float(dem["latitude"]))
            G.add_node(nome)
            node_colors.append("#FF5733")
            node_sizes.append(500)
            labels[nome] = f"{nome}\n({dem.get('demanda', 0)})"

        for parada in dados.get("paradas", []):
            pid = parada["id"]
            nome_p = f"Parada {pid}"
            pos[nome_p] = (float(parada["longitude"]), float(parada["latitude"]))
            G.add_node(nome_p)
            cor = "#2ECC71" if parada.get("estado", True) else "#7F8C8D"
            node_colors.append(cor)
            node_sizes.append(250)
            labels[nome_p] = f"P{pid}"
            paradas_ids_detectados.append(pid)
            
    def _ao_fechar_janela(self) -> None:
        self.destroy()