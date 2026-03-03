import sys
from unittest.mock import MagicMock

# Module-level mocking to allow execution in environments where dependencies are missing
sys.modules['google'] = MagicMock()
sys.modules['google.generativeai'] = MagicMock()
sys.modules['pypdf'] = MagicMock()
sys.modules['docx'] = MagicMock()

import pytest
import classify_proposals

def test_extract_text_pdf(monkeypatch):
    """Test extracting text from a PDF with fewer than 5 pages."""
    mock_pdfreader = MagicMock()
    mock_reader = MagicMock()
    mock_pdfreader.return_value = mock_reader
    monkeypatch.setattr(classify_proposals, 'PdfReader', mock_pdfreader)

    mock_page1 = MagicMock()
    mock_page1.extract_text.return_value = "Page 1 text"
    mock_page2 = MagicMock()
    mock_page2.extract_text.return_value = "Page 2 text"
    mock_reader.pages = [mock_page1, mock_page2]

    text = classify_proposals.extract_text("test.pdf")

    assert "Page 1 text" in text
    assert "Page 2 text" in text
    mock_pdfreader.assert_called_once_with("test.pdf")

def test_extract_text_pdf_max_pages(monkeypatch):
    """Test that PDF extraction only reads up to 5 pages."""
    mock_pdfreader = MagicMock()
    mock_reader = MagicMock()
    mock_pdfreader.return_value = mock_reader
    monkeypatch.setattr(classify_proposals, 'PdfReader', mock_pdfreader)

    mock_pages = []
    for i in range(6):
        page = MagicMock()
        page.extract_text.return_value = f"Page {i+1} text"
        mock_pages.append(page)

    mock_reader.pages = mock_pages

    text = classify_proposals.extract_text("test.pdf")

    assert "Page 5 text" in text
    assert "Page 6 text" not in text

def test_extract_text_docx(monkeypatch):
    """Test extracting text from a DOCX with fewer than 50 paragraphs."""
    mock_document = MagicMock()
    mock_doc = MagicMock()
    mock_document.return_value = mock_doc
    monkeypatch.setattr(classify_proposals, 'Document', mock_document)

    mock_para1 = MagicMock()
    mock_para1.text = "Para 1 text"
    mock_para2 = MagicMock()
    mock_para2.text = "Para 2 text"
    mock_doc.paragraphs = [mock_para1, mock_para2]

    text = classify_proposals.extract_text("test.docx")

    assert "Para 1 text" in text
    assert "Para 2 text" in text
    mock_document.assert_called_once_with("test.docx")

def test_extract_text_docx_max_paras(monkeypatch):
    """Test that DOCX extraction only reads up to 50 paragraphs."""
    mock_document = MagicMock()
    mock_doc = MagicMock()
    mock_document.return_value = mock_doc
    monkeypatch.setattr(classify_proposals, 'Document', mock_document)

    mock_paras = []
    for i in range(55):
        para = MagicMock()
        para.text = f"Para {i+1} text"
        mock_paras.append(para)

    mock_doc.paragraphs = mock_paras

    text = classify_proposals.extract_text("test.docx")

    assert "Para 50 text" in text
    assert "Para 51 text" not in text

def test_extract_text_doc():
    """Test that older .doc files are ignored and return empty text."""
    text = classify_proposals.extract_text("test.doc")
    assert text == ""

def test_extract_text_exception(monkeypatch):
    """Test that exceptions during extraction are caught and return empty text."""
    mock_pdfreader = MagicMock()
    mock_pdfreader.side_effect = Exception("Test error")
    monkeypatch.setattr(classify_proposals, 'PdfReader', mock_pdfreader)

    text = classify_proposals.extract_text("error.pdf")
    assert text == ""

def test_extract_text_unknown_extension():
    """Test that an unknown extension returns an empty text."""
    text = classify_proposals.extract_text("test.txt")
    assert text == ""
