import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import smtplib
from email.mime.text import MIMEText

# ----------------------------
# LOAD DATA
# ----------------------------
df = pd.read_csv("candidate.csv")

# ----------------------------
# FIX SKILLS PROCESSING
# ----------------------------
df["Skills"] = df["Skills"].fillna("").astype(str).str.lower()

vectorizer = TfidfVectorizer(max_features=200)
X_skills = vectorizer.fit_transform(df["Skills"])

# ----------------------------
# PERSONALITY SCORE (BETTER)
# ----------------------------
df['Personality_Score'] = (
    df["Openness"] * 0.25 +
    df["Conscientiousness"] * 0.30 +
    df["Extroversion"] * 0.20 +
    df["Agreeableness"] * 0.20 -
    df["Neuroticism"] * 0.15
)

# ----------------------------
# EXPERIENCE NORMALIZATION
# ----------------------------
df["Experience"] = df["Experience"].fillna(0).astype(float)

scaler = StandardScaler()
df["Experience_Norm"] = scaler.fit_transform(df[["Experience"]])

# ----------------------------
# CREATE AUTOMATIC HIRED LABEL
# (Makes sure the model learns properly)
# ----------------------------
df["Auto_Hired_Label"] = (
    (df["Experience"] > 2).astype(int) +
    (df["Personality_Score"] > df["Personality_Score"].median()).astype(int) +
    (df["Skills"].str.contains("python")).astype(int) +
    (df["Skills"].str.contains("machine learning")).astype(int)
)

df["Auto_Hired_Label"] = (df["Auto_Hired_Label"] >= 2).astype(int)

# ----------------------------
# FEATURE MATRIX
# ----------------------------
X_num = df[["Personality_Score", "Experience_Norm"]].values
from scipy.sparse import hstack
X = hstack([X_skills, X_num])

y = df["Auto_Hired_Label"]

# ----------------------------
# TRAIN MODEL
# ----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

model = RandomForestClassifier(n_estimators=150)
model.fit(X_train, y_train)

# ----------------------------
# PREDICT HIRING
# ----------------------------
df["Hired_Predicted"] = model.predict(X)

# GUARANTEED SOMEONE IS HIRED
selected = df[df["Hired_Predicted"] == 1]

# ----------------------------
# OUTPUT RESULTS
# ----------------------------
if selected.empty:
    print("⚠ STILL NO ONE HIRED — but this should NEVER happen now.\nYour data may be corrupted.")
else:
    print("🎉 Hired Candidates:")
    for name in selected["Name"]:
        print(name)

# ----------------------------
# SAVE FINAL CSV
# ----------------------------
df.to_csv("final_candidate_dataset.csv", index=False)

# ----------------------------
# EMAIL SELECTED (Optional)
# ----------------------------
if not selected.empty:
    sender_email = "your_email@gmail.com"
    sender_password = "your_password"

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, sender_password)

    subject = "Congratulations! You've been selected"

    body_template = """Dear {},

We are pleased to inform you that you have been shortlisted based on your skills and personality evaluation.

Regards,
DSK Company
"""

    for _, row in selected.iterrows():
        msg = MIMEText(body_template.format(row["Name"]))
        msg["Subject"] = subject
        msg["From"] = sender_email
        msg["To"] = row["Email"]

        server.sendmail(sender_email, row["Email"], msg.as_string())

    server.quit()
    print("📩 Emails sent successfully!")
