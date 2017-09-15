# -*- coding: utf-8 -*-

from datetime import datetime

from flask.ext.login import UserMixin
from bolao.database import db


class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150))
    email = db.Column(db.String(50), unique=True)
    telefone = db.Column(db.String(20))
    senha = db.Column(db.String(100))
    hora_registro = db.Column(db.DateTime(), default=datetime.now)
    games = db.relationship("Apostas", backref="user")

    def __repr__(self):
        return self.nome


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
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    partida_id = db.Column(db.Integer, db.ForeignKey('partida.id'))
    partida = db.relationship('Partida', foreign_keys=partida_id)
    placar_team1 = db.Column(db.Integer)
    placar_team2 = db.Column(db.Integer)
    hora = db.Column(db.DateTime(), default=datetime.now)
    edicao = db.Column(db.DateTime())
    pontuacao = db.Column(db.Integer, default=0)
    __table_args__ = (db.UniqueConstraint('usuario_id', 'partida_id',
                                          name='apostas'),)
