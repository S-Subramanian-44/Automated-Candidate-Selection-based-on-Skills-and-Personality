# Automated-Candidate-Selection-based-on-Skills-and-Personality

## Overview

This project implements an automated candidate selection system using Flask, resume analysis, and machine learning. Candidates submit details through a web app, and their resumes are processed to assess their skills and personality. Machine learning models make hiring decisions, and successful candidates receive email notifications.

## Features

- **Web Application:** Utilizes Flask for user sign-up, login, and resume submission.
- **Resume Processing:** Extracts skills and education information from resumes using PyMuPDF and regular expressions.
- **Candidate Assessment:** Evaluates candidates based on skill competency and personality traits.
- **Machine Learning Models:** Implements Linear Regression for skill competency and a Random Forest Classifier for personality assessment.
- **Automated Hiring:** Employs threshold-based criteria for making hiring decisions.
- **Email Notifications:** Sends personalized emails to successful candidates.


Automated Candidate Selection System
Overview
This project employs machine learning models to automate the candidate selection process, incorporating resume analysis, skill evaluation, and personality assessments. The Five Big Traits—Openness, Conscientiousness, Extraversion, Agreeableness, and Neuroticism—are assessed through a personality assessment conducted via five questions, each measured on a scale from strongly agree to strongly disagree. Successful candidates receive personalized email notifications, optimizing and streamlining the hiring process.

## Five Big Traits in Personality Assessment
- *Openness*: Measures the candidate's openness to new experiences, ideas, and ways of thinking.
- *Conscientiousness*: Assesses the level of organization, responsibility, and dependability of the candidate.
- *Extraversion*: Gauges the candidate's sociability, assertiveness, and comfort in social situations.
- *Agreeableness*: Measures the candidate's interpersonal skills, empathy, and cooperative nature.
- *Neuroticism*: Evaluate the candidate's emotional stability, resilience, and stress response.

**These traits are derived from a personality assessment, consisting of five questions for each trait, with responses ranging from strongly agree to strongly disagree.**

## Usage

1. Install dependencies: `pip install -r requirements.txt`
2. Run the Flask app: `python app.py`
3. Access the app in your browser at `http://localhost:5000`

## Data Storage

- Candidate data is stored in CSV files (`candidate0.csv` for junior, `candidate.csv` for experienced).
