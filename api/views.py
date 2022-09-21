from rest_framework.response import Response
from rest_framework.decorators import api_view

import requests
from bs4 import BeautifulSoup

__BASE__ = 'https://isitcom.rnu.tn'

@api_view(['GET'])
def news(request, page):
    data =[]

    response = requests.get(f'{__BASE__}/fra/articles/categorie/p/{page}/2/actualites-de-lisitcom')

    soup = BeautifulSoup(response.text, 'lxml')

    articles = soup.find('div', {'class': 'content'}).find_all('div', {'class': 'newsList'})

    for article in articles:
        img = article.find('img')['src']
        if img[:len(__BASE__)] != __BASE__ :
            img = __BASE__ + '/' + img
        data.append({
            'title': article.find('div', {'class': 'sub_title'}).findChild().text.strip(),
            'slug': article.find('a')['href'][36:],
            'img': img
        })
    return Response(data)

@api_view(['GET'])
def article(request, id, slug):
    data = {}
    urls = []

    response = requests.get(f'{__BASE__}/fra/articles/{id}/{slug}')

    soup = BeautifulSoup(response.text, 'lxml')


    title = soup.find('div', {"class" : "title"})

    links = soup.find('div', {'class': 'desc'}).find_all('a')

    for link in links:
        urls.append({
            'title': link.text.strip(),
            'url': __BASE__ + link["href"]
        })

    data['title'] = title.text.strip()
    data['links'] = urls

    if data['title'] != '' and data['links'] != '':
        return Response(data)
    else:
        return Response('Article invalid', status=400)