from EngineAPI import app, db
from EngineAPI.models.user import UserSchema, LoginSchema, User
from EngineAPI.models.credit_card import CreditCard, CreditCardSchema
from EngineAPI.models.account_balance import Account_balance, Account_balanceSchema
from flask import request, jsonify, json, session
from flask_login import login_user, current_user, login_required
import requests

#pomocna funkcija
def get_value(to_currency, from_currency):
    url = "https://api.exchangerate-api.com/v4/latest/" + to_currency

    response = requests.request("GET", url)
    result = json.loads(response.text)
    resenje = result.get("rates")
    return resenje[from_currency]


@app.route('/register', methods=["POST"])
def register():
    user = UserSchema().load(request.get_json())
    wallet = Account_balance("RSD",0)  
    last_user = User.query.all() #ovde pokupi sve usere
    if len(last_user) != 0:
        last_user_id = last_user[-1].id #ovde uzme id poslednjeg
        wallet.user_id = last_user_id + 1 #ovde poveca za 1 jer to ce biti id ovog sto se upravo sad registruje
    else:
        wallet.user_id = 1
    try:
        #ovde nekako da dobavimo id od usera koji se trenutno registruje
        db.session.add(user)
        db.session.add(wallet)
        db.session.commit()
    except Exception:
        return f'User with email {user.email_address} already exists.', 406
    
    return 'Successfully created account!', 201

@app.route('/login', methods=["POST"])
def login():
    data = LoginSchema().load(request.get_json())
    email_address = data["email_address"]
    password = data["password"]
    
    user = User.query.filter_by(email_address = email_address).first()
    if user:
        if user.password == password:
            ret_user = UserSchema().dump(user)
            ret_user["password"] = ""
            return jsonify(ret_user), 202
        else:
            return 'Wrong password!', 404
        
    return 'User does not exist!', 404

@app.route('/edit_profile', methods=["POST"])
def edit_profile():
    user = UserSchema().load(request.get_json())
    user_to_edit = User.query.filter_by(id = user.id).first()
    
    if user_to_edit:
        try:
            user_to_edit.name = user.name
            user_to_edit.last_name = user.last_name
            user_to_edit.address = user.address
            user_to_edit.city = user.city
            user_to_edit.country = user.country
            user_to_edit.tel_number = user.tel_number
            if user.password != "":
                user_to_edit.password = user.password
                
            db.session.commit()
            
            ret_user = UserSchema().dump(user)
            ret_user["password"] = ""
            return jsonify(ret_user), 202
        except Exception:
            return "Unable to edit user.", 406
    
    return "User does not exist!", 404
    
@app.route('/add_card', methods=["POST", "GET"])
def add_card():
    card = CreditCardSchema().load(request.get_json())
    user = User.query.filter_by(id=card.owner).first()
    try:
        value = get_value('USD', 'RSD')
        card.amount = card.amount - value
        user.verified = True
        db.session.add(card)
        db.session.commit()
    except Exception:
        return 'Something went wrong. Try again.', 406
            
    return 'Successfully added credit card. You have been charged 1$ for verification.', 201


@app.route('/add_funds', methods=["POST", "GET"])
def add_funds():
    added_value = Account_balanceSchema().load(request.get_json())  
    user = User.query.filter_by(id=added_value.user_id).first()
    card=CreditCard.query.filter_by(owner=user.id).first()
    current_balance = Account_balance.query.filter_by(user_id = user.id).first()

    try:
        if card.amount < added_value.amount:
            return "You don't have enough money on credit card.", 406
        
        card.amount = card.amount - added_value.amount
        current_balance.amount = current_balance.amount + added_value.amount
        db.session.commit()
    except Exception:
        return 'Something went wrong. Try again.', 406
            
    return 'You have successfully deposited money into your account.', 200


@app.route('/wallet/<id>', methods=["GET"])
def wallet(id):
    wallet_list = Account_balance.query.filter_by(user_id=id).all()
    return jsonify(Account_balanceSchema().dump(wallet_list, many=True)), 200