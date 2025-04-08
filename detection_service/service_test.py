from requests import post


if __name__ == '__main__':
	url = input('Enter URL: ')
	while url != 'stop':
		r = post('http://127.0.0.1:8080', json = {'url': url})
		print(r.text)
		url = input('Enter URL: ')