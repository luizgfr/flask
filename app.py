# instalar flask = 'pip install flask'
# conferir a versão = 'flask --version'
# rodar a aplicação = 'python app.py'

from flask import Flask, render_template #importando a classe Flask da biblioteca flask
from controllers import routes
from models.database import db, Game
import os

app = Flask(__name__, template_folder = 'views') #atribui a classe Flask a 'app', que agora possui todos seus métodos e atributos
routes.init_app(app)

# Secret para as flash messages
app.config['SECRET_KEY'] = 'thegamessecret'

# Define o tempo de duração da sessão
app.config['PERMANENT_SESSION_LIFETIME'] = 3600

# Permite ler o diretório de um determinado arquivo
dir = os.path.abspath(os.path.dirname(__file__))

# Passamos o diretório ao SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(dir, 'models/games.sqlite3')

if __name__ == '__main__':
    
    db.init_app(app=app)
    # Verifica no início da aplicação se o BD já existe. Caso contrário ele criará o BD.
    with app.test_request_context():
        db.create_all()

    app.run(host = 'localhost', port = 4000, debug = True) #modo debug serve para a aplicação ficar sempre atualizada no desenv.

