import smtplib  
from email.message import EmailMessage  
import os
from dotenv import load_dotenv
import json

load_dotenv()
# "Словарь" для хранения пользователей
user_list = {}


with open("content/questions.json", encoding='UTF8') as file:
    questions = json.load(file)


class APIException(Exception):  
    pass


class User:
    def __init__(self):
        self.counter = 0  # Счетчик на каком вопросе
        # "Словарь" животных, цифра это то сколько балов набрано для него, ответом потом будет тот у кого баллов выше
        # так как это словарь то значения будут одинаковые во всех файлах
        self.points_list = questions['points_list']

    def add_counter(self):
        self.counter += 1

    # Метод для начисления очков животным
    def give_points(self, list_ans):
        for i in range(len(list_ans)):
            i = str(i + 1)
            self.points_list[list_ans[i]] += 1


# Класс для викторины
class Quiz:
    # Получаю вопрос и ответ
    @staticmethod
    def get_question(i):
        i = str(i + 1)
        text = questions[i]['question']
        answers = questions[i]['answers']
        return text, answers


class MailSender:
    def __init__(self):
        self.smtpObj = smtplib.SMTP_SSL('smtp.mail.ru', 465)
        self.smtpObj.login(os.getenv('EMAIL'), os.getenv('EMAIL_PASSWORD'))

    def send(self, result, first_name, last_name):
        msg = EmailMessage()
        msg['Subject'] = "Вопрос о программе опеки"
        msg['From'] = os.getenv('EMAIL')
        msg['To'] = os.getenv('CONTACT_EMAIL')
        msg.set_content(f"{first_name} {last_name} получил результат {result} и теперь интересуется в программе опеки "
                        f"и имеет несколько вопросов о программе, вскоре от него должно поступить письмо.")
        with open(f'content/{result}.jpg', 'rb') as photo:
            img_data = photo.read()
        msg.add_attachment(img_data, maintype="image", subtype="jpeg")
        self.smtpObj.send_message(msg)
        msg.set_content(" ")

    def send_feedback(self, first_name, last_name, feedback):
        msg = EmailMessage()
        msg['subject'] = "Обратная связь о работе бота"
        msg['From'] = os.getenv('EMAIL')
        msg['To'] = os.getenv('CONTACT_EMAIL')
        msg.set_content(f"{first_name} {last_name} посылает обратную связь о работе бота:\n{feedback}")
        self.smtpObj.send_message(msg)
        msg.set_content(" ")
