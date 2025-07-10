import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

# === BANCO DE DADOS ===
def conectar():
    conn = sqlite3.connect('funcionarios.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS funcionarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            cargo TEXT NOT NULL,
            salario REAL,
            setor TEXT NOT NULL,
            telefone TEXT DEFAULT '88 8888-8888',
            email TEXT,
            data_admissao DATE DEFAULT (CURRENT_DATE)
        )
    ''')
    conn.commit()
    return conn, cursor

# === FUNÇÕES DE AÇÃO ===
def carregar_dados():
    for i in tree.get_children():
        tree.delete(i)
    conn, cursor = conectar()
    cursor.execute("SELECT * FROM funcionarios")
    for linha in cursor.fetchall():
        tree.insert('', 'end', values=linha)
    conn.close()

def adicionar_funcionario():
    def salvar():
        try:
            conn, cursor = conectar()
            cursor.execute('''
                INSERT INTO funcionarios (nome, cargo, salario, setor, telefone, email, data_admissao)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                nome.get(), cargo.get(), float(salario.get()), setor.get(), telefone.get(), email.get(), data_admissao.get()
            ))
            conn.commit()
            conn.close()
            messagebox.showinfo("Sucesso", "Funcionário adicionado!")
            janela.destroy()
            carregar_dados()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    janela = tk.Toplevel()
    janela.title("Adicionar Funcionário")

    campos = ["Nome", "Cargo", "Salário", "Setor", "Telefone", "Email", "Data Admissão (YYYY-MM-DD)"]
    entradas = []

    for i, campo in enumerate(campos):
        tk.Label(janela, text=campo).grid(row=i, column=0, padx=5, pady=5)
        entry = tk.Entry(janela)
        entry.grid(row=i, column=1, padx=5, pady=5)
        entradas.append(entry)

    nome, cargo, salario, setor, telefone, email, data_admissao = entradas

    tk.Button(janela, text="Salvar", command=salvar).grid(row=len(campos), column=0, columnspan=2, pady=10)

def excluir_funcionario():
    selecionado = tree.focus()
    if not selecionado:
        messagebox.showwarning("Aviso", "Selecione um funcionário para excluir.")
        return
    id_func = tree.item(selecionado)['values'][0]

    if messagebox.askyesno("Confirmar", f"Excluir funcionário ID {id_func}?"):
        conn, cursor = conectar()
        cursor.execute("DELETE FROM funcionarios WHERE id = ?", (id_func,))
        conn.commit()
        conn.close()
        carregar_dados()
        messagebox.showinfo("Sucesso", "Funcionário excluído com sucesso!")

def atualizar_funcionario():
    selecionado = tree.focus()
    if not selecionado:
        messagebox.showwarning("Aviso", "Selecione um funcionário para editar.")
        return
    dados = tree.item(selecionado)['values']

    def salvar_edicao():
        try:
            conn, cursor = conectar()
            cursor.execute('''
                UPDATE funcionarios
                SET nome=?, cargo=?, salario=?, setor=?, telefone=?, email=?, data_admissao=?
                WHERE id=?
            ''', (
                nome.get(), cargo.get(), float(salario.get()), setor.get(),
                telefone.get(), email.get(), data_admissao.get(), dados[0]
            ))
            conn.commit()
            conn.close()
            janela.destroy()
            carregar_dados()
            messagebox.showinfo("Atualizado", "Funcionário atualizado com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    janela = tk.Toplevel()
    janela.title("Atualizar Funcionário")

    campos = ["Nome", "Cargo", "Salário", "Setor", "Telefone", "Email", "Data Admissão"]
    entradas = []

    for i, (campo, valor) in enumerate(zip(campos, dados[1:])):
        tk.Label(janela, text=campo).grid(row=i, column=0, padx=5, pady=5)
        entry = tk.Entry(janela)
        entry.insert(0, valor)
        entry.grid(row=i, column=1, padx=5, pady=5)
        entradas.append(entry)

    nome, cargo, salario, setor, telefone, email, data_admissao = entradas

    tk.Button(janela, text="Salvar Alterações", command=salvar_edicao).grid(row=len(campos), column=0, columnspan=2, pady=10)

# === INTERFACE PRINCIPAL ===
janela = tk.Tk()
janela.title("Sistema de Funcionários")
janela.geometry("950x500")

# Tabela
colunas = ["ID", "Nome", "Cargo", "Salário", "Setor", "Telefone", "Email", "Data Admissão"]
tree = ttk.Treeview(janela, columns=colunas, show='headings')

for col in colunas:
    tree.heading(col, text=col)
    tree.column(col, width=100)

tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Botões
botoes = tk.Frame(janela)
botoes.pack(pady=10)

tk.Button(botoes, text="➕ Adicionar", width=15, command=adicionar_funcionario).grid(row=0, column=0, padx=5)
tk.Button(botoes, text="✏️ Atualizar", width=15, command=atualizar_funcionario).grid(row=0, column=1, padx=5)
tk.Button(botoes, text="🗑️ Excluir", width=15, command=excluir_funcionario).grid(row=0, column=2, padx=5)
tk.Button(botoes, text="🔄 Atualizar Lista", width=15, command=carregar_dados).grid(row=0, column=3, padx=5)
tk.Button(botoes, text="❌ Sair", width=15, command=janela.quit).grid(row=0, column=4, padx=5)

carregar_dados()
janela.mainloop()