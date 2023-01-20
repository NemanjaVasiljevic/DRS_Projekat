from flask import Flask, render_template, flash, redirect, url_for, jsonify, request, json, session
from API.forms import RegisterForm, LoginForm, EditProfileForm,CreditCardFrom, AccountBalanceForm, ExchangeForm, TransactionForm
from API.models.user import User, UserSchema, LoginSchema
from API.models.credit_card import CreditCard, CreditCardSchema
from API.models.account_balance import Account_balance, Account_balanceSchema
from flask_login import login_user
from urllib import request as req
from urllib.error import HTTPError
import requests

from API import app
address = "http://engine-container:5000"

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
            zahtev = req.Request(f"{address}/register")
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
            zahtev = req.Request(f"{address}/login")
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
    
    return redirect(url_for('login_page'))

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
                zahtev = req.Request(f"{address}/edit_profile")
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
                    zahtev = req.Request(f"{address}/add_card")
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
                    zahtev = req.Request(f"{address}/add_funds")
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
            ret = req.urlopen(f"{address}/wallet/{session['user']['id']}")
            wallet = json.loads(ret.read())
            return render_template('wallet.html', wallet=wallet)
        except HTTPError as e:
            flash(e.read().decode(), category='danger')
            return redirect(url_for("home_page"))
    
    return redirect(url_for("login_page"))


def get_from_currencies():
    try:
        ret = req.urlopen(f"{address}/wallet/{session['user']['id']}")
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
                    zahtev = req.Request(f"{address}/currency_exchange")
                    zahtev.add_header('Content-Type', 'application/json; charset=utf-8')
                    zahtev.add_header('Content-Length', len(data))
                    
                    try:
                        ret = req.urlopen(zahtev, data)
                    except HTTPError as e:
                        flash(e.read().decode(), category='danger')
                        if session["user"]["verified"]:
                            return redirect(url_for('add_funds_page'))
                        else:
                            return redirect(url_for('home_page'))
                        
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


@app.route('/execute_transaction', methods=["POST", "GET"])
def execute_transaction_page():
    form = TransactionForm()
    currencies = get_from_currencies()
    form.currency.choices = currencies
    if "user" in session:
        if request.method == "POST":
            if form.is_submitted():
                
                if form.switch.data:
                    return render_template('execute_transaction.html', form=form, card=True)
                
                if form.submit.data:
                    
                    #validacija
                    if form.email.data == '':
                        flash('Email cannot be empty!', category='danger')
                        return render_template("execute_transaction.html", form=form, card=False)
                        
                    if form.cardNum.data == '':
                        flash('Card number cannot be empty!', category='danger')
                        return render_template("execute_transaction.html", form=form, card=True)
                    
                    if form.amount.data == '':
                        flash('Amount cannot be empty!', category='danger')
                        if form.email.data == None:
                            return render_template("execute_transaction.html", form=form, card=True)
                        else:
                            return render_template("execute_transaction.html", form=form, card=False)
                    
                    try:
                        float(form.amount.data)
                    except Exception:
                        flash('Amount must be number!', category='danger')
                        if form.email.data == None:
                            return render_template("execute_transaction.html", form=form, card=True)
                        else:
                            return render_template("execute_transaction.html", form=form, card=False)
                    ########################################
                    
                    data = {'sender': session["user"]["email_address"], 'receiver_email': form.email.data, 
                            'receiver_card': form.cardNum.data, 'currency': form.currency.data, 'amount': form.amount.data}
                    
                    data_to_send = jsonify(data).get_data()
                    zahtev = req.Request(f"{address}/execute_transaction")
                    zahtev.add_header('Content-Type', 'application/json; charset=utf-8')
                    zahtev.add_header('Content-Length', len(data_to_send))
                
                    try:
                        ret = req.urlopen(zahtev, data_to_send)
                    except HTTPError as e:
                        flash(e.read().decode(), category='danger')
                        if(data['receiver_email'] == None):
                            return render_template("execute_transaction.html", form=form, card=True)
                        else:
                            return render_template("execute_transaction.html", form=form, card=False)
                            
                    flash(ret.read().decode(), category='success')
                    return redirect(url_for("transaction_history_page"))
            
            
        return render_template('execute_transaction.html', form=form, card=False)
    
    return redirect(url_for('login_page'))

@app.route('/transaction_history', methods=["GET"])
def transaction_history_page():
    if "user" in session:
        sent_transactions = []
        received_transactions = []
        try:
            ret = req.urlopen(f'{address}/transaction_history/{session["user"]["email_address"]}')
            transactions = json.loads(ret.read())
            
            for t in transactions:
                if t["sender"] == session["user"]["email_address"]:
                    sent_transactions.append(t)
                    
                if t["receiver"] == session["user"]["email_address"]:
                    received_transactions.append(t)
            
            return render_template('transaction_history.html', sent=sent_transactions, received=received_transactions)
        except HTTPError as e:
            flash(e.read().decode(), category='danger')
            return redirect(url_for('home_page'))
    
    return redirect(url_for('login_page'))