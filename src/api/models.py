from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name=db.Column(db.String(120),unique=False,nullable=False)
    second_name=db.Column(db.String(120),unique=False,nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    user_name= db.Column(db.String(120),unique=False,nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    age_user=db.Column(db.Integer)
    country_user=db.Column(db.String(120),unique=False, nullable=False)
    


    def __repr__(self):
        return f'<User {self.user_name}>'


    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "first_name":self.first_name,
            "password":self.password,
            "second_name":self.second_name,
            "age_user":self.age_user,
            "country_user":self.country_user,
            "user_name":self.user_name
        
            # do not serialize the password, its a security breach
        }