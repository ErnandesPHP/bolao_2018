from flask import request, jsonify, Blueprint, Flask, render_template, request, url_for, \
                  redirect, flash, abort, session
from flask.views import MethodView
from flask_login import LoginManager, login_user, logout_user, login_required
from bolao import db, app
from bolao.models import User
from proveedor import GoogleLogin, LinkedInLogin, FacebookLogin
from bolao.forms import LoginForm, RegistrationForm

bolao = Blueprint('bolao', __name__)

google_login = GoogleLogin(app)
linkedin_login = LinkedInLogin(app)
facebook_login = FacebookLogin(app)
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)

"""
@bolao.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validators=[]e_on_submit():
        login_user(user)

        flash('Logged in successfully.')

        next = app.request.args.get('next')
        if not is_safe_url(next):
            return abort(400)

        return redirect(next or url_for('index'))
    return render_template('login.html',
                            form=form,
                            botoes = [
                        facebook_login.authorization_url(),        
                        google_login.authorization_url(),
                        linkedin_login.authorization_url()
               ]
               )    

@app.route("/logout")
@login_required
def logout2():
    logout_user()
    return redirect(url_for('index'))
"""

@bolao.route("/listar")
def listar():
    users = User.query.all()
    return render_template("usuarios.html", users=users)


@bolao.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        username = (request.form.get("username"))        
        nome = (request.form.get("nome"))
        email = (request.form.get("email"))
        senha = (request.form.get("senha"))
        if nome and email and senha:
            teste1 = User.query.filter_by(username=username).first()
            teste2 = User.query.filter_by(email=email).first()
            if teste1 or teste2:
                flash('Usuário ou E-mail já existe! Favor logar!')
            else:
                u = User(username=username, nome=nome, email=email)
                u.password(senha)
                u.save()
                flash('Usuário cadastrado com sucesso! Favor logar!')
            return redirect(url_for('.login'))
    # load registration template
    return render_template('index.html', title='Register', \
                           botoes = [
                                facebook_login.authorization_url(),        
                                google_login.authorization_url(),
                                linkedin_login.authorization_url()
                                     ])

@bolao.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', title='Index', \
                            botoes = [
                                facebook_login.authorization_url(),        
                                google_login.authorization_url(),
                                linkedin_login.authorization_url()
                                     ])


@bolao.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get("form-username")
        password = request.form.get("form-password")
        usuario = User.query.filter_by(username=username).first()
        print(username)
        print(usuario)
        a = usuario.verify_password(password)
        print(a)
        if usuario.verify_password(password):
            return redirect(url_for('.listar'))
    return "Login"

@bolao.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have successfully been logged out.')

    # redirect to the login page
    return redirect(url_for('login'))