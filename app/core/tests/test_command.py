"""  
Test custom Django management commands
"""


from unittest.mock import patch
from psycopg2 import OperationalError as Psycopg2Error
# allows us to call the command from the code
from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase


# patch decorator replaces the function with a mock function
# base command has a check method
@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """Test commands"""

    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for database if database is available"""
        patched_check.return_value = True
        call_command('wait_for_db')

        # check if the check method was called with the database as an argument
        patched_check.assert_called_once_with(databases=['default'])

    # what should happen if the database is not available
    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):#order is important, en aşağıda olanı en solda olmalı
        """Test waiting for database when getting OperationalError"""
        
        #we used patched_sleep because we don't want to wait for 1 seconds
        # way that you make it raise an error instead of actually pretending that it is available, you can use side effect
        # first two times it is called, it will raise an Psycopg2Error, and then we raise 3 OperationalErrors, and then we return True
        patched_check.side_effect = [
            Psycopg2Error]*2+[OperationalError]*3+[True]

        call_command('wait_for_db')
        self.assertEqual(patched_check.call_count, 6)
        # similar to above assertion but it checks called with database argument
        patched_check.assert_called_with(databases=['default'])


"""
Function Arguments:
When you use the patch decorator on a function or method, the mock object is automatically passed as an argument to that function or method. In this case, the test function test_wait_for_db_ready receives an additional argument (patched_check). This argument is the mock object for whatever you patched with the decorator. The name patched_check is just a convention here; you could name it anything else, but it's clear and descriptive in this context.
"""


"""
Imports:

patch from unittest.mock: This is used to replace the real function/method with a mock (a fake version) for testing purposes.
OperationalError from both psycopg2 and django.db.utils: These are database-related errors which might be raised when the database isn't ready.
call_command from django.core.management: This lets you programmatically call management commands.
SimpleTestCase from django.test: It provides a framework for unit tests in Django.


Mocking:

The @patch('core.management.commands.wait_for_db.Command.check') is a decorator that will replace the check method of the Command class (located in core.management.commands.wait_for_db) with a mock for the duration of the tests in the CommandTests class.

CommandTests class:

test_wait_for_db_ready: This test is checking if, when the database is available (i.e., the mocked check method returns True), the custom management command (wait_for_db) is called with the correct database argument. It ensures that our management command behaves correctly when the database is ready.
"""


"""  
How the Test Works:

The test sets the return value of the mocked check method to True, simulating a scenario where the database is ready.
The call_command('wait_for_db') line simulates the execution of the management command.
The patched_check.assert_called_once_with(database=['default']) line asserts that the mocked check method was called exactly once with the specified arguments (here, a list containing the string 'default').

Notes:

The actual logic for the check method and the real functionality for waiting for the database isn't present in the provided code. This is expected since the main aim was to demonstrate how to test a Django command and not to implement the command's full functionality.
The comment “Django command to wait for database to be available” hints at the intended purpose of the Command class but the real implementation isn’t shown.
Overall, the test checks if the correct functions and methods are called with the expected arguments, but the full functionality of the command is not yet implemented.

"""
