from flask import *
from model.user import user_model

api_user=Blueprint("api_user", __name__, template_folder="templates")




@api_user.route("/api/user")
def memberinfo():
	result = user_model.memberinfo()
	return result		  

@api_user.route("/api/user", methods=["POST"])
def signup():
	signup_result = user_model.signup()
	return signup_result	

@api_user.route("/api/user", methods=["PATCH"])
def signin():
	signin_result = user_model.signin()
	return signin_result

@api_user.route("/api/user", methods=["DELETE"])
def signout():
	signout_result = user_model.signout()
	return signout_result