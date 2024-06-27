import requests
from bs4 import BeautifulSoup
import os
import smtplib
from email.mime.text import MIMEText

def get_current_light():
    url = "URL_DER_WEBSITE"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    section = soup.find('section', class_='elementor-section')
    if section:
        if 'rot' in section.get('class', []):
            return 'rot'
        elif 'gelb' in section.get('class', []):
            return 'gelb'
        elif 'gruen' in section.get('class', []):
            return 'grün'
    return 'keine aktive Farbe gefunden'

def send_email_notification():
    email_user = os.getenv('EMAIL_USER')
    email_password = os.getenv('EMAIL_PASSWORD')
    smtp_server = os.getenv('SMTP_SERVER')
    smtp_port = os.getenv('SMTP_PORT')
    to_email = os.getenv('TO_EMAIL')
    
    msg = MIMEText('Die Ampel ist grün!')
    msg['Subject'] = 'Ampel Status'
    msg['From'] = email_user
    msg['To'] = to_email

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(email_user, email_password)
        server.sendmail(email_user, to_email, msg.as_string())

if __name__ == "__main__":
    if get_current_light() == 'grün':
        send_email_notification()
