import customtkinter as ctk

def exibir_modal(janela_principal, mensagem):
    modal = ctk.CTkToplevel(janela_principal)

    modal.title("Aviso do Sistema")
    modal.geometry("350x160")
    modal.resizable(False, False)

    modal.transient(janela_principal)

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
        command=modal.destroy
    )
    btn_fechar.pack(pady=(0, 15))

    modal.update()  # força a janela a ser exibida

    modal.grab_set()
    modal.focus_set()