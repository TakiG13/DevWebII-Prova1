import mysql.connector
from mysql.connector import Error
from app.config import Config
import logging

logging.basicConfig(filename='app.log', level=logging.ERROR)

class ProdutoModel:
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

    def criar_produto(self, nome, descricao, preco, estoque):
        conn = self.conectar()
        if conn is None:
            return
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO produtos (nome, descricao, preco, estoque) VALUES (%s, %s, %s, %s)",
                (nome, descricao, preco, estoque)
            )
            conn.commit()
            produto_id = cursor.lastrowid
            self.registrar_historico('create', 'produto', produto_id)
        except Error as e:
            logging.error(f"Erro ao criar produto: {e}")
        finally:
            cursor.close()
            conn.close()

    def excluir_produto(self, produto_id):
        conn = self.conectar()
        if conn is None:
            return
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM produtos WHERE id = %s", (produto_id,))
            conn.commit()
            self.registrar_historico('delete', 'produto', produto_id)
        except Error as e:
            logging.error(f"Erro ao excluir produto: {e}")
        finally:
            cursor.close()
            conn.close()

    def atualizar_produto(self, produto_id, nome, descricao, preco, estoque):
        conn = self.conectar()
        if conn is None:
            return
        try:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE produtos SET nome = %s, descricao = %s, preco = %s, estoque = %s WHERE id = %s",
                (nome, descricao, preco, estoque, produto_id)
            )
            conn.commit()
            self.registrar_historico('update', 'produto', produto_id)
        except Error as e:
            logging.error(f"Erro ao atualizar produto: {e}")
        finally:
            cursor.close()
            conn.close()

    def listar_produtos(self):
        """
        Retorna a lista de todos os produtos cadastrados no banco de dados.
        """
        conn = self.conectar()
        if conn is None:
            return []
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM produtos")
            produtos = cursor.fetchall()
            return produtos
        except Error as e:
            logging.error(f"Erro ao listar produtos: {e}")
            return []
        finally:
            cursor.close()
            conn.close()

    def buscar_produto_por_id(self, produto_id):
        """
        Busca um produto pelo ID no banco de dados.

        Args:
            produto_id (int): ID do produto a ser buscado.

        Returns:
            tuple: Dados do produto encontrado ou None se não existir.
        """
        conn = self.conectar()
        if conn is None:
            return None
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM produtos WHERE id = %s", (produto_id,))
            produto = cursor.fetchone()
            return produto
        except Error as e:
            logging.error(f"Erro ao buscar produto por ID: {e}")
            return None
        finally:
            cursor.close()
            conn.close()