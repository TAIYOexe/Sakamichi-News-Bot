from email import message
from pyexpat.errors import messages
import requests
from bs4 import BeautifulSoup
import os

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

#環境変数取得
CHANNEL_ACCESS_TOKEN = os.environ["CHANNEL_ACCESS_TOKEN"]
CHANNEL_SECRET = os.environ["CHANNEL_SECRET"]
USER_ID = os.environ["USER_ID"]

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

# newsのスクレイピング
def sakura_news():
    root = 'https://sakurazaka46.com'

    list_url = 'https://sakurazaka46.com/s/s46/news/list'
    res = requests.get(list_url)
    soup = BeautifulSoup(res.text, 'html.parser')

    news = soup.find('ul', attrs={'class': 'com-news-part type-catenews'})

    items = news.find_all('li')

    messages = []
    for item in items:
        type = item.find('p', attrs={'class': 'type'}).text
        date = item.find('p', attrs={'class': 'date wf-a'}).text
        lead = item.find('p', attrs={'class': 'lead'}).text
        link = item.find('a')
        url = link['href']

        message = type + '\n' + date + '\n' + lead + '\n' + root + url
        messages.append(message)

    return messages

def hinata_news():
    root = 'https://www.hinatazaka46.com'

    # htmlの取得
    list_url = 'https://www.hinatazaka46.com/s/official/news/list'
    res = requests.get(list_url)
    soup = BeautifulSoup(res.text, 'html.parser')

    news = soup.find('ul', attrs={'class': 'p-news__list p-news__list--long'})

    items = news.find_all('li')

    messages = []
    for item in items:
        type = item.find('div').text
        date = item.find('time').text
        lead = item.find('p').text.strip()
        url = item.find('a')['href']

        message = type + '\n' + date  + '\n' + lead + '\n' + root + url
        messages.append(message)
    
    return messages

def main():
    messages = sakura_news()
    for i in range(10):
        line_bot_api.push_message(USER_ID, TextSendMessage(text=messages[i]))
    messages = hinata_news()
    for i in range(10):
        line_bot_api.push_message(USER_ID, TextSendMessage(text=messages[i]))


if __name__ == "__main__":
    main()