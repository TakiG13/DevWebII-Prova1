from flask import Flask, render_template
from app.controllers.produto_controller import produto_blueprint
from app.controllers.usuario_controller import usuario_blueprint

app = Flask(__name__)

# Registro dos blueprints
app.register_blueprint(produto_blueprint, url_prefix='/produto')
app.register_blueprint(usuario_blueprint, url_prefix='/usuario')

@app.route('/')
def index():
    """
    Página inicial do sistema.
    """
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')