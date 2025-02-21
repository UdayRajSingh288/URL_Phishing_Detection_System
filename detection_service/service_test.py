from requests import post

r = post('http://127.0.0.1:8080', json = {'url': 'https://google.com'})
print(r.text)