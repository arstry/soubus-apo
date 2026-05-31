import customtkinter as ctk
from src.application.view_model import InputViewModel
from src.application.view.components.modal import exibir_modal
from src.util.excecoes import ExcecaoValidacaoSeguranca

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class TelaEntrada(ctk.CTk):
    def __init__(self, view_model: InputViewModel) -> None:
        super().__init__()

        self._view_model = view_model

        self.title("SouBus - Cadastro de Dados")
        self.geometry("800x600")
        self.minsize(700, 500)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._widgets_formulario = []
        self._tipo_selecionado = None

        self._criar_menu_lateral()
        self._criar_area_formulario()

        self.protocol("WM_DELETE_WINDOW", self._ao_fechar_janela)

    def _criar_menu_lateral(self) -> None:
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
            text="Cadastro de Dados",
            font=ctk.CTkFont(size=12, slant="italic"),
            text_color="gray"
        )
        self.lbl_subtitulo.pack(padx=20, pady=(0, 35))

        self.separador = ctk.CTkFrame(self.menu_lateral, height=2, fg_color="gray30")
        self.separador.pack(fill="x", padx=20, pady=10)

        self.btn_demanda = ctk.CTkButton(
            self.menu_lateral,
            text="Ponto de Demanda",
            font=ctk.CTkFont(weight="bold"),
            fg_color="#FF5733",
            hover_color="#E04E2D",
            command=self._exibir_formulario_demanda
        )
        self.btn_demanda.pack(padx=20, pady=10, fill="x")

        self.btn_parada = ctk.CTkButton(
            self.menu_lateral,
            text="Parada de Onibus",
            font=ctk.CTkFont(weight="bold"),
            fg_color="#2ECC71",
            hover_color="#27AE60",
            command=self._exibir_formulario_parada
        )
        self.btn_parada.pack(padx=20, pady=10, fill="x")

        self.btn_linha = ctk.CTkButton(
            self.menu_lateral,
            text="Linha de Onibus",
            font=ctk.CTkFont(weight="bold"),
            fg_color="#3498DB",
            hover_color="#2980B9",
            command=self._exibir_formulario_linha_onibus
        )
        self.btn_linha.pack(padx=20, pady=10, fill="x")

        self.separador2 = ctk.CTkFrame(self.menu_lateral, height=2, fg_color="gray30")
        self.separador2.pack(fill="x", padx=20, pady=(20, 10))

        self.lbl_status_titulo = ctk.CTkLabel(
            self.menu_lateral,
            text="Status:",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="gray"
        )
        self.lbl_status_titulo.pack(padx=20, pady=(5, 0))

        self.lbl_status = ctk.CTkLabel(
            self.menu_lateral,
            text="Aguardando...",
            font=ctk.CTkFont(size=11),
            text_color="gray",
            wraplength=220
        )
        self.lbl_status.pack(padx=20, pady=(5, 20))

    def _criar_area_formulario(self) -> None:
        self.area_formulario = ctk.CTkFrame(self, corner_radius=15)
        self.area_formulario.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        self.area_formulario.grid_columnconfigure(0, weight=1)
        self.area_formulario.grid_rowconfigure(0, weight=1)

        self.lbl_placeholder = ctk.CTkLabel(
            self.area_formulario,
            text="Selecione um tipo de cadastro\nno menu lateral",
            font=ctk.CTkFont(size=16),
            text_color="gray"
        )
        self.lbl_placeholder.grid(row=0, column=0, sticky="nsew")

    def _limpar_area_formulario(self) -> None:
        for widget in self._widgets_formulario:
            widget.destroy()
        self._widgets_formulario.clear()

        if self.lbl_placeholder.winfo_exists():
            self.lbl_placeholder.destroy()

    def _criar_campo(self, parent, rotulo: str, placeholder: str = "", tipo: str = "entry") -> ctk.CTkEntry | ctk.CTkCheckBox:
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(fill="x", padx=40, pady=5)
        self._widgets_formulario.append(frame)

        lbl = ctk.CTkLabel(frame, text=rotulo, font=ctk.CTkFont(size=13), width=140, anchor="w")
        lbl.pack(side="left", padx=(0, 10))

        if tipo == "checkbox":
            entrada = ctk.CTkCheckBox(frame, text="")
            entrada.pack(side="left")
        else:
            entrada = ctk.CTkEntry(frame, placeholder_text=placeholder)
            entrada.pack(side="left", fill="x", expand=True)

        return entrada

    def _exibir_formulario_demanda(self) -> None:
        self._limpar_area_formulario()
        self._tipo_selecionado = "demanda"

        container = ctk.CTkScrollableFrame(self.area_formulario, corner_radius=0, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=10, pady=10)
        self._widgets_formulario.append(container)

        ctk.CTkLabel(
            container,
            text="Cadastrar Ponto de Demanda",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#FF5733"
        ).pack(pady=(20, 20))

        self.entry_demanda_nome = self._criar_campo(container, "Nome do Local:", "Ex: Hospital Central")
        self.entry_demanda_lat = self._criar_campo(container, "Latitude:", "-19.917")
        self.entry_demanda_lon = self._criar_campo(container, "Longitude:", "-43.934")
        self.entry_demanda_valor = self._criar_campo(container, "Demanda:", "150")

        btn_enviar = ctk.CTkButton(
            container,
            text="Enviar Dados",
            font=ctk.CTkFont(weight="bold"),
            fg_color="#FF5733",
            hover_color="#E04E2D",
            command=lambda: self._coletar_dados_e_enviar("demanda")
        )
        btn_enviar.pack(pady=30)
        self._widgets_formulario.append(btn_enviar)

    def _exibir_formulario_parada(self) -> None:
        self._limpar_area_formulario()
        self._tipo_selecionado = "parada"

        container = ctk.CTkScrollableFrame(self.area_formulario, corner_radius=0, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=10, pady=10)
        self._widgets_formulario.append(container)

        ctk.CTkLabel(
            container,
            text="Cadastrar Parada de Onibus",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#2ECC71"
        ).pack(pady=(20, 20))

        self.entry_parada_id = self._criar_campo(container, "ID da Parada:", "42")
        self.entry_parada_lat = self._criar_campo(container, "Latitude:", "-19.920")
        self.entry_parada_lon = self._criar_campo(container, "Longitude:", "-43.940")
        self.entry_parada_linhas = self._criar_campo(container, "Linhas de Onibus:", "5102, 8103; 9104")

        self.check_parada_estado = self._criar_campo(container, "Parada Ativa:", tipo="checkbox")
        self.check_parada_estado.select()

        btn_enviar = ctk.CTkButton(
            container,
            text="Enviar Dados",
            font=ctk.CTkFont(weight="bold"),
            fg_color="#2ECC71",
            hover_color="#27AE60",
            command=lambda: self._coletar_dados_e_enviar("parada")
        )
        btn_enviar.pack(pady=30)
        self._widgets_formulario.append(btn_enviar)

    def _exibir_formulario_linha_onibus(self) -> None:
        self._limpar_area_formulario()
        self._tipo_selecionado = "linha_onibus"

        container = ctk.CTkScrollableFrame(self.area_formulario, corner_radius=0, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=10, pady=10)
        self._widgets_formulario.append(container)

        ctk.CTkLabel(
            container,
            text="Cadastrar Linha de Onibus",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#3498DB"
        ).pack(pady=(20, 20))

        self.entry_linha_nome = self._criar_campo(container, "Nome da Linha:", "Ex: Move 51")
        self.entry_linha_capacidade = self._criar_campo(container, "Capacidade:", "80")
        self.entry_linha_ids = self._criar_campo(container, "IDs das Paradas:", "10, 11, 12")

        btn_enviar = ctk.CTkButton(
            container,
            text="Enviar Dados",
            font=ctk.CTkFont(weight="bold"),
            fg_color="#3498DB",
            hover_color="#2980B9",
            command=lambda: self._coletar_dados_e_enviar("linha_onibus")
        )
        btn_enviar.pack(pady=30)
        self._widgets_formulario.append(btn_enviar)

    def _coletar_dados_e_enviar(self, tipo: str) -> None:
        try:
            if tipo == "demanda":
                dados_brutos = {
                    "nome": self.entry_demanda_nome.get().strip(),
                    "latitude": float(self.entry_demanda_lat.get().strip() or 0.0),
                    "longitude": float(self.entry_demanda_lon.get().strip() or 0.0),
                    "demanda": int(self.entry_demanda_valor.get().strip() or 0),
                }
                sucesso = self._view_model.submeter_demanda(dados_brutos)
                if sucesso:
                    self.lbl_status.configure(text="Demanda cadastrada com sucesso!", text_color="#2ECC71")
                    self._limpar_campos(tipo)

            elif tipo == "parada":
                dados_brutos = {
                    "id": int(self.entry_parada_id.get().strip() or 0),
                    "latitude": float(self.entry_parada_lat.get().strip() or 0.0),
                    "longitude": float(self.entry_parada_lon.get().strip() or 0.0),
                    "linhas_onibus": self.entry_parada_linhas.get().strip(),
                    "estado": bool(self.check_parada_estado.get()),
                }
                sucesso = self._view_model.submeter_parada(dados_brutos)
                if sucesso:
                    self.lbl_status.configure(text="Parada cadastrada com sucesso!", text_color="#2ECC71")
                    self._limpar_campos(tipo)

            elif tipo == "linha_onibus":
                ids_str = self.entry_linha_ids.get().strip()
                paradas_ids = [int(p.strip()) for p in ids_str.split(",") if p.strip().isdigit()] if ids_str else []
                dados_brutos = {
                    "nome": self.entry_linha_nome.get().strip(),
                    "capacidade": int(self.entry_linha_capacidade.get().strip() or 0),
                    "paradas_ids": paradas_ids,
                }
                sucesso = self._view_model.submeter_linha_onibus(dados_brutos)
                if sucesso:
                    self.lbl_status.configure(text="Linha de onibus cadastrada com sucesso!", text_color="#2ECC71")
                    self._limpar_campos(tipo)

        except ValueError:
            self.lbl_status.configure(text="Erro: Verifique os valores numericos.", text_color="#E74C3C")
        except ExcecaoValidacaoSeguranca as e:
            self.lbl_status.configure(text=str(e), text_color="#E74C3C")
        except Exception as e:
            exibir_modal(self, f"Ocorreu um erro inesperado:\n{str(e)}")
            self.lbl_status.configure(text="Erro inesperado ao enviar dados.", text_color="#E74C3C")

    def _limpar_campos(self, tipo: str) -> None:
        try:
            if tipo == "demanda":
                self.entry_demanda_nome.delete(0, "end")
                self.entry_demanda_lat.delete(0, "end")
                self.entry_demanda_lon.delete(0, "end")
                self.entry_demanda_valor.delete(0, "end")
            elif tipo == "parada":
                self.entry_parada_id.delete(0, "end")
                self.entry_parada_lat.delete(0, "end")
                self.entry_parada_lon.delete(0, "end")
                self.entry_parada_linhas.delete(0, "end")
                self.check_parada_estado.select()
            elif tipo == "linha_onibus":
                self.entry_linha_nome.delete(0, "end")
                self.entry_linha_capacidade.delete(0, "end")
                self.entry_linha_ids.delete(0, "end")
        except Exception:
            pass

    def _ao_fechar_janela(self) -> None:
        self.destroy()
