import sqlite3

conexao = sqlite3.connect('cache.db')

cursor = conexao.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS cache (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        senha TEXT NOT NULL,
        agendamento DATETIME
    )
''')

conexao.commit()

opcao = 0

while opcao != 3:
    print("\n" + "="*30)
    print("      SEJA BEM VINDO AO HOSPITAL PUCC      ")
    print("="*30)
    print("1 - Fazer Login")
    print("2 - Cadastre-se")
    print("3 - Sair")
    print("="*30)
    opcao = int(input("Escolha uma opção: "))

    if opcao == 1:
        nome = input("Digite seu nome: ")
        senha = input("Digite sua senha: ")

        cursor.execute("SELECT * FROM cache WHERE nome = ? AND senha = ?", (nome, senha))
        resultado = cursor.fetchone()

        if resultado is not None:
            print("Login bem-sucedido! Bem-vindo, {}.".format(nome))

            opcao_2 = 0

            while opcao_2 != 3:
                print("\n" + "="*30)
                print("      SEJA BEM VINDO AO HOSPITAL PUCC, {}.   ".format(nome))
                print("="*30)
                print("1 - Agendar Consulta")
                print("2 - Verificar Consultas Agendadas")
                print("3 - Sair")
                print("="*30)
                opcao_2 = int(input("Escolha uma opção: "))

                if opcao_2 == 1:

                    data = input("Digite a data da consulta (YYYY-MM-DD): ")
                    cursor.execute("Update cache SET agendamento = ? WHERE nome = ?", (data, nome))
                    conexao.commit()
                    print("Consulta agendada para {}.".format(data))

                elif opcao_2 == 2:

                    cursor.execute("SELECT agendamento FROM cache WHERE nome = ?", (nome,))
                    resultado = cursor.fetchone()

                    if resultado is not None:
                        print("Sua consulta está agendada para {}.".format(resultado[0]))
                    else:
                        print("Você não tem consultas agendadas.")

                elif opcao_2 == 3:

                    print("Foi bom ter voce aqui {}! Volte sempre.".format(nome))

                else:
                    print("Opção inválida. Tente novamente.")

        elif opcao == 2:
            nome = input("Digite seu nome: ")
            senha = input("Digite sua senha: ")

            cursor.execute("INSERT INTO cache (nome, senha) values (?, ?)", (nome, senha))
            conexao.commit()
            print("Cadastro realizado com sucesso! Agora você pode fazer login.")
            
        else:
            print("Nome ou senha incorretos. Tente novamente.")

