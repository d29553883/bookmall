from flask import *
from model.addCart import addCart_model



api_addCart=Blueprint("api_addCart", __name__, template_folder="templates")


@api_addCart.route("/api/addCart")
def check():
	get_result = addCart_model.check()
	return get_result				


@api_addCart.route("/api/addCart",methods=["POST"])
def addCart():
	add_result = addCart_model.addCart()
	return add_result				

@api_addCart.route("/api/addCart", methods=["DELETE"])
def deleteBook():
	delete_result = addCart_model.deleteBook()
	return delete_result		