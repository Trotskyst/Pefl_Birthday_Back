import requests
import lxml.html as html
import json


def text_from_link(link):
    """ Скачивает с сайта pefl.ru страницу по её адресу """
    headers = {
        'Cookie': "PHPSESSID=7bb86e5db64ca692b7dd9959ce52f862; rfl=amVmOl86MTc0ODpfOmQyYjBlYTUzZDRiMTc5NDM5ZWJmODAyNzg0ZWU5MjNl; last_visit=1553443497893::1553454297893",
        'cache-control': "no-cache",
        'Postman-Token': "0eeeb98b-a58a-4b41-87a8-a7ebe83d5e31"
    }
    page = requests.request("GET", link, headers=headers)
    page.encoding = 'windows-1251'
    # print(page.text, file=open('file.htm', 'w'))
    return html.document_fromstring(page.text)



def text_from_link3(link, count):
    """ Скачивает с сайта pefl.ru страницу по её адресу """
    headers = {
        'Cookie': "PHPSESSID=7bb86e5db64ca692b7dd9959ce52f862; rfl=amVmOl86MTc0ODpfOmQyYjBlYTUzZDRiMTc5NDM5ZWJmODAyNzg0ZWU5MjNl; last_visit=1553443497893::1553454297893",
        'cache-control': "no-cache",
        'Postman-Token': "0eeeb98b-a58a-4b41-87a8-a7ebe83d5e31"
    }
    page = requests.request("GET", link, headers=headers)
    page.encoding = 'windows-1251'
    print(page.text, file=open('file'+str(count)+'.htm', 'w'))
    return html.document_fromstring(page.text)


def text_from_link2(link):
    """ Скачивает с сайта pefl.ru страницу по её адресу """
    headers = {
        'Cookie': "PHPSESSID=7bb86e5db64ca692b7dd9959ce52f862; rfl=amVmOl86MTc0ODpfOmQyYjBlYTUzZDRiMTc5NDM5ZWJmODAyNzg0ZWU5MjNl; last_visit=1553443497893::1553454297893",
        'cache-control': "no-cache",
        'Postman-Token': "0eeeb98b-a58a-4b41-87a8-a7ebe83d5e31"
    }
    page = requests.request("GET", link, headers=headers)
    page.encoding = 'windows-1251'
    # print(page.text, file=open('file.htm', 'w'))
    return page.text


def find_link_by_link_text(doc, text_to_find):
    """ Находит в документе ссылку "a href=" по тексту ссылки """
    for links in doc.cssselect('a'):
        if links.text == text_to_find:
            return links.get('href')


def text_from_json(link):
    """ Скачивает с сайта pefl.ru JSON страницу по её адресу """
    headers = {
        'Cookie': "PHPSESSID=7bb86e5db64ca692b7dd9959ce52f862; rfl=amVmOl86MTc0ODpfOmQyYjBlYTUzZDRiMTc5NDM5ZWJmODAyNzg0ZWU5MjNl; last_visit=1553443497893::1553454297893",
        'cache-control': "no-cache",
        'Postman-Token': "0eeeb98b-a58a-4b41-87a8-a7ebe83d5e31"
    }
    page = requests.request("GET", link, headers=headers)
    return json.loads(page.text)