from app.models.produto_model import ProdutoModel
from app.historico_model import HistoricoModel  # Importar HistoricoModel
from flask import Blueprint, redirect, url_for, render_template, request

# Blueprint para rotas relacionadas a produtos
produto_blueprint = Blueprint('produto', __name__)
produto_model = ProdutoModel()
historico_model = HistoricoModel()  # Criar uma instância de HistoricoModel

# Rota para listar produtos
@produto_blueprint.route('/lista', methods=['GET'])
def lista_produtos():
    """
    Exibe a lista de produtos cadastrados ou busca um produto específico pelo ID.
    """
    try:
        produto_id = request.args.get('produto_id')  # Obtém o ID do produto da query string
        if produto_id:
            produto = produto_model.buscar_produto_por_id(produto_id)
            if produto:
                produtos = [produto]  # Retorna apenas o produto encontrado
            else:
                produtos = []  # Nenhum produto encontrado
        else:
            produtos = produto_model.listar_produtos()  # Retorna todos os produtos
        return render_template('lista_produtos.html', produtos=produtos)
    except Exception as e:
        print(f"Erro ao listar produtos: {e}")
        return "Erro ao listar os produtos.", 500

# Rota para cadastrar um novo produto
@produto_blueprint.route('/cadastro', methods=['GET', 'POST'])
def cadastro_produto():
    """
    Exibe o formulário para cadastrar um novo produto e processa o cadastro.
    """
    if request.method == 'POST':
        try:
            nome = request.form['nome']
            descricao = request.form['descricao']
            preco = request.form['preco']
            estoque = request.form['estoque']
            produto_model.criar_produto(nome, descricao, preco, estoque)
            return redirect(url_for('produto.lista_produtos'))
        except Exception as e:
            print(f"Erro ao cadastrar produto: {e}")
            return "Erro ao cadastrar o produto.", 500
    return render_template('cadastro_produto.html')

# Rota para excluir um produto
@produto_blueprint.route('/excluir/<int:produto_id>', methods=['POST'])
def excluir_produto(produto_id):
    """
    Exclui um produto do banco de dados e redireciona para a lista de produtos.
    """
    try:
        produto_model.excluir_produto(produto_id)
        return redirect(url_for('produto.lista_produtos'))
    except Exception as e:
        print(f"Erro ao excluir produto: {e}")
        return "Erro ao excluir o produto.", 500

# Rota para exibir o formulário de edição de um produto
@produto_blueprint.route('/editar/<int:produto_id>', methods=['GET'])
def editar_produto(produto_id):
    """
    Exibe o formulário de edição de um produto.
    """
    try:
        produto = produto_model.buscar_produto_por_id(produto_id)
        return render_template('editar_produto.html', produto=produto)
    except Exception as e:
        print(f"Erro ao carregar produto para edição: {e}")
        return "Erro ao carregar o produto.", 500

# Rota para atualizar os dados de um produto
@produto_blueprint.route('/atualizar/<int:produto_id>', methods=['POST'])
def atualizar_produto(produto_id):
    """
    Atualiza os dados de um produto no banco de dados.
    """
    try:
        nome = request.form['nome']
        descricao = request.form['descricao']
        preco = request.form['preco']
        estoque = request.form['estoque']
        produto_model.atualizar_produto(produto_id, nome, descricao, preco, estoque)
        return redirect(url_for('produto.lista_produtos'))
    except Exception as e:
        print(f"Erro ao atualizar produto: {e}")
        return "Erro ao atualizar o produto.", 500

# Rota para exibir o histórico de alterações realizadas nos produtos
@produto_blueprint.route('/historico', methods=['GET'])
def historico():
    """
    Exibe o histórico de alterações realizadas nos produtos.
    """
    try:
        historico = historico_model.listar_historico()  # Use historico_model aqui
        return render_template('historico.html', historico=historico)
    except Exception as e:
        print(f"Erro ao carregar histórico: {e}")
        return "Erro ao carregar o histórico.", 500