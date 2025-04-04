import mysql.connector
from mysql.connector import Error
from app.config import Config
import logging

logging.basicConfig(filename='app.log', level=logging.ERROR)

class HistoricoModel:
    def conectar(self):
        """
        Estabelece uma conexão com o banco de dados.

        Returns:
            conn: Objeto de conexão com o banco de dados ou None em caso de erro.
        """
        try:
            conn = mysql.connector.connect(
                host=Config.MYSQL_HOST,
                user=Config.MYSQL_USER,
                password=Config.MYSQL_PASSWORD,
                database=Config.MYSQL_DB
            )
            return conn
        except Error as e:
            logging.error(f"Erro ao conectar ao MySQL: {e}")
            return None

    def registrar_acao(self, tipo_acao, tabela_afetada, id_afetado):
        """
        Registra uma ação no histórico.

        Args:
            tipo_acao (str): Tipo da ação ('create', 'update', 'delete').
            tabela_afetada (str): Nome da tabela afetada ('produto', 'usuario').
            id_afetado (int): ID do registro afetado.
        """
        conn = self.conectar()
        if conn is None:
            return
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO historico (tipo_acao, tabela_afetada, id_afetado) VALUES (%s, %s, %s)",
                (tipo_acao, tabela_afetada, id_afetado)
            )
            conn.commit()
        except Error as e:
            logging.error(f"Erro ao registrar ação no histórico: {e}")
        finally:
            cursor.close()
            conn.close()

    def listar_historico(self):
        """
        Retorna o histórico de ações registradas no banco de dados.

        Returns:
            list: Uma lista de tuplas contendo os registros do histórico.
        """
        conn = self.conectar()
        if conn is None:
            print("Conexão com o banco de dados falhou.")  # Adicione esta linha
            return []
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM historico ORDER BY data DESC")
            historico = cursor.fetchall()
            print(f"Dados retornados: {historico}")  # Adicione esta linha
            return historico
        except Error as e:
            logging.error(f"Erro ao listar histórico: {e}")
            print(f"Erro ao listar histórico: {e}")  # Adicione esta linha
            return []
        finally:
            cursor.close()
            conn.close()