import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pandas as pd

def send_emails_to_each_row(row):
    variables = {
        'Email': row['Email'], 
        'Name': row['Name'], 
        'DigitalWeightInfoKilos': row['DigitalWeightInfoKilos'], 
        'Scale': row['Scale'], 
        'Scale1Name': row['Scale1Name'], 
        'Scale2Name': row['Scale2Name'], 
        'WeightMessage': row['WeightMessage']
        }
    
    name = row['Name']
    email = row['Email']
    subject = f"Hey {name}, your result from the Infobesity scale"
    template_path = 'sending-emails/infobesity-book-scale-template.txt'
    message = generate_string_from_template(template_path, variables)
    to_emails = [email]
    print("Sending email:")
    send_email(subject, message, to_emails)
    print(variables)


def send_email(subject, message, to_email):
    # Sender's email and password (use an App Password for Gmail)
    # AppPwd: infobesity-scale-book
    sender_email = "fabiopereira.me@gmail.com"
    sender_password = "umqw qsxw yaxn mkjw"

    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = ', '.join(to_email)
    msg['Subject'] = subject

    # Attach the message to the email
    msg.attach(MIMEText(message, 'plain'))

    # Establish a connection to the SMTP server (in this case, Gmail's SMTP server)
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        # Start the TLS connection
        server.starttls()

        # Login to the Gmail account
        server.login(sender_email, sender_password)

        # Send the email
        server.sendmail(sender_email, to_email, msg.as_string())

    print(f"Email sent to {', '.join(to_email)} successfully.")


def generate_string_from_template(template_path, variables):
    # Read the template file
    with open(template_path, 'r') as template_file:
        template = template_file.read()

    # Replace placeholders with variable values
    merged_text = template.format(**variables)

    return merged_text


df = pd.read_csv('sending-emails/infobesity-book-scale-TOSEND.csv')
for index, row in df.iterrows():
    try:
        send_emails_to_each_row(row)
    except Exception as e:
        print(f"An exception occurred: {e}")

