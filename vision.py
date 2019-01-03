# -*- coding: utf-8 -*-
"""
Created on Sun Dec 16 20:23:34 2018

@author: ROSS
"""

import sqlite3
from flask import Flask, render_template, url_for, redirect, session
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess'
bootstrap = Bootstrap(app)

class NameForm(FlaskForm):
    name = StringField("你的名字", validators=[DataRequired()])
    tag = SelectField(
        label='预测双色球组数',
        validators=[DataRequired('请选择标签')],
        choices=[(1, 1), (3, 3), (5, 5), (8, 8), (10, 10)],
        coerce=int 
    )
    tag1 = SelectField(
        label='是否需要准确率估算',
        validators=[DataRequired('请选择标签')],
        choices=[(1, '要'), (2, '不要')],
        coerce=int 
    )
    suggesstions = StringField("其它建议?", validators=[])
    submit = SubmitField("Submit")
    
@app.route("/", methods=["GET", "POST"])
def index():
    name = None
    time = None
    place= None
    form = NameForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        session['acc'] = form.tag1.data
        session['num']= form.tag.data
        form.name.data = ""
        
        return redirect(url_for('my_echart'))
    return render_template("tst_form.html", form=form, name=session.get('name'), acc=session.get('acc'), num=session.get('num'))

@app.route('/suggestion')
def predict():
    return render_template('predict.html',name=session.get('name'), acc=session.get('acc'), num=session.get('num'))

@app.route('/vision')
def my_echart():
#在浏览器上渲染my_templaces.html模板

    return render_template('charts.html')

if __name__ == "__main__":
	app.run(debug=True)



