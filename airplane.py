import requests
from bs4 import BeautifulSoup
import warnings

def get_star(airplane):
    url = airplane.replace(' ', '+').replace('&', '')
    res = requests.get('https://flight-report.com/en/airline/?q=%s' % url)
    html = res.text
    css = "#airlines>div>article>div:last-child>div:first-child>span"

    bs = BeautifulSoup(html, 'html.parser')
    element = bs.select(css)
    names = [i.text for i in bs.select('h3>a>span[itemprop=name]')]

    if not element:
        raise Exception("Invalid airplane name")

    starList = []
    
    for airplanes in element:
        gs = 0
        for i in airplanes.findAll('i'):
            cls = i['class']
            stars = 0
            for i in cls:
                if i == 'empty-star': break
                if i == 'icon-star': stars += 1
                if i == 'icon-star-half': stars += 0.5

            gs += stars
        starList.append(int(gs * 2))
    
    if len(starList) == 1:
        return {"name": names[0], "stars": starList[0]}
    else:
        return [{"name": names[i], "stars": starList[i]} for i in range(len(starList))]

