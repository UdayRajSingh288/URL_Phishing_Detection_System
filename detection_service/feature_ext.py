from urllib.parse import urlparse, urljoin
from os.path import basename
from ipaddress import ip_address
from tld import get_tld
from requests import get
from bs4 import BeautifulSoup
from re import findall, search


def get_char_continuation_rate(url_string):
	total_length = len(url_string)
	max_letter_length = 0
	max_digit_length = 0
	max_other_length = 0

	current_letter_length = 0
	current_digit_length = 0
	current_other_length = 0

	for char in url_string:
		if 'a' <= char <= 'z' or 'A' <= char <= 'Z':
			current_letter_length += 1
			current_digit_length = 0
			current_other_length = 0
			max_letter_length = max(max_letter_length, current_letter_length)
		elif '0' <= char <= '9':
			current_digit_length += 1
			current_letter_length = 0
			current_other_length = 0
			max_digit_length = max(max_digit_length, current_digit_length)
		else:
			current_other_length += 1
			current_letter_length = 0
			current_digit_length = 0
			max_other_length = max(max_other_length, current_other_length)

	continuation_length = max_letter_length + max_digit_length + max_other_length
	return continuation_length / total_length

def get_bank(forms):
	keywords = [
		"account number", "bank name", "routing number", "credit card",
		"debit card", "cvv", "card number", "account balance",
		"transaction history", "sort code", "iban", "swift code"
	]
	for form in forms:
		for keyword in keywords:
			if keyword in form.get_text().lower():
				return 1
		for input in form.find_all("input"):
			name = input.get("name", "").lower()
			if any(keyword in name for keyword in keywords):
				return 1
			type_ = input.get("type", "").lower()
			if type_ in ["card-number", "cvc", "cvv", "pin"]:
				return 1
	return 0

def get_pay(forms):
	for form in forms:
		form_text = form.get_text().lower()
		keywords = [
			"card number", "credit card", "debit card", "cvv", "cvc",
			"expiry date", "expiration date", "cardholder name",
			"billing address", "payment information", "payment details",
			"card details", "cc number", "card type", "card brand",
			"payment method", "payment gateway"
		]
		for keyword in keywords:
			if keyword in form_text:
				return 1
		inputs = form.find_all("input")
		for input_field in inputs:
			name = input_field.get("name", "").lower()
			if any(keyword in name for keyword in keywords):
				return 1
		type_ = input_field.get("type", "").lower()
		if type_ in ["card-number", "cvc", "cvv", "pin", "month", "year"]:
                    return 1
		selects = form.find_all("select") #Check for select elements
		for select in selects:
			name = select.get("name", "").lower()
			if any(keyword in name for keyword in keywords):
				return 1
	return 0

def get_crypto(forms):
	for form in forms:
		form_text = form.get_text().lower()
		keywords = [
			"bitcoin", "ethereum", "litecoin", "dogecoin", "cryptocurrency",
			"crypto payment", "crypto address", "wallet address",
			"blockchain", "erc-20", "tron", "solana",
			"btc", "eth", "ltc", "doge"
		]
		for keyword in keywords:
			if keyword in form_text:
				return 1
		inputs = form.find_all("input")
		for input_field in inputs:
			name = input_field.get("name", "").lower()
			if any(keyword in name for keyword in keywords):
				return 1
		type_ = input_field.get("type", "").lower()
		if type_ in ["text", "hidden"]:
			if any(keyword in name for keyword in keywords):
				return 1
	return 0

def get_copyright_info(text):
        patterns = [
            r"copyright\s+(?:©|\(c\)|all rights reserved)?\s*(?:[0-9]{4}-?[0-9]{4})?\s*(.+)",
            r"©\s*[0-9]{4}\s*(.+)",
            r"all rights reserved\s*(?:[0-9]{4}\s*(.+))?",
            r"©\s*[\d{4}]",
            r"&#169;\s*[0-9]{4}",
            r"&copy;\s*[0-9]{4}",
        ]
        for pattern in patterns:
            if search(pattern, text):
                return 1
        return 0

def get_has_obfuscation(hostname, path, query, url):
	if search(r"[%+]", url):
		return 1
	if search(r"%[0-9a-fA-F]{2}", url) or search(r"\\\[0-7]{3}", url):
		return 1
	if len(path) > 50 and search(r"[^a-zA-Z0-9/]", path):
		return  1
	if len(query) > 50 and search(r"[^a-zA-Z0-9&=]", query):
		return 1
	if hostname:
		if search(r"[0-9]", hostname) and not search(r"\.", hostname):
			return 1
		top_level_domains = [".xyz", ".top", ".club", ".online", ".site", ".tech", ".info"]
		if any(tld in hostname for tld in top_level_domains):
			return 1
	return 0

