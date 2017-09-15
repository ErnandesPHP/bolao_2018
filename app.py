import os

from flask import Flask, jsonify, render_template, request, url_for, redirect
from proveedor import GoogleLogin, LinkedInLogin, FacebookLogin

app = Flask(__name__, static_url_path = "", static_folder = "static")
app.config.update(
    SECRET_KEY="x34sdfm34",
)

for config in (
    "GOOGLE_LOGIN_CLIENT_ID",
    "GOOGLE_LOGIN_CLIENT_SECRET",
    "LINKEDIN_LOGIN_CLIENT_ID",
    "LINKEDIN_LOGIN_CLIENT_SECRET",
    "FACEBOOK_LOGIN_CLIENT_ID",
    "FACEBOOK_LOGIN_CLIENT_SECRET"

):
  app.config[config] = os.environ[config]


google_login = GoogleLogin(app)
linkedin_login = LinkedInLogin(app)
facebook_login = FacebookLogin(app)

@app.route("/")
@app.route("/home")
def home():
  return render_template("index.html")

@app.route("/cadastrar")
def cadastrar():
  return render_template("cadastro.html")

def voltar():
  return render_template("home")

@app.route("/cadastro", methods=['GET', 'POST'])
def cadastro():
  if request.method == "POST":
    nome = (request.form.get("nome"))
    rua = (request.form.get("rua"))
    numero = (request.form.get("numero"))
    bairro = (request.form.get("bairro"))
    cidade = (request.form.get("cidade"))
    estado = (request.form.get("estado"))
    fone = (request.form.get("fone"))
    cpf = (request.form.get("cpf"))
    email = (request.form.get("email"))

    if nome and rua and numero and bairro and cidade and estado and fone and cpf and email:
      p = Pessoa(nome, rua, numero, bairro, cidade, estado, fone, cpf, email)
      db.session.add(p)
      db.session.commit()
      
  return redirect(url_for("home"))

@app.route("/lista")
def lista():
  pessoas = Pessoa.query.all()
  return render_template("lista.html", pessoas=pessoas)

@app.route("/atualizar/<int:id>", methods=['GET', 'POST'])
def atualizar(id):
  pessoa = Pessoa.query.filter_by(_id=id).first()
  if request.method == "POST":
    nome = (request.form.get("nome"))
    rua = (request.form.get("rua"))
    numero = (request.form.get("numero"))
    bairro = (request.form.get("bairro"))
    cidade = (request.form.get("cidade"))
    estado = (request.form.get("estado"))
    fone = (request.form.get("fone"))
    email = (request.form.get("email"))

    if nome and rua and numero and bairro and cidade and estado and fone and email:
      pessoa.nome = nome
      pessoa.rua= rua
      pessoa.numero = numero
      pessoa.bairro = bairro
      pessoa.cidade = cidade
      pessoa.estado = estado
      pessoa.fone = fone
      pessoa.email = email
      db.session.commit()

  return render_template("atualizar.html", pessoa=pessoa)

@app.route("/excluir/<int:id>")
def excluir(id):
  pessoa = Pessoa.query.filter_by(_id=id).first()

  db.session.delete(pessoa)
  db.session.commit()
  
  pessoas = Pessoa.query.all()
  return render_template("lista.html", pessoas=pessoas)

#@app.route("/")
def index():
  return """
<html>
<a href="{}">Login com Google</a> <br>
<a href="{}">Login com Linkedin</a> <br>
<a href="{}">Login com Facebook</a> <br>
""".format(google_login.authorization_url(),
           linkedin_login.authorization_url(),
           facebook_login.authorization_url())


@google_login.login_success
def login_success(token, profile):
  return jsonify(token=token, profile=profile)


@google_login.login_failure
def login_failure(e):
  return jsonify(error=str(e))


@linkedin_login.login_success
def login_success(token, profile):
  return jsonify(token=token, profile=profile)


@linkedin_login.login_failure
def login_failure(e):
  return jsonify(error=str(e))


@facebook_login.login_success
def login_success(token, profile):
  return jsonify(token=token, profile=profile)


@facebook_login.login_failure
def login_failure(e):
  return jsonify(error=str(e))


if __name__ == "__main__":
  app.run(host="0.0.0.0", debug=True)
