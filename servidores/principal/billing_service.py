import sqlite3

def criar_tabela_cobrancas():
    conexao = sqlite3.connect('cache.db')
    cursor = conexao.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cobrancas (
            id integer primary key autoincrement,
            usuario_id integer not null,
            descricao text not null,
            valor real not null,
            status text not null default 'pendente',
            foreign key (usuario_id) references cache(id)
        )
    ''')
    
    conexao.commit()
    conexao.close()

def criar_cobranca(usuario_id, descricao, valor):
    conexao = sqlite3.connect('cache.db')
    cursor = conexao.cursor()

    cursor.execute(
        "insert into cobrancas (usuario_id, descricao, valor) VALUES (?, ?, ?)",
        (usuario_id, descricao, valor)
    )

    conexao.commit()
    conexao.close()

def listar_cobrancas(usuario_id):
    conexao = sqlite3.connect('cache.db')
    cursor = conexao.cursor()

    cursor.execute(
        "select descricao, valor, status from cobrancas where usuario_id = ?",
        (usuario_id,)
    )

    cobrancas = cursor.fetchall()
    conexao.close()

    return cobrancas

def criar_tabela_faturamento():
    conexao = sqlite3.connect('auth.db')
    cursor = conexao.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS faturamento (
            id integer primary key autoincrement,
            usuario_id integer not null,
            descricao text not null,
            valor real not null,
            status text not null,
            foreign key (usuario_id) references users(id)
        )
    ''')

    conexao.commit()
    conexao.close()

def criar_faturamento(usuario_id, descricao, valor, status):
    conexao = sqlite3.connect('auth.db')
    cursor = conexao.cursor()

    cursor.execute(
        "insert into faturamento (usuario_id, descricao, valor, status) values (?, ?, ?, ?)",
        (usuario_id, descricao, valor, status)
    )

    conexao.commit()
    conexao.close()

def listar_faturamento(usuario_id):
    conexao = sqlite3.connect('auth.db')
    cursor = conexao.cursor()

    cursor.execute(
        "select descricao, valor, status from faturamento where usuario_id = ?",
        (usuario_id,)
    )

    cobrancas = cursor.fetchall()
    conexao.close()

    return cobrancas