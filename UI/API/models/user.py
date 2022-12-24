from marshmallow import Schema, fields, post_load

class User():
    def __init__(self, name, last_name, address, city, country, tel_number, email_address, password, id = -1):
        self.id = id
        self.name = name
        self.last_name = last_name
        self.address = address
        self.city = city
        self.country = country
        self.tel_number = tel_number
        self.email_address = email_address
        self.password = password
        
# serijalizuje i deserijalizuje objekte 
class UserSchema(Schema):
    id = fields.Number()
    name = fields.String()
    last_name = fields.String()
    address = fields.String()
    city = fields.String()
    country = fields.String()
    tel_number = fields.String()
    email_address = fields.Email()
    password = fields.String()

    @post_load
    def make_user(self,data,**kwargs):
        return User(**data)