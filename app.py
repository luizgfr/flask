# instalar flask = 'pip install flask'
# conferir a versão = 'flask --version'
# rodar a aplicação = 'python app.py'

from flask import Flask, render_template #importando a classe Flask da biblioteca flask
from controllers import routes

app = Flask(__name__, template_folder = 'views') #atribui a classe Flask a 'app', que agora possui todos seus métodos e atributos
routes.init_app(app)

if __name__ == '__main__':
    app.run(host = 'localhost', port = 5000, debug = True) #modo debug serve para a aplicação ficar sempre atualizada no desenv.

