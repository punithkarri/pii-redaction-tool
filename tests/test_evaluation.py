import unittest
import sys
import os
import math

# Put project root in path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from evaluation.evaluate import calculate_metrics

class TestEvaluation(unittest.TestCase):
    def test_calculate_metrics_perfect(self):
        # 10 TP, 0 FP, 0 FN, 10 TN
        precision, recall, accuracy = calculate_metrics(10, 0, 0, 10)
        self.assertEqual(precision, 1.0)
        self.assertEqual(recall, 1.0)
        self.assertEqual(accuracy, 1.0)

    def test_calculate_metrics_imperfect(self):
        # 8 TP, 2 FP, 4 FN, 6 TN
        # Precision = 8 / 10 = 0.8
        # Recall = 8 / 12 = 0.6666...
        # Accuracy = 14 / 20 = 0.7
        precision, recall, accuracy = calculate_metrics(8, 2, 4, 6)
        self.assertAlmostEqual(precision, 0.8)
        self.assertAlmostEqual(recall, 2/3)
        self.assertAlmostEqual(accuracy, 0.7)

    def test_division_by_zero_handling(self):
        # 0 TP, 0 FP, 0 FN, 10 TN
        # If there are no positive examples in ground truth, recall should be NaN (or handled safely)
        precision, recall, accuracy = calculate_metrics(0, 0, 0, 10)
        self.assertEqual(precision, 1.0)
        self.assertTrue(math.isnan(recall))
        self.assertEqual(accuracy, 1.0)

if __name__ == "__main__":
    unittest.main()
