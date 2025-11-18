import pandas as pd
import random
import string
import numpy as np

# Load the fresher dataset
df0 = pd.read_csv("candidate0.csv")

# -------------------------------
# RANDOM DATA GENERATORS
# -------------------------------

skill_pool = [
    "Python", "Java", "C++", "SQL", "Machine Learning", "Data Analysis",
    "HTML", "CSS", "JavaScript", "Django", "Flask", "React",
    "Git", "Excel", "Power BI"
]

education_levels = [
    "B.Tech", "B.E", "B.Sc", "BCA", "Diploma", "MCA"
]

def random_name():
    first = "".join(random.choices(string.ascii_uppercase, k=1)) + "".join(
        random.choices(string.ascii_lowercase, k=random.randint(4, 7))
    )
    last = "".join(random.choices(string.ascii_uppercase, k=1)) + "".join(
        random.choices(string.ascii_lowercase, k=random.randint(4, 7))
    )
    return f"{first} {last}"

def random_email(name):
    return name.replace(" ", ".").lower() + "@gmail.com"

def random_skills():
    s = random.sample(skill_pool, random.randint(2, 6))
    # Boost top skills so ML can hire someone later
    if random.random() < 0.4:
        s.append("Python")
    if random.random() < 0.3:
        s.append("Machine Learning")
    return ", ".join(sorted(set(s)))

def random_personality():
    return {
        "Openness": random.randint(2, 5),
        "Conscientiousness": random.randint(2, 5),
        "Extroversion": random.randint(2, 5),
        "Agreeableness": random.randint(2, 5),
        "Neuroticism": random.randint(1, 4),
    }

# -------------------------------
# GENERATE NEW FRESHER CANDIDATES
# -------------------------------

num_new = 250  # You can increase if needed

new_rows = []

for _ in range(num_new):
    name = random_name()
    email = random_email(name)
    skills = random_skills()
    education = random.choice(education_levels)
    
    # Freshers typically have 0–1 years experience
    experience = round(abs(np.random.normal(0.3, 0.4)), 2)
    if experience > 1.5:
        experience = 1.0  # Keep freshers realistic
    
    traits = random_personality()

    row = {
        "Name": name,
        "Email": email,
        "Skills": skills,
        "Education": education,
        "Experience": experience,
        "Openness": traits["Openness"],
        "Conscientiousness": traits["Conscientiousness"],
        "Extroversion": traits["Extroversion"],
        "Agreeableness": traits["Agreeableness"],
        "Neuroticism": traits["Neuroticism"],
    }

    new_rows.append(row)

df_new0 = pd.DataFrame(new_rows)

# -------------------------------
# APPEND TO candidate0.csv
# -------------------------------
df_final0 = pd.concat([df0, df_new0], ignore_index=True)
df_final0.to_csv("candidate0.csv", index=False)

print(f"{num_new} new FRESHER candidates added to candidate0.csv successfully!")
