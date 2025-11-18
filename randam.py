import pandas as pd
import random
import string
import numpy as np

# Load existing dataset
df = pd.read_csv("candidate.csv")

# -------------------------------
# RANDOM DATA GENERATORS
# -------------------------------

skill_pool = [
    "Python", "Java", "C++", "SQL", "Machine Learning", "Deep Learning",
    "Data Analysis", "AWS", "Docker", "Kubernetes", "HTML", "CSS",
    "JavaScript", "TensorFlow", "PyTorch", "React", "Node.js"
]

education_levels = [
    "B.Tech", "B.E", "B.Sc", "M.Tech", "M.Sc", "MCA", "BCA", "Diploma"
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
    base = name.replace(" ", ".").lower()
    return base + "@gmail.com"

def random_skills():
    s = random.sample(skill_pool, random.randint(2, 6))
    # boost by inserting ML or Python for better hiring likelihood
    if random.random() < 0.25:
        s.append("Machine Learning")
    if random.random() < 0.25:
        s.append("Python")
    return ", ".join(sorted(set(s)))

def random_personality():
    # Traits between 1 and 5
    return {
        "Openness": random.randint(1, 5),
        "Conscientiousness": random.randint(1, 5),
        "Extroversion": random.randint(1, 5),
        "Agreeableness": random.randint(1, 5),
        "Neuroticism": random.randint(1, 5),
    }

# -------------------------------
# GENERATE NEW CANDIDATES
# -------------------------------

num_new = 200  # Generate 400 new rows

new_rows = []

for _ in range(num_new):
    name = random_name()
    email = random_email(name)
    skills = random_skills()
    education = random.choice(education_levels)
    experience = round(abs(np.random.normal(2, 2)), 2)  # mean 2 yrs

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

df_new = pd.DataFrame(new_rows)

# -------------------------------
# APPEND TO CSV
# -------------------------------
df_final = pd.concat([df, df_new], ignore_index=True)
df_final.to_csv("candidate.csv", index=False)

print(f"{num_new} new candidates added to candidate.csv successfully!")
