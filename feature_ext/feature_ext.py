from urllib.parse import urlparse
from os.path import basename
from ipaddress import ip_address
from tld import get_tld
from requests import get
from bs4 import BeautifulSoup
from re import findall

def get_dataset_features(url):
	try:
		parsed_url = urlparse(url)
	except ValueError:
		return None
	filename = basename(parsed_url.path)
	# url
	url_length = len(url)
	domain = parsed_url.netloc
	domain_length = len(domain)
	is_domain_ip = int(ip_address(domain))
	tld = get_tld(url, as_object = True)
	# url_similarity_index = 90
	# char_continuation_rate = 0.9
	# tld_legitimate_prob = 0.9
	# url_char_prob = 
	tld_length = len(tld)
	no_of_subdomain = len(domain.split('.')) - 2
	has_obfuscation = 
	no_of_obfuscated_char = 
	obfuscation_ratio = 
	no_of_letters_in_url = 0
	for ch in url:
		if ch >= 'A' and ch <= 'Z' or ch >= 'a' and ch <= 'z':
			no_of_letters_in_url += 1
	no_of_digits_in_url = 0
	for ch in url:
		if ch >= '0' and ch <= '9':
			no_of_digits_in_url += 1
	digit_ratio_in_url = float(no_of_digits_in_url) / float(len(url))
	no_of_equals_in_url = 0
	for ch in url:
		if ch == '=':
		no_of_equals_in_url += 1
	no_of_qmark_in_url = 0
	for ch in url:
		if ch == '?':
		no_of_qmark_in_url += 1
	no_of_ampersand_in_url = 0
	for ch in url:
		if ch == '&':
		no_of_ampersand_in_url += 1
	no_of_other_special_characters_in_url = 0
	for ch in url:
		if not ch.isalnum():
			no_of_other_special_characters_in_url += 1
	no_of_other_special_characters_in_url -= (no_of_equals_in_url + no_of_qmark_in_url + no_of_ampersand_in_url)
	special_char_ratio_in_url = float(no_of_other_special_characters_in_url + no_of_equals_in_url
					+ no_of_qmark_in_url + no_of_ampersand_in_url) / float(len(url))
	is_https = int(parsed_url.scheme == "https")
	response = get(url, allow_redirects = True)
	soup = BeautifulSoup(response.content, "html.parser")
	html_text = soup.get_text()
	lines_of_code = 0
	for line in html_text.splitlines():
		if line.strip():
			lines_of_code += 1
	largest_line_length = 0
	for line in html_text.splitlines():
		line = line.strip()
		if largest_line_length < len(line):
			largest_line_length = len(line)
	has_title = int(soup.find("title") is not None)
	title = soup.find("title")
	# domain_title_match_score = 0.9
	# url_title_match_score = 0.9
	has_favicon = int(soup.find("link", rel=lambda rel: rel and "icon" in rel.lower()) is not None)
	robots = int(get(urljoin(url, "/robots.txt")) is not None)
	is_responsive = int(soup.find("meta", attrs={"name": lambda name: name and "viewport" in name.lower()}) is not None)
	no_of_url_reditrect = len(response.history)
	no_of_self_reditrect = 0
	if response.history:
		initial_hostname = parsed_url.hostname
		for redirect in response.history:
			redirect_hostname = urlparse(redirect.url).hostname
			if initial_hostname == redirect_hostname:
				no_of_self_redirect += 1
	has_description = int(soup.find("meta", attrs={"name": lambda name: name and "description" in name.lower()}) is not None)
	no_of_popup = 0
	script_tags = soup.find_all("script")
	for script in script_tags:
		if script.string:
			script_content = script.string
			no_of_popup += len(findall(r"\.open\(\s*['\"]", script_content))
			no_of_popup += len(findall(r"window\.open\(\s*['\"]", script_content))
			no_of_popup += len(findall(r"showModalDialog\(\s*['\"]", script_content))
			no_of_popup += len(findall(r"popup\s*=\s*window\.open", script_content))
			no_of_popup += len(findall(r"new\s+Window\(\s*\)", script_content))
	elements_with_onclick = soup.find_all(lambda tag: tag.has_attr('onclick'))
	for element in elements_with_onclick:
		on_click_content = element.get('onclick').lower()
		if "window.open" in onclick_content or "showmodaldialog" in onclick_content:
			no_of_popup += 1
	no_of_ifrmae = len(soup.find_all("iframes"))
	has_external_form_submit = 0
	forms = soup.find_all("form")
	for form in forms:
		action = form.get("action")
		if action:
			if action.startswith("http://") or action.startswith("https://"):
				action_url = urlparse(action)
				if parsed_url.netloc != action_url:
					has_external_form_submit = 1
					break
	social_networks = [
		"facebook.com", "x.com", "instagram.com", "linkedin.com",
		"youtube.com", "pinterest.com", "tiktok.com", "snapchat.com",
		"reddit.com", "tumblr.com", "twitter.com"
        ]
	has_social_net = 0
	links = soup.find_all("a")
	for link in links:
		href = link.get("href")
		if href:
			parsed_href = urlparse(href)
			if parsed_href.netloc and parsed_href.netloc.lower() in social_networks:
				has_social_net = 1
				break
	has_submit_button = int(soup.find("button", type=lambda type: type and type.lower() == "submit") is not None)
	has_hidden_fields = int(soup.find_all("input", type=lambda type: type and type.lower() == "hidden") is not None)
	has_password_field = int(soup.find_all("input", type=lambda type: type and type.lower() == "password") is not None)
	bank = 0
	keywords = [
		"account number", "bank name", "routing number", "credit card",
		"debit card", "cvv", "card number", "account balance",
		"transaction history", "sort code", "iban", "swift code"
	]
	for form in forms:
		form_text = form.get_text().lower()
		for keyword in keywords:
			if keyword in form_text:
				bank = 1
				break
		inputs = form.find_all("input")
		for input in inputs:
			name = input.get("name", "").lower()
			if any(keyword in name for keyword in keywords):
				bank = 1
				break
			type_ = input.get("type", "").lower()
			if type_ in ["card-number", "cvc", "cvv", "pin"]:
				bank = 1
				break
	pay = 0
	for form in forms:
		form_text = form.get_text().lower()
		for keyword in keywords:
			if keyword in form_text
	crypto = 
	has_copyright_info = 
	no_of_image = len(soup.find_all("image"))
	no_of_css = len(soup.find_all("link", rel=lambda rel: rel and "stylesheet" in rel.lower()))
	no_of_js = len(soup.find_all("script"))
	no_of_self_ref = 0
	for link in links:
		href = link.get("href")
		if href:
			parsed_href = urlparse(href)
			if parsed_href.netloc == parsed_url.netloc:
				no_of_self_ref += 1
	no_of_empty_ref = 0
	for link in links:
		href = link.get("href")
		if href is None and href.strip() == "":
			no_of_empty_ref += 1
	no_of_external_ref = 0
	for link in links:
		href = link.get("href")
		if href:
			parsed_href = urlparse(href)
			if parsed_href.netloc != parsed_url.netloc:
				no_of_external_ref += 1