import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from database import engine, Base, session
from models import User

#Cria o banco de dados antes de executar o programa
Base.metadata.create_all(engine)


def cadastrar():
    #coleta os dados digitados pelo usuario do programa
    nome = nome_entry.get()
    email = email_entry.get()
    senha = senha_entry.get()

    #verifica se todos os campos estão preenchidos
    if nome and email and senha:
        novo_usuario = User(nome=nome,email=email,senha=senha)
        session.add(novo_usuario)
        session.commit()

        #deleta os campos digitados pelo usuário
        nome_entry.delete(0,tk.END)
        email_entry.delete(0, tk.END)
        senha_entry.delete(0, tk.END)

        #atualiza a lista dos usuarios
        listar_usuarios()
    else:
        #mensagem de erro caso o usuário deixe algum campo em branco
        messagebox.showwarning("Aviso", "Não pode haver campo em branco!")


def listar_usuarios():
    #apaga a lista com informações antigas
    lista.delete(0, tk.END)

    #Carrega as informações do banco de dados e mostra na lista
    usuarios = session.query(User).all()
    for usuario in usuarios:
        lista.insert(tk.END,f"{usuario.id} | {usuario.nome} | {usuario.email} | {usuario.senha}")

def alterar_usuario():
    selecionado = lista.curselection() # captura a seleção da linha da lista
    novo_nome = nome_entry.get()
    novo_email = email_entry.get()
    nova_senha = senha_entry.get()

    if selecionado and novo_nome and novo_email and nova_senha:
        usuario_id = int(lista.get(selecionado).split(" | ")[0])
        usuario = session.query(User).filter_by(id = usuario_id).first()
        usuario.nome = novo_nome
        usuario.email = novo_email
        usuario.senha = nova_senha
        session.commit()
        nome_entry.delete(0, tk.END)
        email_entry.delete(0, tk.END)
        senha_entry.delete(0, tk.END)
        listar_usuarios()
    else:
        messagebox.showwarning("Aviso", "Selecione um usuário e preencha todas as informações!")


def deletar_usuario():
    selecionado = lista.curselection()

    if selecionado:
        usuario_id = int(lista.get(selecionado).split(" | ")[0])
        usuario = session.query(User).filter_by(id = usuario_id).first()
        session.delete(usuario)
        session.commit()
        listar_usuarios()
    else:
        messagebox.showwarning("Aviso", "Selecione o usuário que deseja excluir.")


#cria a janela e seus componentes
janela = tk.Tk()
janela.title("CRUD Usuários")
janela.geometry("400x600")


#define os temas da janela
style = ttk.Style()
themes = ["winnative", "clam", "alt","default" ,"classic", "vista", "xpnative"]

theme_selector = ttk.Combobox(janela, values=themes, width=10)
theme_selector.pack()
theme_selector.set("default")

def mudar_tema(event):
    style.theme_use(theme_selector.get())

theme_selector.bind("<<ComboboxSelected>>", mudar_tema)



label_nome = ttk.Label(janela, text="Nome")
label_nome.pack(pady=10)

nome_entry = ttk.Entry(janela)
nome_entry.pack(pady=10)

label_email = ttk.Label(janela, text="Email")
label_email.pack()

email_entry = ttk.Entry(janela)
email_entry.pack(pady=10)

label_senha = ttk.Label(janela, text="Senha")
label_senha.pack()

senha_entry = ttk.Entry(janela, show="*")
senha_entry.pack(pady=10)

btn_adicionar = ttk.Button(janela, text="Adicionar usuario", command=cadastrar)
btn_adicionar.pack(pady=10)


lista = tk.Listbox(janela, width=50, height=15)
lista.pack()

btn_alterar = ttk.Button(janela, text="Editar usuario", command=alterar_usuario)
btn_alterar.pack(pady=10,padx=(90,0), side="left")

btn_deletar = ttk.Button(janela, text="Deletar usuario", command=deletar_usuario)
btn_deletar.pack(pady=10,padx=(0,90), side="right")

listar_usuarios()
janela.mainloop()