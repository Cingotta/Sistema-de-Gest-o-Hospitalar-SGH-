import os
import sqlite3

_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_DB = os.path.join(_DIR, '..', '..', '..', 'clientes', 'recepcao', 'cache.db')
AUTH_DB = os.path.join(_DIR, '..', '..', '..', 'funcionarios', 'principal', 'auth.db')
PATIENTES_DB = os.path.join(_DIR, '..', '..', '..', 'funcionarios', 'principal', 'patient_db.db')


def criar_tabela_prescricoes():
	

	conexao = sqlite3.connect(PATIENTES_DB)
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
	conexao.close()


def paciente_possui_doenca(paciente_id: int):

	conexao = sqlite3.connect(PATIENTES_DB)
	cursor = conexao.cursor()

	cursor.execute(
		"SELECT doenca, tipo_doenca FROM patient_db WHERE id = ?",
		(paciente_id,),
	)
	paciente = cursor.fetchone()
	conexao.close()
	return bool(paciente and paciente[0] and paciente[1])
	


def criar_prescricao(paciente_id: int, medicamento: str, dosagem: str, observacoes: str):

	if not paciente_possui_doenca(paciente_id):
		print("O paciente não possui uma doença registrada. Por favor, registre a doença antes de criar uma prescrição.")
		return

	conexao = sqlite3.connect(PATIENTES_DB)

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

	conexao.close()


