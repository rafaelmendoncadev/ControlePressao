import sqlite3
import logging
from datetime import datetime
from typing import List, Optional
from pathlib import Path
import config
from models import RegistroMedicao

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseManager:
    """Gerenciador do banco de dados com melhor estrutura e tratamento de erros."""
    
    def __init__(self, db_path: str = config.DATABASE_PATH):
        self.db_path = db_path
        self._create_database_directory()
        self.criar_tabela()
    
    def _create_database_directory(self):
        """Cria o diretório do banco de dados se não existir."""
        db_dir = Path(self.db_path).parent
        db_dir.mkdir(parents=True, exist_ok=True)
    
    def conectar(self) -> sqlite3.Connection:
        """Conecta ao banco de dados SQLite com configurações otimizadas."""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.execute("PRAGMA foreign_keys = ON")  # Habilita foreign keys
            conn.execute("PRAGMA journal_mode = WAL")  # Melhor performance
            return conn
        except sqlite3.Error as e:
            logger.error(f"Erro ao conectar ao banco: {e}")
            raise
    
    def criar_tabela(self):
        """Cria a tabela de registros com índices otimizados."""
        try:
            with self.conectar() as conn:
                cursor = conn.cursor()
                
                # Criar tabela principal
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS registros (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        data_hora TEXT NOT NULL,
                        sistolica INTEGER NOT NULL CHECK (sistolica BETWEEN 70 AND 250),
                        diastolica INTEGER NOT NULL CHECK (diastolica BETWEEN 40 AND 150),
                        pulso INTEGER NOT NULL CHECK (pulso BETWEEN 30 AND 200),
                        glicose INTEGER CHECK (glicose IS NULL OR glicose BETWEEN 50 AND 500),
                        observacoes TEXT,
                        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                        updated_at TEXT DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Criar índices para melhor performance
                cursor.execute("""
                    CREATE INDEX IF NOT EXISTS idx_registros_data_hora 
                    ON registros (data_hora)
                """)
                
                cursor.execute("""
                    CREATE INDEX IF NOT EXISTS idx_registros_sistolica 
                    ON registros (sistolica)
                """)
                
                # Criar trigger para updated_at
                cursor.execute("""
                    CREATE TRIGGER IF NOT EXISTS update_timestamp 
                    AFTER UPDATE ON registros
                    BEGIN
                        UPDATE registros SET updated_at = CURRENT_TIMESTAMP 
                        WHERE id = NEW.id;
                    END
                """)
                
                conn.commit()
                logger.info("Tabela e índices criados com sucesso")
                
        except sqlite3.Error as e:
            logger.error(f"Erro ao criar tabela: {e}")
            raise
    
    def adicionar_registro(self, registro: RegistroMedicao) -> int:
        """Adiciona um novo registro ao banco de dados."""
        # Validar dados
        is_valid, message = registro.validar()
        if not is_valid:
            raise ValueError(message)
        
        try:
            with self.conectar() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO registros (data_hora, sistolica, diastolica, pulso, glicose)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    registro.data_hora.strftime('%Y-%m-%d %H:%M:%S'),
                    registro.sistolica,
                    registro.diastolica,
                    registro.pulso,
                    registro.glicose
                ))
                
                registro_id = cursor.lastrowid
                logger.info(f"Registro adicionado com ID: {registro_id}")
                return registro_id
                
        except sqlite3.Error as e:
            logger.error(f"Erro ao adicionar registro: {e}")
            raise
    
    def buscar_registros(self, limite: Optional[int] = None, 
                        data_inicio: Optional[datetime] = None,
                        data_fim: Optional[datetime] = None) -> List[RegistroMedicao]:
        """Busca registros com filtros opcionais."""
        try:
            with self.conectar() as conn:
                cursor = conn.cursor()
                
                query = """
                    SELECT id, data_hora, sistolica, diastolica, pulso, glicose 
                    FROM registros 
                    WHERE 1=1
                """
                params = []
                
                if data_inicio:
                    query += " AND data_hora >= ?"
                    params.append(data_inicio.strftime('%Y-%m-%d %H:%M:%S'))
                
                if data_fim:
                    query += " AND data_hora <= ?"
                    params.append(data_fim.strftime('%Y-%m-%d %H:%M:%S'))
                
                query += " ORDER BY data_hora DESC"
                
                if limite:
                    query += " LIMIT ?"
                    params.append(limite)
                
                cursor.execute(query, params)
                resultados = cursor.fetchall()
                
                return [RegistroMedicao.from_tuple(row) for row in resultados]
                
        except sqlite3.Error as e:
            logger.error(f"Erro ao buscar registros: {e}")
            raise
    
    def deletar_registro(self, registro_id: int) -> bool:
        """Deleta um registro específico pelo ID."""
        try:
            with self.conectar() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM registros WHERE id = ?", (registro_id,))
                
                if cursor.rowcount > 0:
                    logger.info(f"Registro {registro_id} deletado com sucesso")
                    return True
                else:
                    logger.warning(f"Nenhum registro encontrado com ID: {registro_id}")
                    return False
                    
        except sqlite3.Error as e:
            logger.error(f"Erro ao deletar registro: {e}")
            raise
    
    def atualizar_registro(self, registro: RegistroMedicao) -> bool:
        """Atualiza um registro existente."""
        if not registro.id:
            raise ValueError("ID do registro é obrigatório para atualização")
        
        # Validar dados
        is_valid, message = registro.validar()
        if not is_valid:
            raise ValueError(message)
        
        try:
            with self.conectar() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE registros 
                    SET sistolica = ?, diastolica = ?, pulso = ?, glicose = ?
                    WHERE id = ?
                """, (
                    registro.sistolica,
                    registro.diastolica,
                    registro.pulso,
                    registro.glicose,
                    registro.id
                ))
                
                if cursor.rowcount > 0:
                    logger.info(f"Registro {registro.id} atualizado com sucesso")
                    return True
                else:
                    logger.warning(f"Nenhum registro encontrado com ID: {registro.id}")
                    return False
                    
        except sqlite3.Error as e:
            logger.error(f"Erro ao atualizar registro: {e}")
            raise
    
    def obter_estatisticas(self) -> dict:
        """Retorna estatísticas dos registros."""
        try:
            with self.conectar() as conn:
                cursor = conn.cursor()
                
                # Estatísticas gerais
                cursor.execute("""
                    SELECT 
                        COUNT(*) as total,
                        AVG(sistolica) as media_sistolica,
                        AVG(diastolica) as media_diastolica,
                        AVG(pulso) as media_pulso,
                        AVG(glicose) as media_glicose,
                        MIN(data_hora) as primeiro_registro,
                        MAX(data_hora) as ultimo_registro
                    FROM registros
                """)
                
                stats = cursor.fetchone()
                
                return {
                    'total_registros': stats[0] or 0,
                    'media_sistolica': round(stats[1], 1) if stats[1] else 0,
                    'media_diastolica': round(stats[2], 1) if stats[2] else 0,
                    'media_pulso': round(stats[3], 1) if stats[3] else 0,
                    'media_glicose': round(stats[4], 1) if stats[4] else 0,
                    'primeiro_registro': stats[5],
                    'ultimo_registro': stats[6]
                }
                
        except sqlite3.Error as e:
            logger.error(f"Erro ao obter estatísticas: {e}")
            raise

# Instância global do gerenciador
db_manager = DatabaseManager()

# Funções de compatibilidade com o código existente
def criar_tabela():
    """Função de compatibilidade."""
    db_manager.criar_tabela()

def adicionar_registro(sistolica: int, diastolica: int, pulso: int, glicose: Optional[int] = None):
    """Função de compatibilidade."""
    registro = RegistroMedicao(
        sistolica=sistolica,
        diastolica=diastolica,
        pulso=pulso,
        glicose=glicose
    )
    return db_manager.adicionar_registro(registro)

def buscar_registros():
    """Função de compatibilidade."""
    registros = db_manager.buscar_registros()
    return [(r.id, r.data_hora.strftime('%Y-%m-%d %H:%M:%S'), r.sistolica, r.diastolica, r.pulso, r.glicose) 
            for r in registros]

def deletar_registro(registro_id: int):
    """Função de compatibilidade."""
    return db_manager.deletar_registro(registro_id)

if __name__ == '__main__':
    # Testes básicos
    db_manager.criar_tabela()
    print("✅ Banco de dados inicializado com sucesso!")
    
    # Exibir estatísticas
    stats = db_manager.obter_estatisticas()
    print(f"📊 Estatísticas: {stats}")
