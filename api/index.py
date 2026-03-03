from flask import Flask, request, jsonify, send_from_directory
import os
import sys
import tempfile
from werkzeug.utils import secure_filename

# Add project root to sys.path to import classify_proposals
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from classify_proposals import classify_file

# Set the static folder to public
app = Flask(__name__, static_folder='../public', static_url_path='')

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/classify', methods=['POST'])
def classify():
    if 'files' not in request.files:
        return jsonify({"error": "No files provided"}), 400

    files = request.files.getlist('files')
    results = []

    # Create a temporary directory to save uploaded files
    with tempfile.TemporaryDirectory() as temp_dir:
        for file in files:
            if file.filename == '':
                continue

            filename = secure_filename(file.filename)
            filepath = os.path.join(temp_dir, filename)
            file.save(filepath)

            try:
                classification = classify_file(filepath)
                # Determine type for frontend coloring
                type_category = "flex" if "Flex" in classification else "respond"

                # Check if Gemini was likely used (simple check if API key exists)
                is_ai = bool(os.environ.get("GEMINI_API_KEY"))

                results.append({
                    "filename": filename,
                    "classification": classification,
                    "type": type_category,
                    "ai_powered": is_ai
                })
            except Exception as e:
                results.append({
                    "filename": filename,
                    "classification": "Error processing file",
                    "type": "error"
                })

    return jsonify({"results": results})

if __name__ == '__main__':
    app.run(debug=os.environ.get('FLASK_DEBUG', 'False').lower() in ['true', '1', 't'])
