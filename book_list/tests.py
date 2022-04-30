from django.test import TestCase
from models import Book
# Create your tests here.


class BookModelTestCase(TestCase):
    def setUp(self):
        self.book = Book(title="Xx", author="Yy Zz", pub_date=2010, isbn="5448855546663",
                         pages=450, cover_link='https://tvn24.pl/', language='eng')

    def test_book_creation(self):
        self.book.save()
        self.assertIsNone(self.id)
