from flask import *
from model.bookId import bookId_model


api_book_bookId=Blueprint("api_book_bookId", __name__, template_folder="templates")


@api_book_bookId.route("/api/book/<bookId>")
def searchid(bookId):
	result = bookId_model.searchid(bookId)
	return result		