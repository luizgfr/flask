# instalar flask = 'pip install flask'
# conferir a versão = 'flask --version'
# rodar a aplicação = 'python app.py'

from flask import Flask #importando a classe Flask da biblioteca flask

app = Flask(__name__) #atribui a classe Flask a 'app', que agora possui todos seus métodos e atributos

@app.route('/') #decorator atribuindo a função home() a rota principal ('/')
def home():
    return '<h1>Esta é a homepage</h1>'

if __name__ == '__main__':
    app.run(host = 'localhost', port = 5000, debug = True) #modo debug serve para a aplicação ficar sempre atualizada no desenv.

