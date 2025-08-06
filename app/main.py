from flask import Flask, request, jsonify
from parser_engine import process_document
import os
import traceback 

app = Flask(__name__)

@app.route("/parse", methods=["POST"])
def parse():
    file = request.files.get('file')
    template_name = request.form.get('template')

    if not file or not template_name:
        return {"error": "File and template name are required."}, 400

    upload_folder = os.path.join(os.getcwd(), "uploads")
    os.makedirs(upload_folder, exist_ok=True)
    filepath = os.path.join(upload_folder, file.filename)

    try:
        file.save(filepath)
    except Exception as e:
        return {"error": f"Failed to save file: {str(e)}"}, 500

    try:
        data = process_document(filepath, template_name)
        return jsonify(data)
    except Exception as e:
        traceback.print_exc()  # 👈 This prints the full stack trace in your terminal
        return {"error": f"Parsing failed: {str(e)}"}, 500

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)