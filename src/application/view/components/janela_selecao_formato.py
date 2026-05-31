import customtkinter as ctk

class JanelaSelecaoFormato(ctk.CTkToplevel):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.title("Exportar Dados")
        self.geometry("400x180")
        self.resizable(False, False)
        
        # 1. Força a janela a ser renderizada e aparecer imediatamente
        self.deiconify()
        self.update_idletasks()
        
        # 2. Agora que ela está visível, podemos prender o foco com segurança!
        self.grab_set() 
        self.focus_set()
        
        # 3. Centraliza o modal em relação à tela principal
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (400 // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (180 // 2)
        self.geometry(f"+{x}+{y}")

        self.resultado = None

        # Rótulo de instrução
        self.lbl_mensagem = ctk.CTkLabel(
            self, 
            text="Selecione o formato desejado para a exportação:", 
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.lbl_mensagem.pack(pady=(25, 20), padx=20)

        # Container para os botões ficarem lado a lado
        self.frame_botoes = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_botoes.pack(fill="x", padx=40, pady=10)

        # Botão CSV
        self.btn_csv = ctk.CTkButton(
            self.frame_botoes, 
            text="📄 Exportar CSV", 
            fg_color="#27AE60", 
            hover_color="#219653",
            font=ctk.CTkFont(weight="bold"),
            command=lambda: self._definir_formato("csv")
        )
        self.btn_csv.pack(side="left", expand=True, padx=10)

        # Botão JSON
        self.btn_json = ctk.CTkButton(
            self.frame_botoes, 
            text="{ } Exportar JSON", 
            fg_color="#2980B9", 
            hover_color="#2471A3",
            font=ctk.CTkFont(weight="bold"),
            command=lambda: self._definir_formato("json")
        )
        self.btn_json.pack(side="right", expand=True, padx=10)

    def _definir_formato(self, formato: str) -> None:
        self.resultado = formato
        self.destroy()