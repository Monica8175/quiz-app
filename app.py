from flask import Flask, render_template, request, jsonify
from pdf_reader import extract_text_from_pdf
from quiz_generator import generate_quiz

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_pdf():
    if "pdf" not in request.files:
        return jsonify({"error": "No PDF uploaded"})

    pdf = request.files["pdf"]
    text = extract_text_from_pdf(pdf)
    quiz = generate_quiz(text)

    return jsonify({
        "message": "Quiz generated successfully 🎉",
        "quiz": quiz
    })

if __name__ == "__main__":
    app.run(debug=True)
