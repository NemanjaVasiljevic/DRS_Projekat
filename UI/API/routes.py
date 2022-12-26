from flask import Flask, render_template, flash, redirect, url_for, jsonify, request, json, session
from API.forms import RegisterForm, LoginForm, EditProfileForm
from API.models.user import User, UserSchema, LoginSchema
from flask_login import login_user
from urllib import request as req
from urllib.error import HTTPError

from API import app

@app.route('/')
@app.route('/home')
def home_page():
    return render_template("home.html")

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
    if request.method == "POST":
        if form.validate_on_submit():
            user_to_login = LoginSchema().load({"email_address":form.email_address.data, "password":form.password.data})
            data = jsonify(user_to_login).get_data()
            zahtev = req.Request("http://127.0.0.1:5000/login")
            zahtev.add_header('Content-Type', 'application/json; charset=utf-8')
            zahtev.add_header('Content-Length', len(data))
            try:
                ret = req.urlopen(zahtev, data)
            except HTTPError as e:
                flash(e.read().decode(), category='danger')
                return render_template("login.html", form=form)
            
            user = json.loads(ret.read())
            session["user"] = user
            flash(f"Successfully logged in as {user['name']}.", category='success')
            return redirect(url_for("home_page"))
        
        if form.errors != {}:
            for err_msg in form.errors.values():
                flash(err_msg.pop(), category='danger')

    return render_template('login.html', form=form)

@app.route('/logout')
def logout_page():
    if "user" in session:
        session.pop("user")
        flash(f"Successfully logged out.", category='info')
        
    return render_template('home.html')

@app.route('/edit_profile', methods=["GET", "POST"])
def edit_profile_page():
    form = EditProfileForm()
    if "user" in session:
        if request.method == "POST":
            user_to_change = User(form.name.data, form.last_name.data, form.address.data, form.city.data, form.country.data, form.tel_number.data, form.email_address.data, form.password1.data)
            user_to_change.id = session["user"]["id"]
            
            data = UserSchema().dump(user_to_change)
            data = jsonify(data).get_data()
            zahtev = req.Request("http://127.0.0.1:5000/edit_profile")
            zahtev.add_header('Content-Type', 'application/json; charset=utf-8')
            zahtev.add_header('Content-Length', len(data))
            
            try:
                ret = req.urlopen(zahtev, data)
            except HTTPError as e:
                flash(e.read().decode(), category='danger')
                return render_template("edit_profile.html", form=form)
            
            user = json.loads(ret.read())
            session["user"] = user
            flash('Successfully edited profile.', category='info')
            return redirect(url_for("home_page"))
        
        if form.errors != {}:
            for err_msg in form.errors.values():
                flash(err_msg.pop(), category='danger')

        return render_template('edit_profile.html', form=form)
        
    return redirect(url_for('login_page'))