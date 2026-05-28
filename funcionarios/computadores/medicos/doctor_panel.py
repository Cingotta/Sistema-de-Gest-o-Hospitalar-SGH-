import os
import sqlite3

_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_DB = os.path.join(_DIR, '..', '..', 'computadores', 'recepcao', 'cache.db')
AUTH_DB = os.path.join(_DIR, '..', 'recepcao', 'auth.db')
PATIENTES_DB = os.path.join(_DIR, '..', '..', 'servidores', 'principal', 'patient_db.db')


def criar_tabela_prescricoes() -> None:
	"""Cria a tabela de prescrições no banco de pacientes.

	A tabela fica ligada ao paciente por chave estrangeira e guarda o tipo
	de doença como dependência do registro do paciente.
	"""

	conexao = sqlite3.connect(PATIENTES_DB)
	try:
		cursor = conexao.cursor()
		cursor.execute("PRAGMA foreign_keys = ON")
		cursor.execute(
			"""
			CREATE TABLE IF NOT EXISTS prescricoes (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				paciente_id INTEGER NOT NULL,
				tipo_doenca TEXT NOT NULL,
				medicamento TEXT NOT NULL,
				dosagem TEXT NOT NULL,
				observacoes TEXT,
				data_criacao TEXT DEFAULT CURRENT_TIMESTAMP,
				FOREIGN KEY (paciente_id) REFERENCES patient_db(id)
			)
			"""
		)
		conexao.commit()
	finally:
		conexao.close()


def paciente_possui_doenca(paciente_id: int) -> bool:
	"""Verifica se o paciente existe e possui doença cadastrada."""

	conexao = sqlite3.connect(PATIENTES_DB)
	try:
		cursor = conexao.cursor()
		cursor.execute(
			"SELECT doenca, tipo_doenca FROM patient_db WHERE id = ?",
			(paciente_id,),
		)
		paciente = cursor.fetchone()
		return bool(paciente and paciente[0] and paciente[1])
	finally:
		conexao.close()


def criar_prescricao(paciente_id: int, medicamento: str, dosagem: str, observacoes: str | None = None) -> None:
	"""Insere uma prescrição vinculada a um paciente com doença cadastrada."""

	if not paciente_possui_doenca(paciente_id):
		raise ValueError("O paciente precisa ter uma doença cadastrada para receber uma prescrição.")

	conexao = sqlite3.connect(PATIENTES_DB)
	try:
		cursor = conexao.cursor()
		cursor.execute("SELECT tipo_doenca FROM patient_db WHERE id = ?", (paciente_id,))
		tipo_doenca = cursor.fetchone()[0]
		cursor.execute(
			"""
			INSERT INTO prescricoes (paciente_id, tipo_doenca, medicamento, dosagem, observacoes)
			VALUES (?, ?, ?, ?, ?)
			""",
			(paciente_id, tipo_doenca, medicamento, dosagem, observacoes),
		)
		conexao.commit()
	finally:
		conexao.close()


