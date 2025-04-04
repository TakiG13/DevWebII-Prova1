from app.models.usuario_model import UsuarioModel
from flask import Blueprint, render_template, redirect, url_for, request

# Classe para lógica de negócios de usuários
class UsuarioController:
    def __init__(self, usuario_model):
        self.usuario_model = usuario_model

    def listar_usuarios(self):
        """
        Retorna a lista de todos os usuários.
        """
        return self.usuario_model.listar_usuarios()

    def excluir_usuario(self, usuario_id):
        """
        Exclui um usuário pelo ID.
        """
        return self.usuario_model.excluir_usuario(usuario_id)

    def criar_usuario(self, nome, email, senha):
        """
        Cria um novo usuário.
        """
        return self.usuario_model.criar_usuario(nome, email, senha)

    def atualizar_usuario(self, usuario_id, nome, email, senha):
        """
        Atualiza os dados de um usuário.
        """
        return self.usuario_model.atualizar_usuario(usuario_id, nome, email, senha)


# Blueprint para rotas relacionadas a usuários
usuario_blueprint = Blueprint('usuario', __name__)
usuario_controller = UsuarioController(UsuarioModel())

# Rotas para gerenciamento de usuários
@usuario_blueprint.route('/lista_usuarios', methods=['GET'])
def lista_usuarios():
    """
    Exibe a lista de todos os usuários cadastrados ou busca um usuário específico pelo ID.
    """
    try:
        usuario_id = request.args.get('usuario_id')  # Obtém o ID do usuário da query string
        if usuario_id:
            usuario = usuario_controller.usuario_model.buscar_usuario_por_id(usuario_id)
            if usuario:
                usuarios = [usuario]  # Retorna apenas o usuário encontrado
            else:
                usuarios = []  # Nenhum usuário encontrado
        else:
            usuarios = usuario_controller.listar_usuarios()  # Retorna todos os usuários
        return render_template('lista_usuarios.html', usuarios=usuarios)
    except Exception as e:
        print(f"Erro ao listar usuários: {e}")
        return "Erro ao listar os usuários.", 500

@usuario_blueprint.route('/excluir/<int:usuario_id>', methods=['POST'])
def excluir_usuario(usuario_id):
    """
    Exclui um usuário do banco de dados.
    """
    try:
        usuario_controller.excluir_usuario(usuario_id)
        return redirect(url_for('usuario.lista_usuarios'))
    except Exception as e:
        print(f"Erro ao excluir usuário: {e}")
        return "Erro ao excluir o usuário.", 500

@usuario_blueprint.route('/criar', methods=['GET', 'POST'])
def criar_usuario():
    """
    Exibe o formulário para criar um novo usuário e processa o cadastro.
    """
    if request.method == 'POST':
        try:
            nome = request.form['nome']
            email = request.form['email']
            senha = request.form['senha']
            usuario_controller.criar_usuario(nome, email, senha)
            return redirect(url_for('usuario.lista_usuarios'))
        except Exception as e:
            print(f"Erro ao criar usuário: {e}")
            return "Erro ao criar o usuário.", 500
    return render_template('cadastro_usuario.html')

@usuario_blueprint.route('/atualizar/<int:usuario_id>', methods=['POST'])
def atualizar_usuario(usuario_id):
    """
    Atualiza os dados de um usuário no banco de dados.
    """
    try:
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        usuario_controller.atualizar_usuario(usuario_id, nome, email, senha)
        return redirect(url_for('usuario.lista_usuarios'))
    except Exception as e:
        print(f"Erro ao atualizar usuário: {e}")
        return "Erro ao atualizar o usuário.", 500