"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import secrets
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from jwt.exceptions import ExpiredSignatureError
from flask_jwt_extended import  JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_bcrypt import Bcrypt
import logging



api = Blueprint('api', __name__)
# Allow CORS requests to this API
CORS(api)

app=Flask(__name__)
secret_key=secrets.token_hex(32)
app.config["JWT_SECRET_KEY"] = secret_key
jwt=JWTManager(app)
bcrypt=Bcrypt(app)



@api.route('/hello', methods=['GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
        }
    
    return jsonify(response_body), 200


@api.route("/signup", methods=['POST'])
def signup():
    try:
        email=request.json.get("email")
        password=request.json.get("password")
        first_name=request.json.get("first_name")
        second_name=request.json.get("second_name")
        age_user=request.json.get("age_user")
        country_user=request.json.get("country_user")
        user_name=request.json.get("user_name")
        
        
        if not email or not first_name or not password or not second_name or not age_user or not country_user or not user_name:
            return jsonify({"error":"You are missing information, check it out"}),400
        
        existing_user=User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({"Error":"The email already exist"}),400

        password_hash=bcrypt.generate_password_hash(password).decode("utf-8")

        new_user=User(email=email,password=password_hash,first_name=first_name,second_name=second_name,age_user=age_user,country_user=country_user,user_name=user_name)
        
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message":"User created Succesfully!","user_created":user_name}),200


    except Exception as e:
        return jsonify({"Error:":"Error in user creation: "+str(e)}),400



@api.route("/token", methods=["POST"])
def get_token():
    try:
        email=request.json['email']
        password=request.json['password']
        if not email or not password:
            return jsonify({"error": "Email and password are required."}),400
    
        #this is another option
        # get_user_by_email=User.query.filter_by(email=email).first()

        get_user_by_email=User.query.filter_by(email=email).one()
        check_password_of_existing_user=get_user_by_email.password
        is_correctly_the_password=bcrypt.check_password_hash(check_password_of_existing_user,password)
        
        if is_correctly_the_password:
            user_id=get_user_by_email.id            
            access_token=create_access_token(identity=user_id)
            return jsonify({"accessToken":access_token}),200
        else:
            return jsonify ({"Error":"The password does not exist"}),401
    

    except Exception as e:
        return jsonify({"Error:": "The email is wrong "+ str(e)}),400
    

@api.route("/private")
@jwt_required()
def get_private():
    try:
        user_validation=get_jwt_identity()
        if user_validation:
            user=User.query.get(user_validation)
            return jsonify({"message":"Token is valid", "user_id":user.id,"email":user.email,"user_name":user.user_name}),200
    
    except ExpiredSignatureError:
        logging.warning("Token has expired")
        return jsonify({"Error":"Token has expired"}),401

    except Exception as e:
        logging.error("Token verification error: "+ str(e))
        return jsonify({"Error":"The token is invalid"+str(e)}),400


@api.route("/users")
def get_all_users():
    users=User.query.all()
    user_list=[]
    for user in users:
        user_dict={
            "id":user.id,
            "email":user.email,
            "password":user.password,
            "first_name":user.first_name,
            "second_name":user.second_name,
            "age_user":user.age_user,
            "country_user":user.country_user,
            "user_name":user.user_name
        }
        user_list.append(user_dict)
    
    return jsonify(user_list),200

