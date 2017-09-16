import os

from flask import Flask, jsonify, render_template, request, url_for, redirect, flash, abort
from proveedor import GoogleLogin, LinkedInLogin, FacebookLogin
from bolao.models import User
from flask_login import LoginManager
from bolao.forms import LoginForm

google_login = GoogleLogin(app)
linkedin_login = LinkedInLogin(app)
facebook_login = FacebookLogin(app)
login_manager = LoginManager()
login_manager.init_app(app)


def voltar():
  return render_template("home")

'''
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
'''
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

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)