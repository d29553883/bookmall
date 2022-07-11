from flask import *
from model.orders import orders_model


api_orders=Blueprint("api_orders", __name__, template_folder="templates")


@api_orders.route("/api/orders",methods=["POST"])
def createBook():
	createBook_result = orders_model.createBook()
	return createBook_result



@api_orders.route("/api/orders/<orderNumber>")
def thankyouPage(orderNumber):
	thankyouPage_result = orders_model.thankyouPage(orderNumber)
	return thankyouPage_result