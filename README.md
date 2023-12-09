# Automated-Candidate-Selection-based-on-Skills-and-Personality

## Overview

This project implements an automated candidate selection system using Flask, resume analysis, and machine learning. Candidates submit details through a web app, and their resumes are processed to assess skills and personality. Machine learning models make hiring decisions, and successful candidates receive email notifications.

## Features

- **Web Application:** Utilizes Flask for user sign-up, login, and resume submission.
- **Resume Processing:** Extracts skills and education information from resumes using PyMuPDF and regular expressions.
- **Candidate Assessment:** Evaluates candidates based on skill competency and personality traits.
- **Machine Learning Models:** Implements Linear Regression for skill competency and a Random Forest Classifier for personality assessment.
- **Automated Hiring:** Employs threshold-based criteria for making hiring decisions.
- **Email Notifications:** Sends personalized emails to successful candidates.

## Usage

1. Install dependencies: `pip install -r requirements.txt`
2. Run the Flask app: `python app.py`
3. Access the app in your browser at `http://localhost:5000`

## Data Storage

- Candidate data is stored in CSV files (`candidate0.csv` for junior, `candidate.csv` for experienced).
