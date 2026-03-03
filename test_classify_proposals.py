import sys
from unittest.mock import MagicMock, patch

# Mock dependencies before importing classify_proposals
sys.modules['google'] = MagicMock()
sys.modules['google.generativeai'] = MagicMock()
sys.modules['pypdf'] = MagicMock()
sys.modules['docx'] = MagicMock()

from classify_proposals import extract_text

@patch('classify_proposals.PdfReader')
def test_extract_text_pdf_error(mock_pdf_reader):
    # Setup mock to raise an exception when called
    mock_pdf_reader.side_effect = Exception("Mocked PDF error")

    # Call extract_text with a .pdf file
    result = extract_text("test.pdf")

    # Assert it returns empty string and catches the error
    assert result == ""
    mock_pdf_reader.assert_called_once_with("test.pdf")

@patch('classify_proposals.Document')
def test_extract_text_docx_error(mock_document):
    # Setup mock to raise an exception when called
    mock_document.side_effect = Exception("Mocked DOCX error")

    # Call extract_text with a .docx file
    result = extract_text("test.docx")

    # Assert it returns empty string and catches the error
    assert result == ""
    mock_document.assert_called_once_with("test.docx")

@patch('classify_proposals.PdfReader')
def test_extract_text_pdf_not_found(mock_pdf_reader):
    # Simulate FileNotFoundError specifically (common when file doesn't exist)
    mock_pdf_reader.side_effect = FileNotFoundError("No such file or directory: 'missing.pdf'")

    # Call extract_text with a .pdf file that doesn't exist
    result = extract_text("missing.pdf")

    # Assert it returns empty string and handles the FileNotFoundError
    assert result == ""
    mock_pdf_reader.assert_called_once_with("missing.pdf")