def extract_features(url):
	parsed_url = None
	features = []
	try:
		parsed_url = urlparse(url)
	except ValueError:
		return None

	filename = basename(parsed_url.path)
	features.append(filename)
	#url = url
	features.append(url)
	url_length = len(url)
	features.append(url_length)
	domain = parsed_url.netloc
	features.append(domain)
	domain_length = len(domain)
	features.append(domain_length)
	is_domain_ip = 0
	try:
		ip_address(domain)
		is_domain_ip = 1
	except:
		is_domain_ip = 0
	features.append(is_domain_ip)
	tld = get_tld(url, as_object = False)
	features.append(tld)
	url_similarity_index = 100.0
	features.append(url_similarity_index)
	char_continuation_rate = get_char_continuation_rate(parsed_url.geturl())
	features.append(char_continuation_rate)
	tld_legitimate_prob = 0.5229071
	features.append(tld_legitimate_prob)
	url_char_prob = 0.057332856
	features.append(url_char_prob)
	tld_length = len(tld)
	features.append(tld_length)
	no_of_subdomain = len(domain.split('.')) - 2
	features.append(no_of_subdomain)
	has_obfuscation = get_has_obfuscation(parsed_url.netloc, parsed_url.path, parsed_url.query, url)
	features.append(has_obfuscation)
	no_of_obfuscated_char = 0
	no_of_obfuscated_char += len(findall(r"[%+]", url))
	no_of_obfuscated_char += len(findall(r"%[0-9a-fA-F]{2}", url))
	no_of_obfuscated_char += len(findall(r"\\\[0-7]{3}", url))
	no_of_obfuscated_char += len(findall(r"[0O]", url))
	no_of_obfuscated_char += len(findall(r"[1lI]", url))
	features.append(no_of_obfuscated_char)
	obfuscation_ratio = float(no_of_obfuscated_char) / float(len(url))
	features.append(obfuscation_ratio)
	no_of_letters_in_url = 0
	for ch in url:
		if ch >= 'A' and ch <= 'Z' or ch >= 'a' and ch <= 'z':
			no_of_letters_in_url += 1
	features.append(no_of_letters_in_url)
	letter_ratio_in_url = float(no_of_letters_in_url) / float(len(url))
	features.append(letter_ratio_in_url)
	no_of_digits_in_url = 0
	for ch in url:
		if ch >= '0' and ch <= '9':
			no_of_digits_in_url += 1
	features.append(no_of_digits_in_url)
	digit_ratio_in_url = float(no_of_digits_in_url) / float(len(url))
	features.append(digit_ratio_in_url)
	no_of_equals_in_url = 0
	for ch in url:
		if ch == '=':
			no_of_equals_in_url += 1
	features.append(no_of_equals_in_url)
	no_of_qmark_in_url = 0
	for ch in url:
		if ch == '?':
			no_of_qmark_in_url += 1
	features.append(no_of_qmark_in_url)
	no_of_ampersand_in_url = 0
	for ch in url:
		if ch == '&':
			no_of_ampersand_in_url += 1
	features.append(no_of_ampersand_in_url)
	no_of_other_special_characters_in_url = 0
	for ch in url:
		if not ch.isalnum():
			no_of_other_special_characters_in_url += 1
	no_of_other_special_characters_in_url -= (no_of_equals_in_url + no_of_qmark_in_url + no_of_ampersand_in_url)
	features.append(no_of_other_special_characters_in_url)
	special_char_ratio_in_url = float(no_of_other_special_characters_in_url + no_of_equals_in_url
					+ no_of_qmark_in_url + no_of_ampersand_in_url) / float(len(url))
	features.append(special_char_ratio_in_url)
	is_https = int(parsed_url.scheme == "https")
	features.append(is_https)
	response = get(url, allow_redirects = True)
	soup = BeautifulSoup(response.content, "html.parser")
	lines_of_code = 0
	for line in soup.get_text().splitlines():
		if line.strip():
			lines_of_code += 1
	features.append(lines_of_code)
	largest_line_length = 0
	for line in soup.get_text().splitlines():
		line = line.strip()
		if largest_line_length < len(line):
			largest_line_length = len(line)
	features.append(largest_line_length)
	has_title = int(soup.find("title") is not None)
	features.append(has_title)
	title = soup.find("title")
	features.append(title)
	domain_title_match_score = 100.0
	features.append(domain_title_match_score)
	url_title_match_score = 100.0
	features.append(url_title_match_score)
	has_favicon = int(soup.find("link", rel=lambda rel: rel and "icon" in rel.lower()) is not None)
	features.append(has_favicon)
	robots = int(get(urljoin(url, "/robots.txt")) is not None)
	features.append(robots)
	is_responsive = int(soup.find("meta", attrs={"name": lambda name: name and "viewport" in name.lower()}) is not None)
	features.append(is_responsive)
	no_of_url_redirect = len(response.history)
	features.append(no_of_url_redirect)
	no_of_self_redirect = 0
	if response.history:
		for redirect in response.history:
			if urlparse(redirect.url).hostname == parsed_url.hostname:
				no_of_self_redirect += 1
	features.append(no_of_self_redirect)
	has_description = int(soup.find("meta", attrs={"name": lambda name: name and "description" in name.lower()}) is not None)
	features.append(has_description)
	no_of_popup = 0
	for script in soup.find_all("script"):
		if script.string:
			no_of_popup += len(findall(r"\.open\(\s*['\"]", script.string))
			no_of_popup += len(findall(r"window\.open\(\s*['\"]", script.string))
			no_of_popup += len(findall(r"showModalDialog\(\s*['\"]", script.string))
			no_of_popup += len(findall(r"popup\s*=\s*window\.open", script.string))
			no_of_popup += len(findall(r"new\s+Window\(\s*\)", script.string))
	for element in soup.find_all(lambda tag: tag.has_attr('onclick')):
		if "window.open" in element.get('onclick').lower() or "showmodaldialog" in element.get('onclick').lower():
			no_of_popup += 1
	features.append(no_of_popup)
	no_of_iframe = len(soup.find_all("iframes"))
	features.append(no_of_iframe)
	has_external_form_submit = 0
	for form in soup.find_all("form"):
		if form.get("action"):
			if form.get("action").startswith("http://") or form.get("action").startswith("https://"):
				if parsed_url.netloc != urlparse(form.get("action")).netloc:
					has_external_form_submit = 1
					break
	features.append(has_external_form_submit)
	social_networks = [
		"facebook.com", "x.com", "instagram.com", "linkedin.com",
		"youtube.com", "pinterest.com", "tiktok.com", "snapchat.com",
		"reddit.com", "tumblr.com", "twitter.com"
        ]
	has_social_net = 0
	for link in soup.find_all("a"):
		if link.get("href"):
			if urlparse(link.get("href")).netloc and urlparse(link.get("href")).netloc.lower() in social_networks:
				has_social_net = 1
				break
	features.append(has_social_net)
	has_submit_button = int(soup.find("button", type=lambda type: type and type.lower() == "submit") is not None)
	features.append(has_submit_button)
	has_hidden_fields = int(soup.find_all("input", type=lambda type: type and type.lower() == "hidden") is not None)
	features.append(has_hidden_fields)
	has_password_field = int(soup.find_all("input", type=lambda type: type and type.lower() == "password") is not None)
	features.append(has_password_field)
	bank = get_bank(soup.find_all("form"))
	features.append(bank)
	pay = get_pay(soup.find_all("form"))
	features.append(pay)
	crypto = get_crypto(soup.find_all("form"))
	features.append(crypto)
	has_copyright_info = get_copyright_info(soup.get_text().lower())
	features.append(has_copyright_info)
	no_of_image = len(soup.find_all("image"))
	features.append(no_of_image)
	no_of_css = len(soup.find_all("link", rel=lambda rel: rel and "stylesheet" in rel.lower()))
	features.append(no_of_css)
	no_of_js = len(soup.find_all("script"))
	features.append(no_of_js)
	no_of_self_ref = 0
	for link in soup.find_all("a"):
		if link.get("href"):
			if urlparse(link.get("href")).netloc == parsed_url.netloc:
				no_of_self_ref += 1
	features.append(no_of_self_ref)
	no_of_empty_ref = 0
	for link in soup.find_all("a"):
		if link.get("href") is None and link.get("href").strip() == "":
			no_of_empty_ref += 1
	features.append(no_of_empty_ref)
	no_of_external_ref = 0
	for link in soup.find_all("a"):
		if link.get("href"):
			if urlparse(link.get("href")).netloc != parsed_url.netloc:
				no_of_external_ref += 1
	features.append(no_of_external_ref)
	return features

if __name__ == "__main__":
	features = extract_features("https://www.amazon.com/")
	print(len(features))
	print(features)

# url similarity index
# tld legitimate prob
# url char prob
# domain title match score
# url title match score