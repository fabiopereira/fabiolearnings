import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(subject, message, to_email):
    # Sender's email and password (use an App Password for Gmail)
    # AppPwd: infobesity-scale-book
    sender_email = "fabiopereira.me@gmail.com"
    sender_password = ""

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

# Example usage
template_path = 'sending-emails/infobesity-book-scale-template.txt'
variables = {'name': 'Mary', 'weight': 45, 'email': 'john@example.com'}
result_string = generate_string_from_template(template_path, variables)
# Print the generated string
# print(result_string)
# Example usage
subject = "Your result from Infobesity Digital Weight Scale"
message = result_string
to_emails = ["fabiopereira.me@gmail.com", "contato@fabionudge.com"]

send_email(subject, message, to_emails)
