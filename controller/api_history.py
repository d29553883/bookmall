from flask import *
from model.history import history_model

api_history=Blueprint("api_history", __name__, template_folder="templates")

@api_history.route('/api/hidtory', methods=['GET'])
def history():
	result = history_model.history()
	return result	
