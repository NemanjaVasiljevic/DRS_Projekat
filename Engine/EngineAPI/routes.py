from EngineAPI import app, db, cc, pc
from EngineAPI.models.user import UserSchema, LoginSchema, User, ExchangeSchema
from EngineAPI.models.credit_card import CreditCard, CreditCardSchema
from EngineAPI.models.account_balance import Account_balance, Account_balanceSchema
from EngineAPI.models.transaction import Transaction, TransactionSchema, TransactionState, TransactionSchema2
from flask import request, jsonify, json
import requests
import threading
from time import sleep

lock = threading.Lock()

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
    last_user_id = last_user[-1].id #ovde uzme id poslednjeg
    wallet.user_id = last_user_id + 1 #ovde poveca za 1 jer to ce biti id ovog sto se upravo sad registruje
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


@app.route('/currency_exchange', methods=["POST"])
def currency_exchange():
    data = ExchangeSchema().dump(request.get_json()) 
    
    account_balance = Account_balance.query.filter_by(user_id=data["user_id"]).all()
    exists = False
    try:
        for item in account_balance:
            if item.currency == data["from_currency"]:
                if item.amount < data["amount"]:
                    return "You don't have enough money for exchange.", 400
                
                item.amount -= data["amount"]
                db.session.commit()
                
            if item.currency == data["to_currency"]:
                exists = True
                item.amount += data["amount"] * data["rate"]
                db.session.commit()
                
        if not exists:
            amount = data["amount"] * data["rate"]
            new_item = Account_balance(data["to_currency"], amount)
            new_item.user_id = data["user_id"]
            db.session.add(new_item)
            db.session.commit()
            
        return F"Successfully exchanged {data['amount']} {data['from_currency']} to {data['to_currency']}.", 200
                
    except Exception:
        return "Something went wrong. Try again!", 400
    
@app.route('/transaction_history/<email_address>', methods=["GET"])
def transaction_history(email_address):
    sent_transactions = Transaction.query.filter_by(sender=email_address).all()
    received_transactions = Transaction.query.filter_by(receiver=email_address).all()
    transactions = sent_transactions + received_transactions
    return jsonify(TransactionSchema2().dump(transactions, many=True))


@app.route('/execute_transaction', methods=["POST"])
def transaction():
    data = TransactionSchema().dump(request.get_json())

    card = None
    receiver_account_balance = None
    
    sender = User.query.filter_by(email_address=data["sender"]).first()
    
    if data["receiver_email"] != None:
        receiver = User.query.filter_by(email_address=data["receiver_email"]).first()
        if receiver == None:
            return f"User with email {data['receiver_email']} does not exist!", 404
        
        r_account_balance = Account_balance.query.filter_by(user_id=receiver.id).all()
        for item in r_account_balance:
            if item.currency == data["currency"]:
                receiver_account_balance = item
                break
        
    else:
        card = CreditCard.query.filter_by(cardNum=data["receiver_card"]).first()
        if card == None:
            return "Incorrect card number or user is not verified.", 404
        
        receiver = User.query.filter_by(id=card.owner).first()

    if receiver.id == sender.id:
        return "You cannot send money to yourself.", 400
    
    sender_account_balance = Account_balance.query.filter_by(user_id=sender.id).all()
    for item in sender_account_balance:
        if item.currency == data["currency"]:
            if item.amount < data["amount"]:
                transaction = Transaction(sender.email_address, receiver.email_address, data["currency"], data["amount"], TransactionState.REFUSED, None)
                db.session.add(transaction)
                db.session.commit()
                return "You don't have enough money for transaction.", 400
            
            item.amount -= data["amount"]
            item.reserved += data["amount"]
            db.session.commit()
            sender_account_balance = item
            
    transaction = Transaction(sender.email_address, receiver.email_address, data["currency"], data["amount"], TransactionState.PROCESSING, None)
    db.session.add(transaction)
    db.session.commit()

    if card == None:
        p = threading.Thread(target=processing_transaction, args=(receiver.id, transaction.id, sender_account_balance.id, receiver_account_balance.id, -1))
    else:
        p = threading.Thread(target=processing_transaction, args=(receiver.id, transaction.id, sender_account_balance.id, -1, card.id))
        
    p.start()
    return "Transaction successfully started. Processing transaction...", 201


def processing_transaction(receiver_id, transaction_id, sender_account_balance_id, receiver_account_balance_id, card_id):
    with app.app_context():
        lock.acquire()
        
        receiver = User.query.filter_by(id=receiver_id).first()
        transaction = Transaction.query.filter_by(id=transaction_id).first()
        sender_account_balance = Account_balance.query.filter_by(id=sender_account_balance_id).first()
        receiver_account_balance = Account_balance.query.filter_by(id=receiver_account_balance_id).first()
        card = CreditCard.query.filter_by(id=card_id).first()
        
        pc.send(transaction)
        pc.send(sender_account_balance)
        pc.send(receiver_account_balance)
        pc.send(card)
        pc.send(receiver)
        
        transaction_recv = pc.recv()
        sender_account_balance_recv = pc.recv()
        receiver_account_balance_recv = pc.recv()
        card_recv = pc.recv()
        
        
        transaction = Transaction.query.filter_by(id=transaction_recv.id).first()
        sender_account_balance = Account_balance.query.filter_by(id=sender_account_balance_recv.id).first()
        #salje se na karticu
        if card:
            card = CreditCard.query.filter_by(id=card_recv.id).first()
            card.amount = card_recv.amount
            
        else:
            receiver_account_balance = Account_balance.query.filter_by(id=receiver_account_balance_recv.id).first()
            receiver_account_balance.amount = receiver_account_balance_recv.amount
            
        transaction.state = transaction_recv.state
        sender_account_balance.reserved = sender_account_balance_recv.reserved
        db.session.commit()
        
        lock.release()
    
def transaction_process(cc):
    while True:
        try:
            transaction = cc.recv()
            sender_account_balance = cc.recv()
            receiver_account_balance = cc.recv()
            card = cc.recv()
            receiver = cc.recv()
            
            sleep(60)
            #na karticu, ovde ima konverzija valute jer su na kartici dinari
            if card:
                if transaction.currency != "RSD":
                    value = get_value(transaction.currency, "RSD")
                    card.amount += value * transaction.amount
                else:
                    card.amount += transaction.amount
                    
                sender_account_balance.reserved = 0
                transaction.state = TransactionState.PROCESSED
                
                cc.send(transaction)
                cc.send(sender_account_balance)
                cc.send(receiver_account_balance)
                cc.send(card)
                
            else:
                #kod sender_account_balance je vec rezervisan iznos, sad treba dodati iznos na receiver_account_balance
                
                if receiver_account_balance:
                    receiver_account_balance.amount += transaction.amount
                else:
                    new_item = Account_balance(transaction.currency, transaction.amount)
                    new_item.user_id = receiver.id
                    receiver_account_balance = new_item
                
                sender_account_balance.reserved = 0
                transaction.state = TransactionState.PROCESSED
                
                cc.send(transaction)
                cc.send(sender_account_balance)
                cc.send(receiver_account_balance)
                cc.send(card)
                             
        except KeyboardInterrupt:
            break
