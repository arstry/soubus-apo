import customtkinter as ctk 

def exibir_modal(janela_principal, mensagem):
    """Cria uma janela modal em CustomTkinter que bloqueia a janela principal."""

    modal = ctk.CTkToplevel(janela_principal)
    modal.title("Aviso do Sistema")
    modal.geometry("350x160")
    modal.resizable(False, False)

    modal.transient(janela_principal)  
    modal.grab_set()  
    modal.focus_set()  

    lbl_mensagem = ctk.CTkLabel(
        modal, 
        text=mensagem, 
        wraplength=300, 
        font=("Arial", 12)
    )
    lbl_mensagem.pack(pady=(25, 15), padx=20)

    btn_fechar = ctk.CTkButton(
        modal,
        text="Ok, Entendi",
        command=modal.destroy,
        width=110,
        fg_color="#2ECC71",       # Cor de fundo
        hover_color="#27AE60",    # Cor de quando o mouse passa por cima
        text_color="white",
        font=("Arial", 11, "bold"),
    )
    btn_fechar.pack(pady=(0, 15))