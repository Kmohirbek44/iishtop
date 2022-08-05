import os,sys
from django.contrib.auth import get_user_model
import datetime

proj=os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ['DJANGO_SETTINGS_MODULE']='API_project.settings'
import django
django.setup()
import scraping.models
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from platform import python_version
# from dotenv import load_dotenv
# load_dotenv()
import smtplib
import os
from email.mime.text import MIMEText


# def send_email(message):
#     sender = "'komilovmohirbekfda1@gmail.com'"
#     # your password = "your password"
#     password = 'cltewxhpqdiakuqo'
#
#     server = smtplib.SMTP("smtp.gmail.com", 587)
#     server.starttls()
#
#     try:
#         server.login(sender, password)
#         msg = MIMEText(message)
#         msg["Subject"] = "CLICK ME PLEASE!"
#         server.sendmail(sender, sender, msg.as_string())
#
#         # server.sendmail(sender, sender, f"Subject: CLICK ME PLEASE!\n{message}")
#
#         return "The message was sent successfully!"
#     except Exception as _ex:
#         return f"{_ex}\nCheck your login or password please!"
#
#
# def main():
#     message = input("Type your message: ")
#     print(send_email(message=message))


# if __name__ == "__main__":
#     main()
def send():
    server = 'smtp.gmail.com'
    subject='Vakansiyalar'
    text_content='Vakansiyalar'
    from_email='komilovmohirbekfda1@gmail.com'
    empty='malumot yoq'
    user = 'komilovmohirbekfda1@gmail.com'
    password = 'cltewxhpqdiakuqo'

    today=datetime.date.today()
    User=get_user_model()
    qs=User.objects.filter(send_email=True).values('city','language','email')
    user_dct={}
    for i in qs:
        user_dct.setdefault((i['city'],i['language']),[])
        user_dct[(i['city'],i['language'])].append(i['email'])
    if user_dct:
        params={'city_id__in':[],'language_id__in':[]}
        for pair in user_dct.keys():
            params['city_id__in'].append(pair[0])
            params['language_id__in'].append(pair[1])

        qs=scraping.models.Vakation.objects.filter(**params,timestap=today).values()[:10]
        vacancies={}

        for i in qs:
            vacancies.setdefault((i['city_id'],i['language_id']),[])
            vacancies[(i['city_id'],i['language_id'])].append(i)
        for keys,emails in user_dct.items():
            rows=vacancies.get(keys,[])
            html=''
            for row in rows:

                html+=f'<h5><a href="{row["url"]}">{row["title"]}</a></h5>'
                html+=f'<p>Vakansiyalar :  {row["description"]}</p>'
                html+=f'<p>{row["company"]} </p><br><hr>'

            _html=html
            for email in emails:
                to=email
                msg = MIMEMultipart('alternative')
                msg['Subject'] = subject
                msg['From'] = 'Vakansiyalar <' + from_email + '>'
                msg['To'] = ', '.join(to)
                msg['Reply-To'] = from_email
                msg['Return-Path'] = from_email
                msg['X-Mailer'] = 'Python/' + (python_version())


                part_html = MIMEText(_html, 'html')

                msg.attach(part_html)


                mail = smtplib.SMTP_SSL(server)
                mail.login(user, password)
                mail.sendmail(from_email, to, msg.as_string())
                mail.quit()
# a=1
send()
