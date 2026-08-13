import unittest
import sys
import os

# Put project root in path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.redactor import PIIRedactor

class TestRedaction(unittest.TestCase):
    def setUp(self):
        self.redactor = PIIRedactor()

    def test_consistent_mapping(self):
        name = "Sarthak Malvadkar"
        repl1 = self.redactor.get_replacement(name, "FULL_NAME")
        repl2 = self.redactor.get_replacement(name, "FULL_NAME")
        self.assertEqual(repl1, repl2)
        
        email = "cs.connect@kshinternational.com"
        repl_email1 = self.redactor.get_replacement(email, "EMAIL")
        repl_email2 = self.redactor.get_replacement(email, "EMAIL")
        self.assertEqual(repl_email1, repl_email2)

    def test_different_replacements(self):
        # Different values should get different replacements
        repl_a = self.redactor.get_replacement("Sarthak Malvadkar", "FULL_NAME")
        repl_b = self.redactor.get_replacement("Rajesh Kushal Hegde", "FULL_NAME")
        self.assertNotEqual(repl_a, repl_b)
        
        # Different PII types should get different replacements
        repl_c = self.redactor.get_replacement("+91 20 45053237", "PHONE")
        self.assertNotEqual(repl_a, repl_c)

    def test_no_original_pii_leak_in_replacements(self):
        name = "Sarthak Malvadkar"
        repl = self.redactor.get_replacement(name, "FULL_NAME")
        # The fake replacement should not contain the original name
        self.assertNotIn("Sarthak", repl)
        self.assertNotIn("Malvadkar", repl)

if __name__ == "__main__":
    unittest.main()
