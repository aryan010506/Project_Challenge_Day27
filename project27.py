import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import pdfplumber
import docx2txt
import nltk

nltk.download('punkt')

# -------------------------------
# Skills list
# -------------------------------
SKILLS = [
    "Python", "Java", "C++", "SQL", "Machine Learning",
    "Data Analysis", "Deep Learning", "NLP", "TensorFlow",
    "PyTorch", "Excel", "Power BI", "Tableau", "Communication",
    "Leadership", "Teamwork"
]

# -------------------------------
# Extract text from resume
# -------------------------------
def extract_text(file_path):
    if file_path.endswith('.pdf'):
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + " "
        return text
    elif file_path.endswith('.docx'):
        text = docx2txt.process(file_path)
        return text
    else:
        return None

# -------------------------------
# Extract skills
# -------------------------------
def extract_skills(text):
    text = text.replace('\n', ' ')
    tokens = nltk.word_tokenize(text)
    tokens = [token.lower() for token in tokens]
    found_skills = set()
    for skill in SKILLS:
        if skill.lower() in text.lower():
            found_skills.add(skill)
    return list(found_skills)

# -------------------------------
# GUI Functions
# -------------------------------
def upload_resume():
    file_path = filedialog.askopenfilename(
        title="Select Resume",
        filetypes=[("PDF files", "*.pdf"), ("Word files", "*.docx")]
    )
    if file_path:
        text = extract_text(file_path)
        if text:
            text_box.delete(1.0, tk.END)
            text_box.insert(tk.END, text[:500] + "...\n\n")  # Show first 500 chars
            skills = extract_skills(text)
            skills_box.delete(1.0, tk.END)
            skills_box.insert(tk.END, ", ".join(skills))
        else:
            messagebox.showerror("Error", "Unsupported file format!")

# -------------------------------
# GUI Setup
# -------------------------------
root = tk.Tk()
root.title("Resume Parser")
root.geometry("600x500")

upload_btn = tk.Button(root, text="Upload Resume", command=upload_resume, bg="#007bff", fg="white", font=("Arial", 12))
upload_btn.pack(pady=10)

tk.Label(root, text="Extracted Text (first 500 chars):", font=("Arial", 10, "bold")).pack()
text_box = scrolledtext.ScrolledText(root, width=70, height=10, wrap=tk.WORD)
text_box.pack(pady=5)

tk.Label(root, text="Skills Found:", font=("Arial", 10, "bold")).pack()
skills_box = scrolledtext.ScrolledText(root, width=70, height=5, wrap=tk.WORD)
skills_box.pack(pady=5)

root.mainloop()
