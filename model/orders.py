from flask import *
import json
import requests
from cnxpool import cnxpool
from datetime import datetime
import os


class OrdersModel:
  def createBook(self):
    try:
      if session != {}:
        cnx=cnxpool.get_connection()
        mycursor=cnx.cursor()			
        partnerKey = os.getenv("PARTNERKEY")
        req = request.get_json()
        prime = req["prime"]
        email = req["email"]
        phone = req["phone"]
        address = req["address"]
        bookNameList = req["bookName"]
        countList = req["count"]
        list_combined = list(zip(bookNameList, countList))
        sql = "SELECT name,author,price from cart WHERE email = %s" 
        adr = (email,)
        mycursor.execute(sql, adr)
        myresult = mycursor.fetchall()
        pricetotal = 0
        for i in myresult:	
          price	= i[2]
          pricetotal += price
        number = datetime.now().strftime('%Y%m%d%H%M%S')
        username = req["username"]
        if phone !="":
          header = {
            "content-type": "application/json",
            "x-api-key": partnerKey
          }
          my_data = {
              "prime": prime,
              "partner_key": partnerKey,
              "merchant_id": "d29553883_CTBC",
              "details":"TapPay Test",
              "amount": pricetotal,
              "cardholder": {
                "phone_number": phone,
                "name": username,
                "email": email,
              },
              "remember": True
            }
          response = requests.post('https://sandbox.tappaysdk.com/tpc/payment/pay-by-prime', json = my_data, headers=header)
          data = response.json()
          status = data["status"]
          rec_trade_id = data["rec_trade_id"]
          if status == 0:
            for i in myresult:	
              name = i[0]
              author = i[1]
              price	= i[2]
              sql2 = ("INSERT INTO orderhistory(number,name,author,price,username,email,phone,address,status,rec_trade_id)" 
              " VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")		
              adr2 = (number,name,author,price,username,email,phone,address,status,rec_trade_id)
              mycursor.execute(sql2,adr2)
              cnx.commit()
              mycursor.execute("DELETE FROM cart where email= %s",(email,))
              cnx.commit()
            #取商品數量
            for i in list_combined:
              sql = "update orderhistory set count = %s where name = %s AND number = %s"
              adr = (i[1],i[0],number)
              mycursor.execute(sql,adr)
              cnx.commit()
              sql2 = "update books set stock = stock - %s where name = %s"
              adr2 = (i[1],i[0])
              mycursor.execute(sql2,adr2)
              cnx.commit()						
            return jsonify({
              "data": {
                "number": number,
                "payment": {
                "status":status,
                "message": "付款成功"
              }
              }
            })
          else:
            sql2 = ("INSERT INTO orderhistory(number,name,author,price,username,email,phone,address,status)" 
            " VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)")		
            adr2 = (number,name,author,price,username,email,phone,address,status)
            mycursor.execute(sql2,adr2)
            cnx.commit()
            return jsonify({
              "data": {
                "number": number,
                "payment": {
                "status":status,
                "message": "付款失敗"
              }
              }
            })					
        else:
          return jsonify({
            "error": True,
            "message": "建立失敗，資料沒輸入"
          }),400				
      else:
        return jsonify({
          "error": True,
          "message": "未登入系統，拒絕存取"
        }),403
    except:
      return jsonify({
        "error": True,
        "message": "伺服器內部錯誤"
      }),500	
    finally:
      if cnx.in_transaction:
        cnx.rollback()
      cnx.close()



  def thankyouPage(self,orderNumber):
    try:
      if session != {}:
        cnx=cnxpool.get_connection()
        mycursor=cnx.cursor()
        sql = "SELECT number FROM orderhistory WHERE number = %s" 
        adr = (orderNumber,)
        mycursor.execute(sql, adr)
        myresult = mycursor.fetchall()
        x = myresult[0]
        x.__str__()
        number = x[0]
        return jsonify({
          "data":{"number":number}
        })
      else:
          return jsonify({
            "error": True,
            "message": "未登入系統，拒絕存取"
          }),403
    finally:
      if cnx.in_transaction:
        cnx.rollback()
      cnx.close()


orders_model = OrdersModel()