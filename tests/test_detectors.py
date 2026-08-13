import unittest
import sys
import os

# Put project root in path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.pii_detector import PIIDetector

class TestDetectors(unittest.TestCase):
    def setUp(self):
        self.detector = PIIDetector()

    def test_email_detection(self):
        text = "Please reach out to john.doe@gmail.com for questions."
        matches = self.detector.detect_emails(text)
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0]["original"], "john.doe@gmail.com")
        self.assertEqual(matches[0]["type"], "EMAIL")

    def test_phone_detection(self):
        text = "Call us at +91 9876543210 for details."
        matches = self.detector.detect_phone_numbers(text)
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0]["original"], "+91 9876543210")
        self.assertEqual(matches[0]["type"], "PHONE")

    def test_ssn_detection(self):
        # We need SSN context to detect SSN with high confidence
        text = "SSN: 123-45-6789 is my number."
        matches = self.detector.detect_ssns(text)
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0]["original"], "123-45-6789")
        self.assertEqual(matches[0]["type"], "SSN")

    def test_credit_card_detection(self):
        # Visa card that passes Luhn check
        text = "My card number is 4111 1111 1111 1111."
        matches = self.detector.detect_credit_cards(text)
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0]["original"], "4111 1111 1111 1111")
        self.assertEqual(matches[0]["type"], "CREDIT_CARD")

    def test_ip_detection(self):
        text = "The server is at 192.168.1.10."
        matches = self.detector.detect_ip_addresses(text)
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0]["original"], "192.168.1.10")
        self.assertEqual(matches[0]["type"], "IP_ADDRESS")

    def test_dob_detection(self):
        text = "My Date of Birth: 15/08/2000 is on a holiday."
        matches = self.detector.detect_dates_of_birth(text)
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0]["original"], "15/08/2000")
        self.assertEqual(matches[0]["type"], "DOB")

    def test_name_detection(self):
        text = "Contact Person: John Smith is here."
        matches = self.detector.detect_names(text)
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0]["original"], "John Smith")
        self.assertEqual(matches[0]["type"], "FULL_NAME")

    def test_company_detection(self):
        text = "We are hiring Example Technologies Limited for the audit."
        matches = self.detector.detect_company_names(text)
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0]["original"], "Example Technologies Limited")
        self.assertEqual(matches[0]["type"], "COMPANY")

    def test_address_detection(self):
        text = "The registered office is at 123 Example Road, Pune, Maharashtra - 411001 India."
        matches = self.detector.detect_addresses(text)
        self.assertEqual(len(matches), 1)
        self.assertTrue("411001" in matches[0]["original"])
        self.assertEqual(matches[0]["type"], "ADDRESS")

    def test_negatives(self):
        # These should NOT be detected as PII
        negative_texts = [
            "The year 2025 is next.",
            "The project will cost ₹7,100 million.",
            "Please turn to Page 123.",
            "Read the Risk Factors section.",
            "The Book Building Process is online.",
            "31/03/2025 is the end of the fiscal year.",
            "December 10, 2025"
        ]
        for t in negative_texts:
            matches = self.detector.detect_all(t)
            # Ensure none of the matches classify these negative cases as PII
            for m in matches:
                self.assertNotEqual(m["original"], "2025")
                self.assertNotEqual(m["original"], "₹7,100 million")
                self.assertNotEqual(m["original"], "Page 123")
                self.assertNotEqual(m["original"], "Risk Factors")
                self.assertNotEqual(m["original"], "Book Building Process")
                self.assertNotEqual(m["original"], "December 10, 2025")
                self.assertNotEqual(m["type"], "DOB") # ordinary dates should not be DOB

if __name__ == "__main__":
    unittest.main()
