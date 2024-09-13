from flask import Flask, request, jsonify
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os
from dotenv import load_dotenv
import ast

load_dotenv()

app = Flask(__name__)

DROPSCAN_IP = os.getenv('DROPSCAN_IP')
FALLBACK_MAIL = os.getenv('FALLBACK_MAIL')
FALLBACK_RECIPIENT = os.getenv('FALLBACK_RECIPIENT')
RECIPIENTS = ast.literal_eval(os.getenv('RECIPIENTS'))
KEY_PATH = os.getenv('KEY_PATH')

def send_mail(name, email, document):
    subject = f"Neuer Brief für {name}!"
    body = ""
    sender_email = os.getenv('SENDER_MAIL')
    recipient_email = email
    sender_password = os.getenv('SENDER_PASSWORD')
    smtp_server = os.getenv('SMTP_SERVER')
    smtp_port = os.getenv('SMTP_PORT')
    message = MIMEMultipart()
    message['Subject'] = subject
    message['From'] = sender_email
    message['To'] = recipient_email
    message['Cc'] = FALLBACK_MAIL
    body_part = MIMEText(body)
    message.attach(body_part)
    message.attach(MIMEApplication(document.read(), Name=document.filename))

    with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, [recipient_email,FALLBACK_MAIL], message.as_string())

@app.route('/<current_path>', methods=['POST'])
def webhook_receiver(current_path):

     if (current_path == KEY_PATH) and (request.headers.get('X-Forwarded-For', request.remote_addr) in DROPSCAN_IP or request.remote_addr in DROPSCAN_IP):
        try:
            metadata = json.loads(request.files['metadata'].read())

            if 'recipient_id' in metadata:
                recipient = metadata['recipient_id']
            else:
                recipient = FALLBACK_RECIPIENT

            name = RECIPIENTS[recipient]['name']
            email = RECIPIENTS[recipient]['email']
            document = request.files['document']

            send_mail(name, email, document)
        except:
            print ("error...")
        return jsonify({'message': 'POST successfully'}), 200
     else:
         print(request.headers.get('X-Forwarded-For', request.remote_addr))
     return jsonify({'message': 'POST failed'}), 403

if __name__ == '__main__':
    app.run(port=8000, debug=True)
