import pandas as pd
from datetime import datetime
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# Function to read the content of a file
def read_template(file_path):
    with open(file_path, 'r') as file:
        return file.read()


# Load letter templates
letter_templates = [
    read_template('letter_templates/letter_1.txt'),
    read_template('letter_templates/letter_2.txt'),
    read_template('letter_templates/letter_3.txt')
]

# Load the CSV file
df = pd.read_csv("birthdays.csv")

# Get today's date
today = datetime.today()
today_year = today.year
today_month = today.month
today_day = today.day


# Check if today is anyone's birthday
def check_birthday(row):
    return row["year"] == today_year and row["month"] == today_month and row["day"] == today_day


def sendmail(to_email, subject, body):
    smtp_server = "smtp.gmail.com"
    smtp_port = "587"
    smtp_user = "sampleEmail@gmail.com"  # Sample Email for Testing (Dummy)
    smtp_password = "samplePassword"  # Sample Password for Testing (Dummy)

    # Create the email
    msg = MIMEMultipart()
    msg["From"] = smtp_user
    msg["To"] = to_email
    msg["Subject"] = subject

    # Attach the email body
    msg.attach(MIMEText(body, "plain"))

    try:
        # Connect to the SMTP server and send the email
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.sendmail(smtp_user, to_email, msg.as_string())
        server.quit()
        print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email to {to_email}: {e}")


# Apply the check_birthday function to each row in the DataFrame
df["is_birthday_today"] = df.apply(check_birthday, axis=1)

# Print the rows where today is the birthday
birthdays_today = df[df["is_birthday_today"]]

# Check if there are any birthdays today
if not birthdays_today.empty:
    print("Today's Birthdays:")
    for index, row in birthdays_today.iterrows():
        name = row['name']
        email = row['email']
        print(f"Name: {name}, Email: {email}")

        # Select a random letter template
        letter_template = random.choice(letter_templates)

        # Customize the letter
        body = letter_template.replace('[NAME]', name)

        # Define the subject of the email
        subject = "Happy Birthday!"

        # Send the email
        sendmail(email, subject, body)
else:
    print("No birthdays today.")
