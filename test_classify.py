import unittest
from unittest.mock import patch, MagicMock
from classify_proposals import Palette, classify_file

class TestClassification(unittest.TestCase):
    def test_palette_exists(self):
        self.assertTrue(hasattr(Palette, 'FLEX'))
        self.assertTrue(hasattr(Palette, 'RESPOND'))

    @patch('classify_proposals.extract_text')
    @patch('os.path.basename')
    def test_classify_flex_heuristic(self, mock_basename, mock_extract_text):
        # Simulate a Flex document
        mock_basename.return_value = "guidelines.pdf"
        mock_extract_text.return_value = "request for proposal project overview"

        result = classify_file("dummy/path/guidelines.pdf")
        self.assertIn("Flex", result)

    @patch('classify_proposals.extract_text')
    @patch('os.path.basename')
    def test_classify_respond_heuristic(self, mock_basename, mock_extract_text):
        # Simulate a Respond document
        mock_basename.return_value = "application_form.pdf"
        mock_extract_text.return_value = "application template please note that a session will time out"

        result = classify_file("dummy/path/application_form.pdf")
        self.assertIn("Respond", result)

if __name__ == "__main__":
    unittest.main()
