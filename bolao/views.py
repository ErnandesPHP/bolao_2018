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
    if form.validate_on_submit():
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

@app.route("/lista")
def lista():
    users = User.query.all()
    print(users)
    return render_template("usuarios.html", users=users)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        nome = (request.form.get("nome"))
        email = (request.form.get("email"))
        senha = (request.form.get("senha"))
        username = (request.form.get("username"))
        if nome and email and senha:
            u = User(username=username, nome=nome, email=email, senha=senha)
            u.save()
        flash('You have successfully registered! You may now login.')
        return redirect(url_for('login'))
    # load registration template
    return render_template('index.html', form=form, title='Register')

@bolao.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', title='Index', \
                            botoes = [
                                facebook_login.authorization_url(),        
                                google_login.authorization_url(),
                                linkedin_login.authorization_url()
                                     ])

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have successfully been logged out.')

    # redirect to the login page
    return redirect(url_for('login'))