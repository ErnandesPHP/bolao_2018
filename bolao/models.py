# -*- coding: utf-8 -*-

from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from bolao import db, login_manager


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(10))
    nome = db.Column(db.String(150))
    email = db.Column(db.String(50), unique=True)
    senha = db.Column(db.String(128))
    hora_registro = db.Column(db.DateTime(), default=datetime.now)
    #games = db.relationship("Apostas", backref="user")

    def __init__(self, username, nome, email, senha):
        self.username = username
        self.nome = nome
        self.email = email
        self.senha = senha
        self.hora_registro = datetime.now()

    def __repr__(self):
        return '<User: {}>'.format(self.nome)

    def senha(self):
        """
        Prevent pasword from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    def password(self, password):
        """
        Set password to a hashed password
        """
        self.senha = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.senha, password)

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


class Apostas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    partida_id = db.Column(db.Integer, db.ForeignKey('partida.id'))
    partida = db.relationship('Partida', foreign_keys=partida_id)
    placar_team1 = db.Column(db.Integer)
    placar_team2 = db.Column(db.Integer)
    hora = db.Column(db.DateTime(), default=datetime.now)
    edicao = db.Column(db.DateTime())
    pontuacao = db.Column(db.Integer, default=0)
    __table_args__ = (db.UniqueConstraint('usuario_id', 'partida_id',
                                          name='apostas'),)
