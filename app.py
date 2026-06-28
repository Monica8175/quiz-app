from flask import Flask, render_template, request, jsonify
from pdf_reader import extract_text_from_pdf


app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")



@app.route("/upload", methods=["POST"])
def upload_pdf():

    pdf = request.files["pdf"]


    text = extract_text_from_pdf(pdf)


    return jsonify({

        "message":"PDF extracted successfully ✅",

        "content": text[:1000]

    })



if __name__ == "__main__":
    app.run(debug=True)
