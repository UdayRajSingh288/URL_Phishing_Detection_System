from requests import post

d = {
	'email': 'udayrajsingh288@gmail.com',
	'password': 'Qwer1234%',
	'url': 'https://google.com'
}

r = post('http://127.0.0.1:8000/testURL/', json = d)
print(r.text)