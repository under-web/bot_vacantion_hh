import time
import telebot
import requests
from config import api_token, channel
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

bot = telebot.TeleBot(api_token)

def get_html(url):
    """
    Принимает урл и подменяет юзер-агент
    :param url:
    :return: html-text страницы
    """
    ua = UserAgent()
    headers = {'User-Agent': ua.firefox}
    res = requests.get(url, headers=headers)
    return res.text


def get_vacantion(res):
    """
    Принимает html текст и парсит вакансии с hh.ru
    :param res:
    :return: список в строковом значении
    """
    b_list = []
    soup = BeautifulSoup(res, 'lxml')
    block_vac = soup.find_all('div', class_='vacancy-serp-item')
    for i in block_vac:
        title = i.find('a', class_='bloko-link').text
        linkin = i.find('a').get('href')
        try:
            salary = i.find('div', class_='vacancy-serp-item__sidebar').text
        except Exception as e:
            print('salary err ', e)
            continue
        if salary == '':
            salary = 'Не указана'
        b_list.append(title + '\n')
        b_list.append(salary + '\n')
        b_list.append(linkin + '\n')
    result_note = ''.join(b_list)
    return result_note

def main():
    """
    Управляющая функция
    :return:
    """
    while True:
        # try:
            url = 'https://kazan.hh.ru/search/vacancy?area=88&fromSearchLine=true&st=searchVacancy&text=Junior+python' \
                  '&from=suggest_post '
            bot.send_message(channel, get_vacantion(get_html(url)))  # Указываем канал и текст который нужно отправить
            time.sleep(21600)
        # except Exception as e:
        #     if 'API was unsuccessful' in str(e):
        #         print('Проверьте доступ API код 401')
        #         break
        #     else:
        #         print('err main', e)
        #         time.sleep(20)

if __name__ == '__main__':
    main()