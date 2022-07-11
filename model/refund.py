from flask import *
import json
import requests
from cnxpool import cnxpool
import os


class RefundModel:
  def refund(self):
    cnx=cnxpool.get_connection()
    mycursor=cnx.cursor(buffered = True, dictionary = True)		
    try:
      req = request.get_json()
      orderNumber = req["orderNumber"]	
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
      mycursor.close()
      cnx.close()


refund_model = RefundModel()