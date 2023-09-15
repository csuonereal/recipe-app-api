"""
Simple Tests    
"""

# SimpleTestCase: Does not use database
# TestCase: Uses database
from django.test import SimpleTestCase, TestCase
from app import calc


class CalcTests(SimpleTestCase):
    """Test the calc module"""

    def testAddNumbers(self):
        """Test adding numbers together"""
        res = calc.add(3, 8)
        self.assertEqual(res, 11)
