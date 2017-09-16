# -*- coding: utf-8 -*-

from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from bolao import db, login_manager
from sqlalchemy import ForeignKey

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(10))
    nome = db.Column(db.String(150))
    email = db.Column(db.String(50), unique=True)
    password_hash = db.Column(db.String(128))
    hora_registro = db.Column(db.DateTime(), default=datetime.now)

    def __init__(self, username, nome, email):
        self.username = username
        self.nome = nome
        self.email = email
        self.hora_registro = datetime.now()

    def __repr__(self):
        return '<User: {}>'.format(self.nome)

    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    def save(self):
        db.session.add(self)
        db.session.commit()
        return True

@login_manager.user_loader
def load_user(user_id):
    return Employee.query.get(int(user_id))

    
class Time(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sigla = db.Column(db.String(3), unique=True)
    nome = db.Column(db.String(80))
    posicao = db.Column(db.Integer)

    def __repr__(self):
        return self.nome


class Partida(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    grupo = db.Column(db.String(1))
    hora = db.Column(db.DateTime())
    local = db.Column(db.String(50))
    time1_id = db.Column(db.Integer, db.ForeignKey('time.id'))
    time1 = db.relationship('Time', foreign_keys=time1_id)
    time2_id = db.Column(db.Integer, db.ForeignKey('time.id'))
    time2 = db.relationship('Time', foreign_keys=time2_id)
    placar_time1 = db.Column(db.Integer)
    placar_time2 = db.Column(db.Integer)

    def __repr__(self):
        return u"%s X %s" % (self.time1, self.time2)


class Aposta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    usuario = db.relationship('User', foreign_keys=usuario_id)
    partida_id = db.Column(db.Integer, db.ForeignKey('partida.id'))
    partida = db.relationship('Partida', foreign_keys=partida_id)
    placar_time1 = db.Column(db.Integer)
    placar_time2 = db.Column(db.Integer)
    hora = db.Column(db.DateTime(), default=datetime.now)
    edicao = db.Column(db.DateTime())
    pontuacao = db.Column(db.Integer, default=0)
    __table_args__ = (db.UniqueConstraint('usuario_id', 'partida_id',
                                          name='aposta'),) 