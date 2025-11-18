import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
import smtplib
from email.mime.text import MIMEText

# ----------------------------------
# LOAD DATA
# ----------------------------------
df = pd.read_csv("candidate0.csv")

df["Skills"] = df["Skills"].fillna("").astype(str).str.lower()

# ----------------------------------
# TF-IDF SKILL VECTORIZATION
# ----------------------------------
vectorizer = TfidfVectorizer(max_features=150)
X_skills = vectorizer.fit_transform(df["Skills"])

# ----------------------------------
# PERSONALITY SCORE (Weighted)
# ----------------------------------
df["Personality_Score"] = (
    df["Openness"] * 0.25 +
    df["Conscientiousness"] * 0.30 +
    df["Extroversion"] * 0.20 +
    df["Agreeableness"] * 0.20 -
    df["Neuroticism"] * 0.15
)

# ----------------------------------
# EXPERIENCE FIX (Freshers dataset)
# ----------------------------------
df["Experience"] = df["Experience"].fillna(0).astype(float)

scaler = StandardScaler()
df["Experience_Norm"] = scaler.fit_transform(df[["Experience"]])

# ----------------------------------
# GENERATE A HIRING LABEL (Auto)
# ensures model learns real patterns
# ----------------------------------
df["Auto_Hired_Label"] = (
    (df["Personality_Score"] > df["Personality_Score"].median()).astype(int) +
    (df["Skills"].str.contains("python")).astype(int) +
    (df["Skills"].str.contains("machine learning")).astype(int)
)

# Hire if at least 2 good signals
df["Auto_Hired_Label"] = (df["Auto_Hired_Label"] >= 2).astype(int)

# ----------------------------------
# FINAL FEATURE SET
# ----------------------------------
X_num = df[["Personality_Score", "Experience_Norm"]].values

from scipy.sparse import hstack
X = hstack([X_skills, X_num])

y = df["Auto_Hired_Label"]

# ----------------------------------
# TRAIN ML MODEL
# ----------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)

model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

# ----------------------------------
# PREDICT HIRING
# ----------------------------------
df["Hired_Predicted"] = model.predict(X)

selected = df[df["Hired_Predicted"] == 1]

# ----------------------------------
# DISPLAY RESULTS
# ----------------------------------
if selected.empty:
    print("⚠ No one hired. Your dataset may be low-quality.")
else:
    print("🎉 Hired Candidates:")
    for name in selected["Name"]:
        print(name)

# Save CSV
df.to_csv("final_candidate_dataset0.csv", index=False)

# ----------------------------------
# EMAIL SELECTED CANDIDATES
# ----------------------------------
if not selected.empty:
    sender_email = "your_email@gmail.com"
    sender_password = "your_password"

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, sender_password)

    subject = "Congratulations! You Have Been Shortlisted"

    body_template = """Dear {},

Congratulations! Based on your skills and personality traits, 
you have been shortlisted for the next round.

Regards,
Xtreme & Co
"""

    for _, row in selected.iterrows():
        msg = MIMEText(body_template.format(row["Name"]))
        msg["Subject"] = subject
        msg["From"] = sender_email
        msg["To"] = row["Email"]

        server.sendmail(sender_email, row["Email"], msg.as_string())

    server.quit()
    print("📩 Emails sent successfully!")
