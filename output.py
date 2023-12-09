from flask import Flask, render_template, request, redirect, url_for, session, flash
import pandas as pd
from collections import defaultdict
import os
import re
import fitz

app = Flask(__name__)
app.secret_key = 'your_secret_key'

data_file = 'data.xlsx'

csv_file_junior = 'candidate0.csv'
try:
    df_junior = pd.read_csv(csv_file_junior)
except FileNotFoundError:
    df_junior = pd.DataFrame(columns=['Candidate_ID', 'Name', 'Age', 'Mobile', 'Gender', 'Email','Skills', 'Education'])

csv_file_experience = 'candidate.csv'
try:
    df_experience = pd.read_csv(csv_file_experience)
except FileNotFoundError:
    df_experience = pd.DataFrame(columns=['Candidate_ID', 'Name', 'Age', 'Mobile', 'Gender', 'Email', 'Experience','Skills', 'Education'])

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['Name']
        degree = request.form['Degree']
        email = request.form['Email']
        phone_number = request.form['Phone Number']
        experience = request.form['Experience']
        password = request.form['Password']

        user_details = {
            'Name': name,
            'Degree': degree,
            'Email': email,
            'Phone Number': phone_number,
            'Experience': experience,
            'Password': password
        }

        if os.path.exists(data_file):
            if data_file.endswith('.xlsx'):
                df = pd.read_excel(data_file)
            elif data_file.endswith('.csv'):
                df = pd.read_csv(data_file)
            else:
                df = pd.DataFrame()

            new_user_df = pd.DataFrame([user_details])

            df = pd.concat([df, new_user_df], ignore_index=True)

            if data_file.endswith('.xlsx'):
                df.to_excel(data_file, index=False)
            elif data_file.endswith('.csv'):
                df.to_csv(data_file, index=False)
            else:
                print('Invalid file format')

            return redirect(url_for('login'))
        else:
            print(f"File '{data_file}' does not exist.")
    else:
        return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['Email']
        password = request.form['Password']

        if os.path.exists(data_file):
            if data_file.endswith('.xlsx'):
                df = pd.read_excel(data_file)
            elif data_file.endswith('.csv'):
                df = pd.read_csv(data_file)
            else:
                df = pd.DataFrame()

            user_exists = not df[(df['Email'] == email) & (df['Password'] == password)].empty

            if user_exists:
                return render_template('profile.html', name=email)
            else:
                return redirect(url_for('signup'))
        else:
            print(f"File '{data_file}' does not exist.")
    else:
        return render_template('login.html')

def process_resume(resume_file, dataset):
    upload_folder = 'uploads'
    os.makedirs(upload_folder, exist_ok=True)

    resume_path = os.path.join(upload_folder, resume_file.filename)
    resume_file.save(resume_path)

    try:
        pdf_document = fitz.open(resume_path)

        resume_text = ""
        for page in pdf_document:
            resume_text += page.get_text("text")

            found_skills = set()
            for skill in skills_to_find:
                pattern = rf'\b{re.escape(skill)}\b'
                matches = re.findall(pattern, resume_text, re.IGNORECASE)
                for match in matches:
                    found_skills.add(match.lower())

            found_education = set()
            for keyword in education_keywords:
                pattern = rf'\b{re.escape(keyword)}\b'
                matches = re.findall(pattern, resume_text, re.IGNORECASE)
                for match in matches:
                    found_education.add(match.lower())

        dataset.loc[dataset.index[-1], 'Skills'] = ", ".join(found_skills)
        dataset.loc[dataset.index[-1], 'Education'] = ", ".join(found_education)

        return redirect(url_for('profile', selected_candidate_type=session.get('user_type')))

    except FileNotFoundError:
        print("File not found. Please provide the correct path to the PDF file.")
    finally:
        if 'pdf_document' in locals():
            pdf_document.close()

skills_to_find = ["Java", "Python", "SQL", "C++", "JavaScript", "HTML/CSS", "C#", "PHP", "Data Structures",
                  "R", "Data Analysis", "React", "Node.js", "Machine Learning", "Angular", "UX Design",
                  "Data Science", "Database Administration"]

education_keywords = ["Bachelor's", "Master's", "PhD", "Degree", "University", "College", "Graduation", "Diploma", "M.Sc"]

@app.route('/select_candidate_type', methods=['GET', 'POST'])
def select_candidate_type():
    if request.method == 'POST':
        candidate_type = request.form.get('candidate_type')
        session['user_type'] = candidate_type
        if candidate_type == 'junior':
            return redirect('/junior')
        elif candidate_type == 'experience':
            return redirect('/experience')
    else:
        flash('Please select a candidate type.')

@app.route('/junior')
def index_junior():
    if 'user_type' in session and session['user_type'] == 'junior':
        return render_template('index0.html')
    else:
        return redirect(url_for('select_candidate_type'))

@app.route('/experience')
def index_experience():
    if 'user_type' in session and session['user_type'] == 'experience':
        return render_template('index1.html')
    else:
        return redirect(url_for('select_candidate_type'))

