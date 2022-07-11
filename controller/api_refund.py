from flask import *
from model.refund import refund_model



api_refund=Blueprint("api_refund", __name__, template_folder="templates")




@api_refund.route("/api/refund",methods=["POST"])
def refund():
	refund_result = refund_model.refund()
	return refund_result