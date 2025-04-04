import mysql.connector
from mysql.connector import Error
from app.config import Config
import logging

logging.basicConfig(filename='app.log', level=logging.ERROR)

class UsuarioModel:
    def conectar(self):
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

    def registrar_historico(self, tipo_acao, tabela_afetada, id_afetado):
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
            logging.error(f"Erro ao registrar histórico: {e}")
        finally:
            cursor.close()
            conn.close()

    def criar_usuario(self, nome, email, senha):
        conn = self.conectar()
        if conn is None:
            return
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO usuarios (nome, email, senha) VALUES (%s, %s, %s)",
                (nome, email, senha)
            )
            conn.commit()
            usuario_id = cursor.lastrowid
            self.registrar_historico('create', 'usuario', usuario_id)
        except Error as e:
            logging.error(f"Erro ao criar usuário: {e}")
        finally:
            cursor.close()
            conn.close()

    def atualizar_usuario(self, usuario_id, nome, email, senha):
        conn = self.conectar()
        if conn is None:
            return
        try:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE usuarios SET nome = %s, email = %s, senha = %s WHERE id = %s",
                (nome, email, senha, usuario_id)
            )
            conn.commit()
            self.registrar_historico('update', 'usuario', usuario_id)
        except Error as e:
            logging.error(f"Erro ao atualizar usuário: {e}")
        finally:
            cursor.close()
            conn.close()

    def excluir_usuario(self, usuario_id):
        conn = self.conectar()
        if conn is None:
            return
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM usuarios WHERE id = %s", (usuario_id,))
            conn.commit()
            self.registrar_historico('delete', 'usuario', usuario_id)
        except Error as e:
            logging.error(f"Erro ao excluir usuário: {e}")
        finally:
            cursor.close()
            conn.close()

    def listar_usuarios(self):
        """
        Retorna a lista de todos os usuários cadastrados no banco de dados.
        """
        conn = self.conectar()
        if conn is None:
            return []
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM usuarios")
            usuarios = cursor.fetchall()
            return usuarios
        except Error as e:
            logging.error(f"Erro ao listar usuários: {e}")
            return []
        finally:
            cursor.close()
            conn.close()

    def buscar_usuario_por_id(self, usuario_id):
        """
        Busca um usuário pelo ID no banco de dados.

        Args:
            usuario_id (int): ID do usuário a ser buscado.

        Returns:
            tuple: Dados do usuário encontrado ou None se não existir.
        """
        conn = self.conectar()
        if conn is None:
            return None
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM usuarios WHERE id = %s", (usuario_id,))
            usuario = cursor.fetchone()
            return usuario
        except Error as e:
            logging.error(f"Erro ao buscar usuário por ID: {e}")
            return None
        finally:
            cursor.close()
            conn.close()