@app.route('/submit/junior', methods=['POST'])
def submit_junior():
    global df_junior

    name = request.form.get('name')
    age = int(request.form.get('age'))
    mobile = int(request.form.get('mobile'))
    gender = request.form.get('gender')
    email = request.form.get('email')

    candidate_id = df_junior['Candidate_ID'].max() + 1 if not df_junior.empty else 1
    candidate_id = int(candidate_id)

    questions = {
        'Openness': [int(request.form.get('openness_q1')), int(request.form.get('openness_q2'))],
        'Conscientiousness': [int(request.form.get('conscientiousness_q1')),
                              int(request.form.get('conscientiousness_q2'))],
        'Extroversion': [int(request.form.get('extroversion_q1')), int(request.form.get('extroversion_q2'))],
        'Agreeableness': [int(request.form.get('agreeableness_q1')), int(request.form.get('agreeableness_q2'))],
        'Neuroticism': [int(request.form.get('neuroticism_q1')), int(request.form.get('neuroticism_q2'))],
    }

    scores = calculate_scores(questions)

    new_data = {'Candidate_ID': [candidate_id], 'Name': [name], 'Age': [age], 'Mobile': [mobile], 'Gender': [gender],
                'Email': [email], **scores}
    new_df = pd.DataFrame(new_data)

    df_junior = pd.concat([df_junior, new_df], ignore_index=True)
    process_resume(request.files['resume'], df_junior)
    df_junior.to_csv(csv_file_junior, index=False)

    return render_template('thank.html', submission_message='Submission for Junior successful!')

@app.route('/submit/experience', methods=['POST'])
def submit_experience():
    global df_experience

    name = request.form.get('name')
    age = int(request.form.get('age'))
    mobile = int(request.form.get('mobile'))
    gender = request.form.get('gender')
    email = request.form.get('email')
    experience = int(request.form.get('experience'))

    candidate_id = df_experience['Candidate_ID'].max() + 1 if not df_experience.empty else 1
    candidate_id = int(candidate_id)

    questions = {
        'Openness': [int(request.form.get('openness_q1')), int(request.form.get('openness_q2'))],
        'Conscientiousness': [int(request.form.get('conscientiousness_q1')),
                              int(request.form.get('conscientiousness_q2'))],
        'Extroversion': [int(request.form.get('extroversion_q1')), int(request.form.get('extroversion_q2'))],
        'Agreeableness': [int(request.form.get('agreeableness_q1')), int(request.form.get('agreeableness_q2'))],
        'Neuroticism': [int(request.form.get('neuroticism_q1')), int(request.form.get('neuroticism_q2'))],
    }

    scores = calculate_scores(questions)

    new_data = {'Candidate_ID': [candidate_id], 'Name': [name], 'Age': [age], 'Mobile': [mobile], 'Gender': [gender],
                'Email': [email], 'Experience': [experience], **scores}
    new_df = pd.DataFrame(new_data)

    df_experience = pd.concat([df_experience, new_df], ignore_index=True)
    process_resume(request.files['resume'], df_experience)
    df_experience.to_csv(csv_file_experience, index=False)

    return render_template('thank.html', submission_message='Submission for Experience successful!')

@app.route('/profile')
def profile():
    selected_candidate_type = request.args.get('selected_candidate_type')
    email = session.get('email')
    username = email.split('@')[0]
    return render_template('profile.html', name=username, selected_candidate_type=selected_candidate_type)

def calculate_scores(answers):
    scores = defaultdict(int)

    for trait, values in answers.items():
        scores[trait] = int(sum(values)/5)

    return scores

def extract_skills_and_education_from_resume(pdf_file_path, skills_to_find, education_keywords):
    try:
        pdf_document = fitz.open(pdf_file_path)

        resume_text = ""
        for page in pdf_document:
            resume_text += page.get_text("text")

        found_skills = []
        for skill in skills_to_find:
            matches = re.findall(rf'\b{re.escape(skill)}\b', resume_text, re.IGNORECASE)
            if matches:
                found_skills.extend(matches)

        found_skills = list(set(found_skills))

        found_education = []
        for keyword in education_keywords:
            matches = re.findall(rf'\b{re.escape(keyword)}\b', resume_text, re.IGNORECASE)
            if matches:
                found_education.extend(matches)

        found_education = list(set(found_education))

        print("Found Skills:", ", ".join(found_skills))
        print("\nFound Education:")
        for education_info in found_education:
            print(education_info)

    except FileNotFoundError:
        print("File not found. Please provide the correct path to the PDF file.")
    finally:
        if 'pdf_document' in locals():
            pdf_document.close()

@app.route('/submit/resume', methods=['POST'])
def submit_resume():
    if 'resume' not in request.files:
        return redirect(request.url)

    resume_file = request.files['resume']

    if resume_file.filename == '':
        return redirect(request.url)

    process_resume(resume_file, df_experience)

    return redirect(url_for('profile', selected_candidate_type='experience'))

if __name__ == '__main__':
    app.run(debug=True)
