#atualização rápida de pacientes

import sqlite3
import os

_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_DB = os.path.join(_DIR, '..', '..', '..', 'clientes', 'recepcao', 'cache.db')
AUTH_DB = os.path.join(_DIR, '..', '..', '..', 'funcionarios', 'principal', 'auth.db')


def criar_tabela_patient():
    conexao = sqlite3.connect(AUTH_DB)
    cursor = conexao.cursor()

    cursor.execute("PRAGMA foreign_keys = ON")

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS patient_db (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            idade INTEGER NOT NULL,
            doenca TEXT,
            tipo_doenca TEXT
        )
        """
    )
    conexao.commit()
    conexao.close()
