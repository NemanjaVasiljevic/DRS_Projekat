from EngineAPI import app, db
from EngineAPI.models.user import UserSchema
from flask import request

@app.route('/register', methods=["POST"])
def register():
    user = UserSchema().load(request.get_json())
    try:
        db.session.add(user)
        db.session.commit()
    except Exception:
        return 'NEUSPESNO', 500
    
    return 'USPESNO', 200