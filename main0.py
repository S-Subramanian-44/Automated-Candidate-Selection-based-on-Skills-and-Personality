import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestClassifier
import smtplib
from email.mime.text import MIMEText

df = pd.read_csv('candidate0.csv')
df.isnull().sum()
label_encoder = LabelEncoder()

df['Skills'] = df['Skills'].apply(lambda x: ', '.join(sorted(str(x).split(', '))) if pd.notna(x) else x)
df['Skills'] = label_encoder.fit_transform(df['Skills'])
df['Education'] = label_encoder.fit_transform(df['Education'])

def assess_skill_competency(skills):
    return skills

df['Skill_Competency'] = df['Skills'].apply(assess_skill_competency)

def assess_personality(openness, conscientiousness, extroversion, agreeableness, neuroticism):
    return openness + conscientiousness + extroversion + agreeableness - neuroticism

df['Personality_Score'] = df.apply(lambda row: assess_personality(row['Openness'], row['Conscientiousness'],
                                                                row['Extroversion'], row['Agreeableness'],
                                                                row['Neuroticism']), axis=1)

df.to_csv('updated_candidate0.csv', index=False)

df['Years_Experience_Education'] = df['Education']
df['Skill_Education_Interaction'] = df['Skills'] * df['Education']

scaler = StandardScaler()
df['Normalized_Personality_Score'] = scaler.fit_transform(df[['Personality_Score']])
df['Hired'] = 0

df.to_csv('updated_candidate0.csv', index=False)

outcomes = df['Hired']

skill_model = LinearRegression()
personality_model = RandomForestClassifier()

features = df[['Skill_Competency', 'Normalized_Personality_Score', 'Years_Experience_Education', 'Skill_Education_Interaction']]
X_train, X_test, y_train, y_test = train_test_split(features, outcomes, test_size=0.2, random_state=42)

skill_model.fit(X_train, y_train)
personality_model.fit(X_train, y_train)

skill_predictions = skill_model.predict(X_test)
personality_predictions = personality_model.predict(X_test)

skill_threshold = 0.7
personality_threshold = 0.6
interaction_threshold = 100

df['Hired'] = (
    (df['Skill_Competency'] >= skill_threshold) &
    (df['Normalized_Personality_Score'] >= personality_threshold) &
    (df['Skill_Education_Interaction'] >= interaction_threshold)
).astype(int)

selected_candidates = df[df['Hired'] == 1]

hired_candidates = selected_candidates['Name'].tolist()

if hired_candidates:
    print("Hired Candidates:")
    for candidate in hired_candidates:
        print(candidate)
else:
    print("No one is hired.")

df.to_csv('final_candidate_dataset0.csv', index=False)

if hired_candidates:
    sender_email = "71762133044@cit.edu.in"
    sender_password = "mani@2133044"
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(sender_email, sender_password)

    subject = "Congratulations! You've Been Selected for the Next Round."
    body = "Dear {},\n\nCongratulations! We are thrilled to inform you that you have been selected to advance to the next round of our selection process. Your profile and outstanding performance on the personality test have set you apart, and we are excited to explore your potential further in the upcoming stages.\n\nBest regards,\nDSK Company"

    for candidate_email in selected_candidates['Email']:
        msg = MIMEText(body.format(candidate_email))
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = candidate_email

        server.sendmail(sender_email, candidate_email, msg.as_string())

    server.quit()

    print("Emails sent successfully.")
else:
    print("No one is hired.")
