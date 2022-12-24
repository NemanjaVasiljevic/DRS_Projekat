from flask import Flask, render_template, flash, redirect, url_for, jsonify, request
from API.forms import RegisterForm, LoginForm
from API.models.user import User, UserSchema
from flask_login import login_user
from urllib import request as req
from urllib.error import HTTPError

from API import app

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/register', methods=["POST", "GET"])
def register_page():
    form = RegisterForm()
    if request.method == "POST":
        if form.validate_on_submit():
            user_to_create = User(form.name.data, form.last_name.data, form.address.data, form.city.data, form.country.data, form.tel_number.data, form.email_address.data, form.password1.data)

            data = UserSchema().dump(user_to_create)
            data.pop('id')
            data = jsonify(data).get_data()
            zahtev = req.Request("http://127.0.0.1:5000/register")
            zahtev.add_header('Content-Type', 'application/json; charset=utf-8')
            zahtev.add_header('Content-Length', len(data))
            
            try:
                ret = req.urlopen(zahtev, data)
            except HTTPError as e:
                flash(e.read().decode(), category='danger')
                return render_template("register.html", form=form)
                
            flash(ret.read().decode(), category='success')
            return redirect(url_for("home_page"))
        
        if form.errors != {}:
            for err_msg in form.errors.values():
                flash(err_msg.pop(), category='danger')
                
    return render_template('register.html', form=form)
    

@app.route('/login', methods=["POST", "GET"])
def login_page():
    form = LoginForm()
    return render_template('login.html', form=form)

