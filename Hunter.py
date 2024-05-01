import requests
import re

RED = '\033[91m'
CYAN = '\033[96m'
GREEN = '\033[92m'
RESET = '\033[0m'
BOLD = '\033[1m'

downloaded = []

timeout = input(CYAN + BOLD + "[+]" + RESET + " Maximum proxy timeout (ms) [15000] -> ")
if timeout == "":
    timeout = 15000

def extract_ips_from_text(text):
    ip_pattern = r'(\b(?:socks4|socks5|http|https)://(?:\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):(?:\d+)\b)'
    return re.findall(ip_pattern, text)

def retrieve_ips_from_website(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return extract_ips_from_text(response.text)
        else:
            print(RED + BOLD + "[!]" + RESET + " Error, server returned code != 200.")
            return []
    except requests.exceptions.RequestException as e:
        print(RED + BOLD + "[!]" + RESET + " Error:", e)
        return []


website_url = f"https://api.proxyscrape.com/v3/free-proxy-list/get?request=displayproxies&protocol=all&country=all&anonymity=all&timeout={timeout}&proxy_format=protocolipport&format=text"  # Replace with the URL of the website you want to retrieve IPs from
ips = retrieve_ips_from_website(website_url)

for ip in ips:
    downloaded.append(ip)

def create_text_file(file_name, data_list):
    try:
        with open(file_name, 'w') as file:
            for item in data_list:
                file.write(str(item) + '\n')
        print(GREEN + BOLD + "[i]" + RESET + f" Scraped proxies successfully added to '{file_name}'.")
    except Exception as e:
        print(RED + BOLD + "[!]"+ RESET + f" Error: {e}")

print(GREEN + BOLD + "[i]" + RESET + f" Scraped " + GREEN + BOLD + str(len(downloaded)) + RESET + " proxies.")

create_text_file('type.txt', downloaded)
