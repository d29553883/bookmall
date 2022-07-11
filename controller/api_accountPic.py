from flask import *
from model.accountPic import accountPic_model


api_accountPic=Blueprint("api_accountPic", __name__, template_folder="templates")


@api_accountPic.route('/api/accountPic' ,methods=['POST'])
def update_pic():
	update_pic_result = accountPic_model.update_pic()
	return update_pic_result	



@api_accountPic.route('/api/accountPic', methods=['GET'])
def get_pic():
	get_result = accountPic_model.get_pic()
	return get_result