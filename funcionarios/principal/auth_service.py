import sqlite3
import os
import sys
from unidecode import unidecode ## para tirar acentos

_DIR = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.abspath(os.path.join(_DIR, '..', '..'))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

conexao = sqlite3.connect(os.path.join(_DIR, 'auth.db'))
cursor = conexao.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    tipo_usuario TEXT NOT NULL
)''')

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

        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (nome, senha,))
        resultado = cursor.fetchone()

        if resultado is not None: # !!!!           
            ##aqui não faz sentido que os medicos e enfermeiros sejam redirecionados para a tela de cobrança
            from clientes.billing_service import criar_tabela_cobrancas, criar_cobranca, listar_cobrancas

            usuario_id = resultado[0]

            print(f"Seja bem-vindo {nome}")

            criar_tabela_cobrancas()
            criar_cobranca(usuario_id, "Consulta medica", 150.0)

            cobrancas = listar_cobrancas(usuario_id)

            for cobranca in cobrancas:
                print(f"Descrição: {cobranca[0]} | Valor: R$ {cobranca[1]} | Status: {cobranca[2]}")
        else:
            print("Usuario nao encontrado, tente novamente.")
    elif opcao == 2:
        nome = input("Por favor, nos informe seu nome: ")
        tipo_usuario = unidecode(input("Voce é medico ou enfermeira? ")) ## tira os acentos
        senha = input("Por favor, crie uma senha: ")
        try:
            cursor.execute(
                "INSERT INTO users (username, tipo_usuario, password) VALUES (?, ?, ?)",
                (nome, tipo_usuario, senha)
            )
            conexao.commit()
            print("Cadastro realizado com sucesso! Agora você pode fazer login.")
        except sqlite3.IntegrityError:
            print("Erro: O nome de usuário já existe. Por favor, escolha outro nome.")
