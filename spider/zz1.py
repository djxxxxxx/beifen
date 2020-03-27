import requests
from lxml import etree
import json

def get_page(url, headers):
    html = requests.get(url, headers=headers)
    return html.text
    
def parse_page(html):
    html = etree.HTML(html)
    items = html.xpath('//div[@class="cell item"]')
    for item in items:
        res = {
            'title': item.xpath('.//td[3]/span[1]/a/text()'),
            'author': item.xpath('.//td[3]/span[2]/strong[1]/a/text()')
            }
        yield res

def main():
    url = 'https://v2ex.com/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537'
            +'.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
            }
    html = get_page(url, headers)
    item = parse_page(html)
    with open('data.json', 'a') as f:
        f.write("[\n")
        for i in item:
            for i in item:
                f.write(json.dumps(i, ensure_ascii=None))
                f.write(',\n')
        f.write("]")
        
if __name__ == '__main__':
    main()
