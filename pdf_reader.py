import fitz   # PyMuPDF


def extract_text_from_pdf(pdf_file):

    text = ""

    # Open PDF
    document = fitz.open(stream=pdf_file.read(), filetype="pdf")


    # Read every page
    for page in document:

        text += page.get_text()


    return text
