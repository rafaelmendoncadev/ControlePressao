
import sqlite3
from datetime import datetime

def conectar():
    """Conecta ao banco de dados SQLite."""
    return sqlite3.connect('controle_pressao.db')

def criar_tabela():
    """Cria a tabela de registros se ela não existir."""
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS registros (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data_hora TEXT NOT NULL,
                sistolica INTEGER NOT NULL,
                diastolica INTEGER NOT NULL,
                pulso INTEGER NOT NULL,
                glicose INTEGER
            )
        """)
        conn.commit()

def adicionar_registro(sistolica, diastolica, pulso, glicose):
    """Adiciona um novo registro de medição ao banco de dados."""
    data_hora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO registros (data_hora, sistolica, diastolica, pulso, glicose)
            VALUES (?, ?, ?, ?, ?)
        """, (data_hora, sistolica, diastolica, pulso, glicose))
        conn.commit()

def buscar_registros():
    """Busca todos os registros do banco de dados, ordenados por data."""
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, data_hora, sistolica, diastolica, pulso, glicose FROM registros ORDER BY data_hora DESC")
        return cursor.fetchall()

def deletar_registro(id):
    """Deleta um registro específico pelo seu ID."""
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM registros WHERE id = ?", (id,))
        conn.commit()

if __name__ == '__main__':
    # Cria a tabela ao executar o script diretamente
    criar_tabela()
    print("Banco de dados e tabela criados com sucesso!")
