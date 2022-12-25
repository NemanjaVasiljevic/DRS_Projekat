from EngineAPI import app, db
from EngineAPI.models.user import UserSchema, LoginSchema, User
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