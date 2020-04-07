from tornado.httpclient import HTTPClient

def synchronous_fetch(url):
    http_client = HTTPClient()
    response = http_client.fetch(url)
    return response.body

res = synchronous_fetch('https://cocktail8.com')
print(res)
