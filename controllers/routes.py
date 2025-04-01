import urllib.request
from flask import render_template, request, url_for, redirect, flash, session
from markupsafe import Markup
import urllib
import json
from models.database import db, Game, Usuario
from werkzeug.security import generate_password_hash, check_password_hash

jogadores = []
gamelist = [{'Título' : 'CS-GO', 'Ano' : 2012, 'Categoria' : 'FPS Online'}]

def init_app(app):
    
    #Função de middleware para verificar a autenticação do usuário
    @app.before_request
    def check_auth():
        # Rotas que não precisam de autenticação
        routes = ['login', 'caduser', 'home']
        # Se a rota atual não requer autenticação, permite o acesso
        if request.endpoint in routes or request.path.startswith('/static/'):
            return
        # Se o usuário não estiver autenticado, redireciona para a página de login
        if 'user_id' not in session:
            return redirect(url_for('login'))
    
    @app.route('/') #decorator atribuindo a função home() a rota principal ('/')
    def home():
        return render_template('index.html')

    # CRUD - LISTAGEM E CADASTRO
    @app.route('/estoque', methods=['GET', 'POST'])
    @app.route('/estoque/delete/<int:id>')
    def estoque(id=None):

        if id:
            game = Game.query.get(id)
            # Deleta o cadastro pela ID
            db.session.delete(game)
            db.session.commit()
            return redirect(url_for('estoque'))
        # Cadastra um novo jogo
        if request.method == 'POST':
            newgame = Game(request.form['titulo'], request.form['ano'], request.form['categoria'],request.form['plataforma'], request.form['preco'], request.form['quantidade'])
            db.session.add(newgame)
            db.session.commit()
            return redirect(url_for('estoque'))
        else:
            # Captura o valor de 'page' que foi passado pelo método GET
            # Define como padrão o valor 1 e o tipo inteiro
            page = request.args.get('page', 1, type=int)
            # Valor padrão de registros por página (definimos 3)
            per_page = 3
            # Faz um SELECT no banco a partir da pagina informada (page)
            # Filtrando os registro de 3 em 3 (per_page)
            games_page = Game.query.paginate(page=page,per_page=per_page)
            return render_template('estoque.html', gamesestoque=games_page)
        
    @app.route('/edit/<int:id>', methods=['GET', 'POST'])
    def edit(id):
        g = Game.query.get(id)
        # Edita o jogo com as informações do formulário
        if request.method == 'POST':
            g.titulo = request.form['titulo']
            g.ano = request.form['ano']
            g.categoria = request.form['categoria']
            g.plataforma = request.form['plataforma']
            g.preco = request.form['preco']
            g.quantidade = request.form['quantidade']
            db.session.commit()
            return redirect(url_for('estoque'))
        return render_template('editgame.html', g=g)
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            user = Usuario.query.filter_by(email=email).first()
            if user and check_password_hash(user.password, password):
                session['user_id'] = user.id
                session['email'] = user.email
                nickname = user.email.split('@')
                flash(f'Login bem-sucedido! Bem-vindo {nickname[0]}!', 'success')
                return redirect(url_for('home'))
            else:
                flash('Falha no login. Verifique seu nome de usuário e senha.', 'danger')
        return render_template('login.html')
    
    @app.route('/logout', methods=['GET', 'POST'])
    def logout():
        session.clear()
        return redirect(url_for('home'))
        
    @app.route('/caduser', methods=['GET', 'POST'])
    def caduser():
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            user = Usuario.query.filter_by(email=email).first()
            if user:
                msg = Markup("Usuário já cadastrado. Faça<a href='/login'>login.</a>")
                flash(msg, 'danger')
                return redirect(url_for('caduser'))
            else:
                hashed_password = generate_password_hash(password, method='scrypt')
                new_user = Usuario(email=email, password=hashed_password)
                db.session.add(new_user)
                db.session.commit()
                flash('Registro realizado com sucesso! Faça o login.', 'success')
                return redirect(url_for('login'))
        return render_template('caduser.html')

    
    @app.route('/apigames', methods=['GET', 'POST'])
    @app.route('/apigames/<int:id>', methods=['GET', 'POST'])
    def apigames(id=None):
        url = 'https://www.freetogame.com/api/games'
        res = urllib.request.urlopen(url)
        data = res.read()
        gamesjson = json.loads(data)
        if id:
            ginfo = []
            for g in gamesjson:
                if g['id'] == id:
                    ginfo = g
                    break
            if ginfo:
                return render_template('gameinfo.html', ginfo=ginfo)
            else:
                return f'Game com a ID {id} não foi encontrado.'
        else:
            return render_template('apigames.html', gamesjson=gamesjson)