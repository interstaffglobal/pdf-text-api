from flask import Flask, request, jsonify
import pdfplumber
import requests
import io

app = Flask(__name__)

@app.route("/extract-text", methods=["POST"])
def extract_text():
    data = request.get_json()
    pdf_url = data.get("url")

    if not pdf_url:
        return jsonify({"error": "No URL provided"}), 400

    try:
        response = requests.get(pdf_url)
        response.raise_for_status()
        with pdfplumber.open(io.BytesIO(response.content)) as pdf:
            text = ""
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return jsonify({"text": text.strip()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

