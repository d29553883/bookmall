from flask import *
from model.recomment import recomment_model



api_recomment=Blueprint("api_recomment", __name__, template_folder="templates")


@api_recomment.route('/api/recomment' ,methods=['POST'])
def input_message():
	meggage_result = recomment_model.input_message()
	return meggage_result	