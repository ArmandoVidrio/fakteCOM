import unittest
from unittest.mock import patch
from bookstore import Book, BookStore, main


class TestBook(unittest.TestCase):
    def test_book_display(self):
        book = Book('x_title', 'x_author', 4.99, 10)
        with patch('builtins.print') as mock_print:
            book.display()
        mock_print.assert_any_call('Title: x_title')
        mock_print.assert_any_call('Author: x_author')
        mock_print.assert_any_call('Price: $4.99')
        mock_print.assert_any_call('Quantity: 10')


class TestBookStore(unittest.TestCase):
    def test_add_book(self):
        store = BookStore()
        book = Book('x_title', 'x_author', 4.99, 10)
        with patch('builtins.print') as mock_print:
            store.add_book(book)
        self.assertIn(book, store.books)
        mock_print.assert_called_once_with("Book 'x_title' added to the store.")

    def test_search_book_found(self):
        store = BookStore()
        book = Book('x_title', 'x_author', 4.99, 10)
        store.books.append(book)
        with patch('builtins.print') as mock_print:
            store.search_book('x_title')
        mock_print.assert_any_call("Found 1 book(s) with title 'x_title':")
        mock_print.assert_any_call('Title: x_title')
        mock_print.assert_any_call('Author: x_author')

    def test_search_book_not_found(self):
        store = BookStore()
        with patch('builtins.print') as mock_print:
            store.search_book('unknown')
        mock_print.assert_called_once_with("No book found with title 'unknown'.")

    def test_display_books_empty(self):
        store = BookStore()
        with patch('builtins.print') as mock_print:
            store.display_books()
        mock_print.assert_called_once_with('No books in the store.')

    def test_display_books_with_books(self):
        store = BookStore()
        book = Book('x_title', 'x_author', 4.99, 10)
        store.books.append(book)
        with patch('builtins.print') as mock_print:
            store.display_books()
        mock_print.assert_any_call('Books available in the store:')
        mock_print.assert_any_call('Title: x_title')


class TestMainFunction(unittest.TestCase):
    @patch('builtins.input', side_effect=['2', 'x_title', '4'])
    @patch('builtins.print')
    def test_main_search_book(self, mock_print, mock_input):
        with patch('bookstore.BookStore.search_book') as mock_search:
            main()
            mock_search.assert_called_once_with('x_title')
        mock_print.assert_any_call('Exiting...')

    @patch('builtins.input', side_effect=['3', 'x_title2', 'x_author2', '10.0', '2', '4'])
    @patch('builtins.print')
    def test_main_add_book(self, mock_print, mock_input):
        main()
        mock_print.assert_any_call("Book 'x_title2' added to the store.")
        mock_print.assert_any_call('Exiting...')

    @patch('builtins.input', side_effect=['invalid', '4'])
    @patch('builtins.print')
    def test_main_invalid_choice(self, mock_print, mock_input):
        main()
        mock_print.assert_any_call('Invalid choice. Please try again.')
        mock_print.assert_any_call('Exiting...')
        self.assertGreaterEqual(mock_print.call_count, 2)


if __name__ == '__main__':
    unittest.main()
