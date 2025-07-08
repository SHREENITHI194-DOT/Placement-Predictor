from flask import Flask, render_template, request
import os
import fitz  # PyMuPDF
from app.predictor import predict_placement  # adjust import if needed

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Ensure the uploads folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Extract text from PDF using PyMuPDF
def extract_text_from_pdf(file_path):
    text = ""
    try:
        doc = fitz.open(file_path)
        for page in doc:
            text += page.get_text()
        doc.close()
    except Exception as e:
        text = f"Error reading PDF: {e}"
    return text

@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    resume_text = ""
    
    if request.method == "POST":
        # Form inputs
        cgpa = float(request.form["cgpa"])
        iq = int(request.form["iq"])
        extra = int(request.form["extra_courses"])
        
        # Run prediction
        prediction = predict_placement(cgpa, iq, extra)
        result = "✅ Placed" if prediction == 1 else "❌ Not Placed"
        
        # Handle resume upload
        resume = request.files.get("resume")
        if resume and resume.filename.endswith(".pdf"):
            resume_path = os.path.join(app.config["UPLOAD_FOLDER"], resume.filename)
            resume.save(resume_path)
            resume_text = extract_text_from_pdf(resume_path)
        else:
            resume_text = "Invalid or no PDF uploaded."

    return render_template("index.html", result=result, resume_text=resume_text)

if __name__ == "__main__":
    app.run(debug=True)
