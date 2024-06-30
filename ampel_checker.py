import requests
from bs4 import BeautifulSoup
import os
import smtplib
from email.mime.text import MIMEText

url = os.getenv('WEBSITE')
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

def get_current_light(soup):
    traffic_light = soup.find('div', class_='trafficLight')
    if traffic_light:
        if traffic_light.find('span', class_='red'):
            return 'rot'
        elif traffic_light.find('span', class_='yellow'):
            return 'gelb'
        elif traffic_light.find('span', class_='green'):
            return 'grün'
    return 'keine aktive Farbe gefunden'

def send_email_notification():
    email_user = os.getenv('EMAIL_USER')
    email_password = os.getenv('EMAIL_PASSWORD')
    smtp_server = os.getenv('SMTP_SERVER')
    smtp_port = os.getenv('SMTP_PORT')
    to_email = os.getenv('TO_EMAIL')
    
    msg = MIMEText(paste0('Die Ampel ist grün! Call ', os.getenv('PHONE')))
    msg['Subject'] = 'Ampel Checker'
    msg['From'] = email_user
    msg['To'] = to_email

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(email_user, email_password)
        server.sendmail(email_user, to_email, msg.as_string())

if __name__ == "__main__":
    if get_current_light(soup) == 'rot':
        send_email_notification()
