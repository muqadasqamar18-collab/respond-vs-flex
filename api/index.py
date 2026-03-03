from flask import Flask, request, jsonify, send_from_directory
import os
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from werkzeug.utils import secure_filename

# Add project root to sys.path to import classify_proposals
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from classify_proposals import classify_file

# Set the static folder to public
app = Flask(__name__, static_folder='../public', static_url_path='')

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

def process_single_file(file, temp_dir, is_ai):
    if file.filename == '':
        return None

    filename = secure_filename(file.filename)
    filepath = os.path.join(temp_dir, filename)
    file.save(filepath)

    try:
        classification = classify_file(filepath)
        # Determine type for frontend coloring
        type_category = "flex" if "Flex" in classification else "respond"

        return {
            "filename": filename,
            "classification": classification,
            "type": type_category,
            "ai_powered": is_ai
        }
    except Exception as e:
        return {
            "filename": filename,
            "classification": "Error processing file",
            "type": "error"
        }

@app.route('/api/classify', methods=['POST'])
def classify():
    if 'files' not in request.files:
        return jsonify({"error": "No files provided"}), 400

    files = request.files.getlist('files')
    results = []

    # Check if Gemini was likely used (simple check if API key exists)
    is_ai = bool(os.environ.get("GEMINI_API_KEY"))

    # Create a temporary directory to save uploaded files
    with tempfile.TemporaryDirectory() as temp_dir:
        # Using a thread pool to process files concurrently
        # The number of workers is dynamically determined based on CPU count, with a fallback
        max_workers = min(32, (os.cpu_count() or 1) + 4)
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(process_single_file, file, temp_dir, is_ai) for file in files]
            for future in futures:
                result = future.result()
                if result is not None:
                    results.append(result)

    return jsonify({"results": results})

if __name__ == '__main__':
    app.run(debug=True)
