import sys
from unittest.mock import MagicMock, patch
import pytest

# Mock missing dependencies
sys.modules['google'] = MagicMock()
sys.modules['google.generativeai'] = MagicMock()
sys.modules['pypdf'] = MagicMock()
sys.modules['docx'] = MagicMock()

# Mock flask modules
class MockFlaskApp:
    def route(self, *args, **kwargs):
        def decorator(f):
            # Do NOT wrap the function, just return it so it can be called
            return f
        return decorator
    def run(self, *args, **kwargs):
        pass

mock_flask = MagicMock(return_value=MockFlaskApp())
mock_jsonify = MagicMock(side_effect=lambda x: x)
mock_request = MagicMock()
mock_send_from_directory = MagicMock()

# Instead of relying on a real Flask app which requires real Flask,
# we can just test the `classify()` function itself by mocking the request object
sys.modules['flask'] = MagicMock(
    Flask=mock_flask,
    jsonify=mock_jsonify,
    request=mock_request,
    send_from_directory=mock_send_from_directory
)

mock_secure_filename = MagicMock(side_effect=lambda x: x)
sys.modules['werkzeug'] = MagicMock()
sys.modules['werkzeug.utils'] = MagicMock(secure_filename=mock_secure_filename)

import api.index

# Make sure the imported functions point to our mocks
api.index.jsonify = mock_jsonify
api.index.request = mock_request
api.index.secure_filename = mock_secure_filename

@patch('api.index.classify_file')
def test_classify_error_path(mock_classify_file):
    """Test the /api/classify endpoint when classify_file raises an Exception."""
    # Setup mock to raise an exception
    mock_classify_file.side_effect = Exception("Mocked failure")

    # Mock request object
    mock_file = MagicMock()
    mock_file.filename = 'dummy.pdf'

    # We need a dictionary-like object that also has a getlist method
    class MockFiles(dict):
        def getlist(self, key):
            return [mock_file] if key == 'files' else []

    api.index.request.files = MockFiles({'files': mock_file})

    # Call the function directly
    result = api.index.classify()

    # Assertions
    assert 'results' in result, f"Expected 'results' in {result}"
    assert len(result['results']) == 1

    res = result['results'][0]
    assert res['filename'] == 'dummy.pdf'
    assert res['classification'] == 'Error processing file'
    assert res['type'] == 'error'
