import sys
import unittest
from unittest.mock import MagicMock

# Apply mocks as requested
sys.modules['google'] = MagicMock()
sys.modules['google.generativeai'] = MagicMock()
sys.modules['pypdf'] = MagicMock()
sys.modules['docx'] = MagicMock()

import classify_proposals

class TestClassify(unittest.TestCase):
    def test_classify_heuristic(self):
        result = classify_proposals.classify_file("Grant-form-2025-V2C1.pdf")
        self.assertIn("Flex (Type 2)", result)
        result = classify_proposals.classify_file("SBIR-STTR-RFP-V26.pdf")
        self.assertIn("Flex (Type 2)", result)

if __name__ == '__main__':
    unittest.main()
