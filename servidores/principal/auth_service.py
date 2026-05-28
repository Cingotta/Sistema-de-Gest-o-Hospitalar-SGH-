import sqlite3
from unidecode import unidecode ## para tirar acentos

conexao = sqlite3.connect('auth.db')

cursor = conexao.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL UNIQUE,
    senha TEXT NOT NULL,
    tipo_usuario TEXT NOT NULL,
    faturamento TEXT NOT NULL,
    cobrancas TEXT NOT NULL
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

        cursor.execute("SELECT * FROM users WHERE nome = ? AND senha = ?", (nome, senha,))
        resultado = cursor.fetchone()

        if resultado is not None:
            print("Seja bem-vindo {}".format(nome))
        else:
            print("Usuario nao encontrado, tente novamente.")
    elif opcao == 2:
        nome = input("Por favor, nos informe seu nome: ")
        tipo_usuario = unidecode(input("Voce é medico ou enfermeira? ")) ## tira os acentos
        senha = input("Por favor, crie uma senha: ")

        cursor.execute(
            "INSERT INTO users (nome, tipo_usuario, senha) VALUES (?, ?, ?)",
            (nome, tipo_usuario, senha)
        )
        conexao.commit()
        print("Cadastro realizado com sucesso! Agora você pode fazer login.")
