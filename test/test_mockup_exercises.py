import unittest
from src.mockup_exercises import *
from unittest import TestCase
from unittest.mock import patch, mock_open


class TestDataFetcher(unittest.TestCase):
    """
    Data fetcher unittest class
    """

    @patch("src.mockup_exercises.requests.get")
    def test_fetch_data_from_api_success(self, mock_get):
        """
        Success case.
        """
        # Set up the mock response
        mock_get.return_value.json.return_value = {"key": "value"}

        # Call the function under test
        result = fetch_data_from_api("https://api.example.com/data")

        # Assert that the function returns the expected result
        self.assertEqual(result, {"key": "value"})

        # Assert that requests.get was called with the correct URL
        mock_get.assert_called_once_with("https://api.example.com/data", timeout=10)

class TestReadFromFile(unittest.TestCase):
    """
    Read data from a file
    """
    @patch("builtins.open", new_callable=mock_open, read_data="Hola mundo")
    def read_data_from_file_success(self, mock_file):
        result = read_data_from_file("archivo.txt")
        assert result == "Hola, mundo"
        mock_file.assert_called_once_with("archivo.txt", encoding="utf-8")

    def test_read_data_from_file_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            read_data_from_file("archivo_inexistente.txt")

class TestExecuteCommand(unittest.TestCase):
    """
    Execute a command in a subprocess
    """

    @patch('subprocess.run')
    def test_execute_command_valid(self, mock_run):
        mock_run.return_value.stdout = 'Hello World\n'
        
        command = ['echo', 'Hello World']
        result = execute_command(command)
        
        self.assertEqual(result, 'Hello World\n')
        mock_run.assert_called_once_with(command, capture_output=True, check=False, text=True)

    @patch('subprocess.run')
    def test_execute_command_invalid(self, mock_run):
        mock_run.side_effect = subprocess.CalledProcessError(1, 'non_existing_command')
        
        command = ['non_existing_command']
        
        with self.assertRaises(subprocess.CalledProcessError):
            execute_command(command)
        mock_run.assert_called_once_with(command, capture_output=True, check=False, text=True)

class TestPerformActionBasedOnTime(unittest.TestCase):
    """
    Perform an action based on the current time.
    """
    
    @patch('time.time')
    def test_action_a_when_time_less_than_10(self, mock_time):
        mock_time.return_value = 5
        result = perform_action_based_on_time()
        self.assertEqual(result, "Action A")

    @patch('time.time')
    def test_action_b_when_time_10_or_more(self, mock_time):
        mock_time.return_value = 15
        result = perform_action_based_on_time()
        self.assertEqual(result, "Action B")