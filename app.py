from flask import Flask, render_template, request, jsonify
import fitz   # PyMuPDF


app = Flask(__name__)


# Open frontend
@app.route("/")
def home():
    return render_template("index.html")


# Receive PDF
@app.route("/upload", methods=["POST"])
def upload_pdf():

    pdf_file = request.files["pdf"]

    # Open PDF
    document = fitz.open(pdf_file)

    text = ""

    # Extract text from all pages
    for page in document:
        text += page.get_text()


    return jsonify({
        "status": "success",
        "message": "PDF uploaded successfully ✅",
        "text": text[:1000]
    })



if __name__ == "__main__":
    app.run(debug=True)
