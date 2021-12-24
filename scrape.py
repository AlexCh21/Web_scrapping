
import requests
from bs4 import BeautifulSoup
import re

KEYWORDS = ['дизайн', 'фото', 'web', 'python']

ret = requests.get('https://habr.com/ru/all/')
soup = BeautifulSoup(ret.text, 'html.parser')
posts = soup.find_all('article', class_='post')
all_links_read = []
for post in posts:
    all_blogs_read = post.find_all('a', class_='btn btn_x-large btn_outline_blue post__habracut-btn')
    all_blogs_read = str(all_blogs_read)
    all_link_read = re.search("(https:\/\/habr\.com\/ru\/)(post|company)?\/?([\w]+)?\/?(blog)?\/?([\d]+)\/?#habracut", all_blogs_read).group(0)
    all_links_read.append(all_link_read)

for link in all_links_read:
    ret = requests.get(link)
    soup = BeautifulSoup(ret.text, 'html.parser')
    article_text = soup.find('div', class_='post__body post__body_full')
    article_text = article_text.text
    if any([key_word in article_text for key_word in KEYWORDS]):
        title = soup.find('span', class_='post__title-text')
        title = title.text
        time_element = soup.find('span', class_='post__time')
        time_element = time_element.attrs.get('data-time_published')

        print(f'<{time_element}> - <{title}> - <{link}>')

