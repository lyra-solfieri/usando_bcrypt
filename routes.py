

from flask import Flask, request, render_template
from models import db, bcrypt, User

# Criação da aplicação Flask
app = Flask(__name__)

# Configuração do banco de dados SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db.init_app(app)

# Criação das tabelas no banco de dados
with app.app_context():
    db.create_all()


@app.route('/cadastro', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Geração do hash da senha
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Criação de um novo usuário
        new_user = User(username=username, password=hashed_password)

        # Adição do novo usuário ao banco de dados
        db.session.add(new_user)
        db.session.commit()

        return 'Cadastro Realizado com sucesso'  # Mensagem de sucesso em caso de cadastro bem-sucedido
    else:
        return render_template('cadastro.html')  # Renderiza o formulário de registro


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Busca pelo usuário no banco de dados
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            return render_template('home.html')  # Renderiza a página inicial em caso de login bem-sucedido
        else:
            return render_template('cadastro.html')  # Renderiza o formulário de cadastro em caso de falha no login

    return render_template('login.html')  # Renderiza o formulário de login
