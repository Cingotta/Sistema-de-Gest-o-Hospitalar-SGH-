import os
import sqlite3
from datetime import datetime #para horarios de login, cadastro

_DIR = os.path.dirname(os.path.abspath(__file__))
PATIENT_DB = os.path.join(_DIR, '..', '..', 'funcionarios', 'principal', 'patient_db.db')
CACHE_DB = os.path.join(_DIR, 'cache.db')

# Conexão principal para pacientes e agendamentos
conexao = sqlite3.connect(PATIENT_DB)
cursor = conexao.cursor()
cursor.execute("PRAGMA foreign_keys = ON")

# Garante que a tabela patient_db exista
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

# Garante que a tabela de agendamentos 
cursor.execute('''
    CREATE TABLE IF NOT EXISTS agendamentos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        paciente_id INTEGER NOT NULL,
        data_consulta DATETIME NOT NULL,
        FOREIGN KEY (paciente_id) REFERENCES patient_db(id)
    )
''')
conexao.commit()

#agenda logs recepcao
conexao_logs = sqlite3.connect(CACHE_DB)
cursor_logs = conexao_logs.cursor()
cursor_logs.execute('''
    CREATE TABLE IF NOT EXISTS historico_acessos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome_paciente TEXT NOT NULL,
        acao TEXT NOT NULL,
        horario DATETIME NOT NULL
    )
''')
conexao_logs.commit()

def registrar_log(nome, acao):
    """Guarda a informação de quando o paciente fez cadastro ou login"""
    horario_atual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor_logs.execute("INSERT INTO historico_acessos (nome_paciente, acao, horario) VALUES (?, ?, ?)", (nome, acao, horario_atual))
    conexao_logs.commit()


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

        cursor.execute("SELECT id, nome FROM patient_db WHERE nome = ? AND senha = ?", (nome, senha))
        resultado = cursor.fetchone()

        if resultado is not None:
            paciente_id = resultado[0]
            nome_paciente = resultado[1]
            print(f"Login bem-sucedido! Bem-vindo, {nome_paciente}.")
            
            # Registrar que o paciente fez o login
            registrar_log(nome_paciente, "LOGIN")

            opcao_2 = 0
            while opcao_2 != 3:
                print("\n" + "="*30)
                print(f"      PAINEL DO PACIENTE: {nome_paciente}   ")
                print("="*30)
                print("1 - Agendar Consulta")
                print("2 - Verificar Consultas Agendadas")
                print("3 - Sair")
                print("="*30)
                opcao_2 = int(input("Escolha uma opção: "))

                if opcao_2 == 1:
                    data = input("Digite a data da consulta (YYYY-MM-DD HH:MM): ")
                    cursor.execute("INSERT INTO agendamentos (paciente_id, data_consulta) VALUES (?, ?)", (paciente_id, data))
                    conexao.commit()
                    print(f"Consulta agendada para {data}.")

                elif opcao_2 == 2:
                    cursor.execute("SELECT data_consulta FROM agendamentos WHERE paciente_id = ? ORDER BY data_consulta", (paciente_id,))
                    consultas = cursor.fetchall()

                    if consultas:
                        print("\nSuas consultas agendadas:")
                        for consulta in consultas:
                            print(f"- {consulta[0]}")
                    else:
                        print("Você não tem consultas agendadas.")

                elif opcao_2 == 3:
                    print(f"Foi bom ter você aqui {nome_paciente}! Volte sempre.")

                else:
                    print("Opção inválida. Tente novamente.")
        else:
            print("Nome ou senha incorretos. Tente novamente.")

    elif opcao == 2:
        nome = input("Digite seu nome: ")
        senha = input("Digite sua senha: ")
        idade = int(input("Digite sua idade: "))
        peso = float(input("Digite seu peso (kg): "))
        altura = float(input("Digite sua altura (m): "))
        
        # Insere todos os dados doenca, essa eh parte dpo medico
        cursor.execute('''
            INSERT INTO patient_db (nome, senha, idade, peso, altura)
            VALUES (?, ?, ?, ?, ?)
        ''', (nome, senha, idade, peso, altura))
        conexao.commit()
        print("Cadastro realizado com sucesso! Agora você pode fazer login.")
        
        # novo cadastro no cache
        registrar_log(nome, "CADASTRO NOVO")
            
    elif opcao == 3:
        print("Encerrando o sistema da recepção...")
    else:
        print("Opção inválida. Tente novamente.")