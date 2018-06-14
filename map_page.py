#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author: yata
# @Date:   2018-06-13 22:00
# @Last Modified by:   yata

import os, json
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, _app_ctx_stack
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.update(dict(
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:yata123@140.143.32.44:3306/yata_data_01',
    DEBUG = True,
    SECRET_KEY = 'yanzhipeng',
    SQLALCHEMY_TRACK_MODIFICATIONS = False
))

db = SQLAlchemy(app)

class ElmNew(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255), nullable = True)
    ele_id = db.Column(db.Integer, nullable = False)
    latitude = db.Column(db.Float, nullable = True)
    longitude = db.Column(db.Float, nullable = True)

    def __init__(self, name, ele_id, latitude, longitude):
        self.name = name
        self.ele_id = ele_id
        self.latitude = latitude
        self.longitude = longitude

    def __repr__(self):
        return '<ElmNew %r>' % self.name

@app.route('/')
def show_map():

    query = db.session.query(ElmNew.ele_id.distinct().label('ele_id'), ElmNew.name, ElmNew.latitude, ElmNew.longitude).limit(4000)
    # data = ElmNew.query.limit(10).offset(2)
    data = query.all()
    cwd = []
    for info in data:
        cwd.append({'longitude': info.longitude, 'latitude': info.latitude})

    return render_template('map.html', data = json.dumps(cwd))


if __name__ == '__main__':
    app.run()