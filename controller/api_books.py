from flask import *
from model.books import books_model



api_books=Blueprint("api_books", __name__, template_folder="templates")


@api_books.route("/api/books")
def books():
	result = books_model.books()
	return result	