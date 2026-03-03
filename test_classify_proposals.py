import os
import sys
from unittest.mock import MagicMock, patch

# Mock out external dependencies before importing the module under test
sys.modules['google.generativeai'] = MagicMock()
sys.modules['google'] = MagicMock()
sys.modules['pypdf'] = MagicMock()
sys.modules['docx'] = MagicMock()

import classify_proposals

def test_classify_with_gemini_no_api_key():
    # Ensure GEMINI_API_KEY is not in the environment
    with patch.dict(os.environ, {}, clear=True):
        result = classify_proposals.classify_with_gemini("Sample text")
        assert result is None

@patch('classify_proposals.genai')
def test_classify_with_gemini_success(mock_genai):
    # Setup mock response
    mock_model = MagicMock()
    mock_response = MagicMock()
    mock_response.text = "Flex (Type 2)  \n" # Test stripping
    mock_model.generate_content.return_value = mock_response
    mock_genai.GenerativeModel.return_value = mock_model

    with patch.dict(os.environ, {"GEMINI_API_KEY": "test_key"}):
        result = classify_proposals.classify_with_gemini("Sample text")

        # Verify API configuration
        mock_genai.configure.assert_called_once_with(api_key="test_key")

        # Verify model initialization
        mock_genai.GenerativeModel.assert_called_once_with("gemini-1.5-flash")

        # Verify content generation
        prompt_call_arg = mock_model.generate_content.call_args[0][0]
        assert "Document Text:\nSample text" in prompt_call_arg

        # Verify return value
        assert result == "Flex (Type 2)"

@patch('classify_proposals.genai')
def test_classify_with_gemini_exception(mock_genai):
    # Setup mock to raise exception
    mock_model = MagicMock()
    mock_model.generate_content.side_effect = Exception("API failure")
    mock_genai.GenerativeModel.return_value = mock_model

    with patch.dict(os.environ, {"GEMINI_API_KEY": "test_key"}):
        result = classify_proposals.classify_with_gemini("Sample text")

        # Verify it handled the exception and returned None
        assert result is None
