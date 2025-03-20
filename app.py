# instalar flask = 'pip install flask'
# conferir a versão = 'flask --version'
# rodar a aplicação = 'python app.py'

from flask import Flask, render_template #importando a classe Flask da biblioteca flask

app = Flask(__name__, template_folder = 'views') #atribui a classe Flask a 'app', que agora possui todos seus métodos e atributos

@app.route('/') #decorator atribuindo a função home() a rota principal ('/')
def home():
    return render_template('index.html')

@app.route('/games')
def games():
    game = {'Título' : 'CS-GO',
            'Ano' : 2012,
            'Categoria' : 'FPS Online'}
    jogadores = ['Pedro', 'João', 'Marcos', 'Maria', 'Diego']
    return render_template('games.html', game=game, jogadores=jogadores)

if __name__ == '__main__':
    app.run(host = 'localhost', port = 5000, debug = True) #modo debug serve para a aplicação ficar sempre atualizada no desenv.

