from EngineAPI import app, db
from EngineAPI.models.user import UserSchema, LoginSchema, User
from EngineAPI.models.creditCard import CreditCard, CreditCardSchema
from flask import request, jsonify, json, session
from flask_login import login_user, current_user, login_required


@app.route('/register', methods=["POST"])
def register():
    user = UserSchema().load(request.get_json())
    try:
        db.session.add(user)
        db.session.commit()
    except Exception:
        return 'NEUSPESNO', 500
    
    return 'USPESNO', 200

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
    try:
        db.session.add(card)
        db.session.commit()
    except Exception:
        return 'NEUSPESNO', 500
            
    return 'USPESNO', 200