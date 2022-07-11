from flask import *
from model.cartCount import cartCount_model


api_cartCount=Blueprint("api_cartCount", __name__, template_folder="templates")


@api_cartCount.route("/api/cartCount")
def cartCount():
	result = cartCount_model.cartCount()
	return result		


