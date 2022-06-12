from flask import *
import json
import requests
from cnxpool import cnxpool
import os



api_refund=Blueprint("api_refund", __name__, template_folder="templates")




@api_refund.route("/api/refund",methods=["POST"])
def refund():
	try:
		req = request.get_json()
		orderNumber = req["orderNumber"]
		cnx=cnxpool.get_connection()
		mycursor=cnx.cursor(buffered = True, dictionary = True)			
		partnerKey = os.getenv("PARTNERKEY")
		mycursor.execute("SELECT rec_trade_id FROM orderhistory WHERE number = %s" ,(orderNumber,))
		myresult = mycursor.fetchall()
		rec_trade_id = myresult[0]["rec_trade_id"]
		header = {
		"content-type": "application/json",
		"x-api-key": partnerKey
		}
		my_data = {
			"partner_key": partnerKey,
			"rec_trade_id": rec_trade_id,
		}
		response = requests.post('https://sandbox.tappaysdk.com/tpc/transaction/refund', json = my_data, headers=header)
		data = response.json()
		print(data)
		status = data["status"]
		if status == 0:
			return jsonify({
				"data": {
					"status":status,
					"message": "退款成功"
				}
			})
		else:
			return jsonify({
				"data": {
					"status":status,
					"message": "退款失敗"
				}
			})
	except:
		return jsonify({
			"error": True,
			"message": "伺服器內部錯誤"
		}),500	
	finally:
		if cnx.in_transaction:
			cnx.rollback()
		cnx.close()