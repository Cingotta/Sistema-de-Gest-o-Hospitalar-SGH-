import sqlite3

conexao = sqlite3.connect('patient_db.db') # crio um banco de dados

cursor = conexao.cursor() # conecto com o banco de dados
cursor.execute("PRAGMA foreign_keys = ON")

cursor.execute('''
    CREATE TABLE IF NOT EXISTS patient_db (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        senha TEXT NOT NULL,
        idade INTEGER,
        peso REAL,
        altura REAL,
        doenca BOOLEAN,
        tipo_doenca TEXT
    )
''')

conexao.commit() # crio a tabela patient_db

cursor.execute("PRAGMA table_info(patient_db)")
colunas = [coluna[1] for coluna in cursor.fetchall()]

if "tipo_doenca" not in colunas:
    cursor.execute("ALTER TABLE patient_db ADD COLUMN tipo_doenca TEXT")
    conexao.commit()


opcao = 0

while opcao != 5:
    print("\n" + "="*30)
    print("      MENU PRINCIPAL      ")
    print("="*30)
    print("1 - Cadastrar Novo Paciente")
    print("2 - Listar Cadastros")
    print("3 - Atualizar Cadastro")
    print("4 - Deletar Cadastro")
    print("5 - Sair")
    print("="*30)
    opcao = int(input("Escolha uma opção: "))

    if opcao == 1:
        nome = input("Digite o nome do paciente: ")
        senha = input("Digite a senha do paciente: ")
        idade = int(input("Digite a idade do paciente: "))
        peso = float(input("Digite o peso do paciente (kg): "))
        altura = float(input("Digite a altura do paciente (m): "))
        doenca = input("O paciente tem alguma doença? (S/N): ").upper()

        if doenca == 'S':
            doenca = True
            tipo_doenca = input("Digite o tipo da doença: ")
        else: 
            doenca = False
            tipo_doenca = None
        comando_sql = "INSERT INTO patient_db (nome, senha, idade, peso, altura, doenca, tipo_doenca) VALUES (?, ?, ?, ?, ?, ?, ?)"

        valores = (nome, senha, idade, peso, altura, doenca, tipo_doenca) # faco um tule com os valores

        cursor.execute(comando_sql, valores ) # injeto no banco de dados
        conexao.commit() # commito a trnasacao ao bano de dados
        print("Paciente cadastrado com sucesso!")

    elif opcao == 2:
        print("\nLista de Pacientes Cadastrados:")

        cursor.execute("SELECT * FROM patient_db") ## seleciono todos os pacientes cadastrados no banco de dados

        pacientes = cursor.fetchall() ## puxo os dados da db e coloco em tulas

        if len(pacientes) == 0:
            print("Nenhum paciente cadastrado.")
        else:
            for paciente in pacientes:

                id_paciente = paciente[0]
                nome_paciente = paciente[1]
                senha_paciente = paciente[2]
                idade_paciente = paciente[3]
                peso_paciente = paciente[4]
                altura_paciente = paciente[5]

                if paciente[6]: # se o paciente tiver doença
                    doenca_paciente = "Sim"
                    tipo_doenca_paciente = paciente[7]
                else:
                    doenca_paciente = "Não"
                    tipo_doenca_paciente = "N/A"

                print(f"ID: {id_paciente} | Nome: {nome_paciente} | Idade: {idade_paciente} | Peso: {peso_paciente} kg | Altura: {altura_paciente} m | Doença: {doenca_paciente} | Tipo da Doença: {tipo_doenca_paciente}")

    elif opcao == 3:
        id_paciente = int(input("Digite o ID do paciente que deseja atualizar: "))

        cursor.execute("SELECT * FROM patient_db WHERE id = ?", (id_paciente,))

        if cursor.fetchone() is None:
            print("Paciente não encontrado.")
        else:
            novo_nome = input("Digite o novo nome do paciente: ")
            nova_idade = int(input("Digite a nova idade do paciente: "))
            novo_peso = float(input("Digite o novo peso do paciente (kg): "))
            nova_altura = float(input("Digite a nova altura do paciente (m): "))
            nova_senha = input("Digite a nova senha do paciente: ")
            doenca = input("O paciente tem alguma doenca? (S/N): ").upper()

            if doenca == 'S':
                doenca = True
                tipo_doenca = input("Digite o tipo da doença: ")
            else:
                doenca = False
                tipo_doenca = None
            
            comando_sql = """
                UPDATE patient_db
                SET nome = ?, senha = ?, idade = ?, peso = ?, altura = ?, doenca = ?, tipo_doenca = ?
                WHERE id = ?
            """
            valores = (novo_nome, nova_idade, novo_peso, nova_altura, doenca, tipo_doenca, id_paciente)

            cursor.execute(comando_sql, valores)
            conexao.commit()
            print("Cadastro atualizado com sucesso!")
    elif opcao == 4:
        id_paciente = int(input("Digite o ID do paciente que deseja deletar: "))

        cursor.execute("SELECT * FROM patient_db WHERE id = ?", (id_paciente,))

        if cursor.fetchone() is None:
            print("Paciente não encontrado.")
        else:
            cursor.execute("DELETE FROM patient_db WHERE id = ?", (id_paciente,))
            conexao.commit()
            print("Cadastro deletado com sucesso!")
