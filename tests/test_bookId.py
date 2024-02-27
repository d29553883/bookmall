import pytest
from model.bookId import BookIdModel


bookid_model = BookIdModel()
@pytest.mark.parametrize("book_id", [309, 513])
def test_searchid(book_id):
  book_info, _= bookid_model.searchid(book_id)
  assert isinstance(book_info, dict)
  assert "bookid" in book_info
  assert "author" in book_info
  assert isinstance(book_info["data"], list)
