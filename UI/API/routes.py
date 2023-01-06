from flask import Flask, render_template, flash, redirect, url_for, jsonify, request, json, session
from API.forms import RegisterForm, LoginForm, EditProfileForm,CreditCardFrom, AccountBalanceForm, ExchangeForm
from API.models.user import User, UserSchema, LoginSchema
from API.models.credit_card import CreditCard, CreditCardSchema
from API.models.account_balance import Account_balance, Account_balanceSchema
from flask_login import login_user
from urllib import request as req
from urllib.error import HTTPError
import requests

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
            return redirect(url_for("login_page"))
        
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
            if form.validate_on_submit():
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

@app.route('/add_card', methods=["POST", "GET"])
def addCard_page():
    form = CreditCardFrom()
    if "user" in session:
        if session["user"]["verified"] == False:
            if request.method == "POST":
                if form.validate_on_submit():
                    card_to_add = CreditCard(form.cardNum.data, form.expDate.data, form.securityCode.data)
                    card_to_add.owner = session["user"]["id"]
                    
                    data = CreditCardSchema().dump(card_to_add)
                    data.pop('id')
                    data = jsonify(data).get_data()
                    zahtev = req.Request("http://127.0.0.1:5000/add_card")
                    zahtev.add_header('Content-Type', 'application/json; charset=utf-8')
                    zahtev.add_header('Content-Length', len(data))
                    
                    try:
                        ret = req.urlopen(zahtev, data)
                    except HTTPError as e:
                        flash(e.read().decode(), category='danger')
                        return render_template("credit_card.html", form=form)
                        
                    flash(ret.read().decode(), category='success')
                    session["user"]["verified"] = True
                    return redirect(url_for("home_page"))

                if form.errors != {}:
                    for err_msg in form.errors.values():
                        flash(err_msg.pop(), category='danger')
                
            return render_template('credit_card.html', form=form)
        
        else:
            flash('Account already verified.', category='primary')
            return redirect(url_for('home_page'))
        
    return redirect(url_for('login_page'))

@app.route('/add_funds', methods=["POST", "GET"])
def add_funds_page():
    form = AccountBalanceForm()
    if "user" in session:
        if session["user"]["verified"] == True:
            
            if request.method == "POST":
                if form.validate_on_submit():
                    balance_to_add = Account_balance(form.amount.data)
                    balance_to_add.user_id=session["user"]["id"]
                    data = Account_balanceSchema().dump(balance_to_add)
                    data.pop('id')
                    data = jsonify(data).get_data()
                    zahtev = req.Request("http://127.0.0.1:5000/add_funds")
                    zahtev.add_header('Content-Type', 'application/json; charset=utf-8')
                    zahtev.add_header('Content-Length', len(data))
                    
                    try:
                        ret = req.urlopen(zahtev, data)
                    except HTTPError as e:
                        flash(e.read().decode(), category='danger')
                        return render_template("add_funds.html", form=form)
                        
                    flash(ret.read().decode(), category='success')
                    return redirect(url_for("wallet_page"))

                if form.errors != {}:
                    for err_msg in form.errors.values():
                        flash(err_msg.pop(), category='danger')
                
            return render_template('add_funds.html', form=form)
        
    return redirect(url_for('login_page'))


@app.route('/wallet', methods=["GET"])
def wallet_page():
    if "user" in session:
        
        try:
            ret = req.urlopen(f"http://127.0.0.1:5000/wallet/{session['user']['id']}")
            wallet = json.loads(ret.read())
            return render_template('wallet.html', wallet=wallet)
        except HTTPError as e:
            flash(e.read().decode(), category='danger')
            return redirect(url_for("home_page"))
    
    return redirect(url_for("login_page"))


def get_from_currencies():
    try:
        ret = req.urlopen(f"http://127.0.0.1:5000/wallet/{session['user']['id']}")
        result = json.loads(ret.read())
        currencies = [r["currency"] for r in result]
        return currencies
    except HTTPError as e:
        flash(e.read().decode(), category='danger')
        return redirect(url_for("home_page"))
    
def get_exchange_rates(from_currency):
    url = "https://api.exchangerate-api.com/v4/latest/" + from_currency
    response = requests.request("GET", url)
    result = json.loads(response.text)
    table = result.get("rates")
    table.pop(from_currency)
    return table


@app.route('/currency_exchange', methods=["POST", "GET"])
def currency_exchange_page():
    form = ExchangeForm()
    
    if "user" in session:
        
        if request.method == "POST":
            if form.is_submitted():
                if form.submit.data:
                    
                    table = get_exchange_rates(form.from_currency.data)
                    
                    rate = table[form.to_currency.data]
                    
                    if form.amount.data == '':
                        flash('Amount cannot be empty!', category='danger')
                        return redirect(url_for("currency_exchange_page"))
                    
                    if int(form.amount.data) == 0:
                        flash('Amount must be greater than 0.', category='danger')
                        return redirect(url_for("currency_exchange_page"))

                    data = {'user_id': session["user"]["id"], 'from_currency': form.from_currency.data, 
                            'to_currency': form.to_currency.data, 'amount': form.amount.data, 'rate': rate}
                    
                    data = jsonify(data).get_data()
                    zahtev = req.Request("http://127.0.0.1:5000/currency_exchange")
                    zahtev.add_header('Content-Type', 'application/json; charset=utf-8')
                    zahtev.add_header('Content-Length', len(data))
                    
                    try:
                        ret = req.urlopen(zahtev, data)
                    except HTTPError as e:
                        flash(e.read().decode(), category='danger')
                        return redirect(url_for('add_funds_page'))
                        
                    flash(ret.read().decode(), category='success')
                    return redirect(url_for("wallet_page"))
                
                if form.refresh.data:
                    
                    from_currencies = get_from_currencies()
                    form.from_currency.choices = from_currencies
                    
                    table = get_exchange_rates(form.from_currency.data)
                    
                    form.to_currency.choices = [key for key, value in table.items()]
            
                    return render_template('currency_exchange.html', table=table, form=form)
        

        from_currencies = get_from_currencies()
        form.from_currency.choices = from_currencies
        
        table = get_exchange_rates(from_currencies[0])
        
        form.to_currency.choices = [key for key, value in table.items()]
            
        return render_template('currency_exchange.html', table=table, form=form)
            
    
    return redirect(url_for("login_page"))
