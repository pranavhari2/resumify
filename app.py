from flask import Flask, request, jsonify, send_from_directory
import openai
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
import PyPDF2
import docx2txt
from werkzeug.utils import secure_filename
from openai import OpenAI

# Load Api key 
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/generate-cover-letter', methods=['POST'])
def generate_cover_letter_endpoint():

    # company_name = request.form.get('company_name')
    # resume = request.files['resume']

    # filename = secure_filename(resume.filename)
    # file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    # resume.save(file_path)

    # resume_text = extract_text_from_resume(file_path)

    data = request.json 

    company_name = data['company']
    resume_text = data['resume']

    # cover_letter = generate_cover_letter(company_name)

    cover_letter = generate_cover_letter(company_name, resume_text)

    # print(cover_letter)

    return jsonify({"cover_letter": cover_letter})


# def scrape(url):
#     resp = requests.get(url)
#     soup = BeautifulSoup(resp.text, 'html.parser')
#     comp_name = soup.find('title').text

#     return comp_name

def extract_text_from_resume(file_path):
    if file_path.endswith('.pdf'):
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfFileReader(file)
            text = ''
            for page_num in range(reader.numPages):
                page = reader.getPage(page_num)
                text += page.extractText()
        return text
    elif file_path.endswith('.docx'):
        return docx2txt.process(file_path)
    else:
        return ''

def generate_cover_letter(company_name, resume_text):
    openai.api_key = openai_api_key
    
    prompt = f"Write a cover letter for a software engineer position at {company_name}. Mention the company's values, recent projects, and why I would be a good fit. Here is my resume:\n{resume_text}"

    chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": prompt,
        }
    ],
    model="gpt-4o-mini",
    )

    return chat_completion.choices[0].message.content

if __name__ == '__main__':
    app.run(debug=True)
