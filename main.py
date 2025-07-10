import sqlite3

# Função para conectar e criar a tabela
def conectar():
    conn = sqlite3.connect('funcionarios.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS funcionarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome VARCHAR(100) NOT NULL,
            cargo VARCHAR(100) NOT NULL,
            salario FLOAT,
            setor VARCHAR(100) NOT NULL,
            telefone VARCHAR(15) DEFAULT '88 8888-8888',
            email VARCHAR(100),
            data_admissao DATE DEFAULT (CURRENT_DATE)
        )
    ''')
    conn.commit()
    return conn, cursor

# Função para adicionar funcionário
def novo_funcionario(conn, cursor):
    nome = input('Digite seu nome: ')
    cargo = input('Digite seu cargo: ')
    salario = float(input('Digite seu salário: '))
    setor = input('Digite o seu setor: ')
    telefone = input('Digite o seu telefone: ')
    email = input('Digite seu email: ')
    
    cursor.execute('''
        INSERT INTO funcionarios (nome, cargo, salario, setor, telefone, email)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (nome, cargo, salario, setor, telefone, email))
    
    conn.commit()
    print(f"\nFuncionário '{nome}' adicionado com sucesso!\n")

# Função para listar funcionários
def listar_funcionarios(conn,cursor):
    import pandas as pd
    cursor.execute('SELECT * FROM funcionarios')
    columns = ['    id','        nome', '         cargo', '         salario', '         setor', '        telefone', '         email','         data de admissao ']
    funcionarios = pd.DataFrame(cursor,columns=columns)
    print('\n--- LISTA DE FUNCIONÁRIOS ---')
    print (funcionarios)
    print('-----------------------------\n')

# Função para Atualizar dados de um funcionario
def atualizar_funcionario(conn, cursor):
    listar_funcionarios(conn, cursor) 

    try:
        id_func = int(input("Digite o id do funcionario que deseja atualizar: "))
        
        cursor.execute("SELECT id FROM funcionarios WHERE id = ?", (id_func,))
        if cursor.fetchone() is None:
            print(f"Funcionário com ID {id_func} não encontrado.")
            return

        while True:
            print('\n--- Opções de Atualização ---\n')
            print('1 - Nome')
            print('2 - Cargo')
            print('3 - Salário')
            print('4 - Setor')
            print('5 - Telefone')
            print('6 - Email')
            print('7 - Data de Admissão')
            print('8 - TUDO (Atualizar todos os campos)')
            print('9 - Voltar ao menu principal')
            opcao = input('\nO que você deseja alterar? ')
            
            if opcao == '1':
                novo_nome = input('Digite o novo nome: ')
                cursor.execute("UPDATE funcionarios SET nome = ? WHERE id = ?", (novo_nome, id_func))
                print('Nome alterado com sucesso!')
            elif opcao == '2':
                novo_cargo = input('Digite o novo cargo: ')
                cursor.execute("UPDATE funcionarios SET cargo = ? WHERE id = ?", (novo_cargo, id_func))
                print('Cargo alterado com sucesso!')
            elif opcao == '3':
                while True:
                    try:
                        novo_salario = float(input('Digite o novo salário: '))
                        if novo_salario <= 0:
                            print("O salário deve ser um valor positivo. Tente novamente.")
                        else:
                            cursor.execute("UPDATE funcionarios SET salario = ? WHERE id = ?", (novo_salario, id_func))
                            print('Salário alterado com sucesso!')
                            break
                    except ValueError:
                        print("Entrada inválida. Por favor, digite um número para o salário.")
            elif opcao == '4':
                novo_setor = input('Digite o novo setor: ')
                cursor.execute("UPDATE funcionarios SET setor = ? WHERE id = ?", (novo_setor, id_func))
                print('Setor alterado com sucesso!')
            elif opcao == '5':
                novo_telefone = input('Digite o novo telefone: ')
                cursor.execute("UPDATE funcionarios SET telefone = ? WHERE id = ?", (novo_telefone, id_func))
                print('Telefone alterado com sucesso!')
            elif opcao == '6':
                novo_email = input('Digite o novo email: ')
                cursor.execute("UPDATE funcionarios SET email = ? WHERE id = ?", (novo_email, id_func))
                print('Email alterado com sucesso!')
            elif opcao == '7':
                novo_data_admissao = input('Digite a nova data de admissão (YYYY-MM-DD): ')
                
                cursor.execute("UPDATE funcionarios SET data_admissao = ? WHERE id = ?", (novo_data_admissao, id_func))
                print('Data de admissão alterada com sucesso!')
            elif opcao == '8':
                
                novo_nome = input('Digite o novo nome: ')
                novo_cargo = input('Digite o novo cargo: ')
                
                while True:
                    try:
                        novo_salario = float(input('Digite o novo salário: '))
                        if novo_salario <= 0:
                            print("O salário deve ser um valor positivo. Tente novamente.")
                        else:
                            break
                    except ValueError:
                        print("Entrada inválida. Por favor, digite um número para o salário.")

                novo_setor = input('Digite o novo setor: ')
                novo_telefone = input('Digite o novo telefone: ')
                novo_email = input('Digite o novo email: ')
                novo_data_admissao = input('Digite a nova data de admissão (YYYY-MM-DD): ') 

                cursor.execute("""
                    UPDATE funcionarios 
                    SET nome = ?, cargo = ?, salario = ?, setor = ?, telefone = ?, email = ?, data_admissao = ? 
                    WHERE id = ?
                """, (novo_nome, novo_cargo, novo_salario, novo_setor, novo_telefone, novo_email, novo_data_admissao, id_func))
                print('Todos os dados do funcionário foram alterados com sucesso!')
            elif opcao == '9':
                menu()
                break
            else:
                print('Opção inválida. Por favor, escolha uma opção de 1 a 9.')
            
            conn.commit()

    except ValueError:
        print("Entrada inválida. Por favor, digite um número para o ID do funcionário.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        
        conn.rollback()

# Função para excluir um funcionário
def excluir_funcionario(conn, cursor):
    listar_funcionarios(conn, cursor)
    
    try:
        id_func = input('Digite o ID do funcionário que deseja excluir: ')
    
        cursor.execute('DELETE FROM funcionarios WHERE id = ?', (id_func,))
        conn.commit()
        if cursor.rowcount == 0:
            print("Funcionario não encontrado")
        else:
            print(f"Funcionário com ID {id_func} excluído com sucesso!")
    except ValueError:
        print("Id invalido")
# Menu principal
def menu():
    conn, cursor = conectar()
    while True:
        print('MENU')
        print('1 - Adicionar funcionário')
        print('2 - Listar funcionários')
        print('3 - Atualizar funcionario')
        print('4 - Excluir funcionário')
        print('5 - Sair')
        opcao = input('Escolha uma opção: ')

        if opcao == '1':
            novo_funcionario(conn, cursor)
        elif opcao == '2':
            listar_funcionarios(conn, cursor)
        elif opcao == '3':
            atualizar_funcionario(conn, cursor)
        elif opcao == '4':
            excluir_funcionario(conn, cursor)
        elif opcao == '5':
            print('Saindo...')
            break
        else:
            print('Opção inválida. Tente novamente.\n')

    conn.close()

# Executar menu
if __name__ == "__main__":
    menu()