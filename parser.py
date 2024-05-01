import re

RED = '\033[91m'
CYAN = '\033[96m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RESET = '\033[0m'
BOLD = '\033[1m'

print(GREEN + BOLD + "[i]" + RESET + " Running Parser...")

input_file = "stuff.txt"

ips = []

def protocol_parser(filename):
    urls = []
    with open(filename, 'r') as file:
        for line in file:
            url_matches = re.findall(r'(https?|socks[45]?):\/\/([^\/\s:]+)(?::(\d+))?', line)
            for match in url_matches:
                protocol, ip, port = match
                if port:
                    url = f"{protocol}://{ip}:{port}"
                    ips.append(ip + ":" + port)
                else: 
                    url = f"{protocol}://{ip}"
                urls.append(url)
    return urls

def crude_ip_parser(file_path):
    ip_port_pattern = r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s+(\d{1,5})'
    ip_port_list = []

    with open(file_path, 'r') as file:
        for line in file:
            matches = re.findall(ip_port_pattern, line)
            for match in matches:
                ip_port_list.append(match[0] + ":" + match[1]) 

    return ip_port_list

def html_parser(html_code):
    pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b.*?:\d{2,5}'
    matches = re.findall(pattern, html_code)
    return matches

def read_html_from_file(filename):
    with open(filename, 'r') as file:
        return file.read()


html_code = read_html_from_file(input_file)
ip_ports = html_parser(html_code)

ip_port_list = []

for ip_port in ip_ports:
    ip, port = re.findall(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', ip_port)[0], re.findall(r':\d{2,5}', ip_port)[0][1:]
    ip_port_list.append(f"{ip}:{port}")


protocol_proxies = protocol_parser(input_file)

def copy_http_elements(input_list):
    http_elements = []
    for element in input_list:
        if element.startswith("https://"):
            http_elements.append(element.replace("https://", "http://"))
        else: http_elements.append(element)        
    return http_elements

def create_text_file(file_name, data_list):
    try:
        with open(file_name, 'w') as file:
            for item in data_list:
                file.write(str(item) + '\n')
    except Exception as e:
        print(RED + BOLD + "[!]"+ RESET + f" Error: {e}")

stripped_protocol = copy_http_elements(protocol_proxies)

sub1 = [item for item in ip_port_list if item not in ips] 

crude_proxies = crude_ip_parser(input_file)

sub2 = [item2 for item2 in crude_proxies if item2 not in ips]

just_ip = sub1 + sub2

if len(just_ip) > 0:
    print(GREEN + BOLD + "[i]" + RESET + f" Parsed " + GREEN + BOLD + str(len(just_ip)) + RESET + " generic proxies.")
    create_text_file('IPs.txt', just_ip)

else: 
    print(YELLOW + BOLD + "[i]" + RESET + f" Parsed " + YELLOW + BOLD + "0" + RESET + " generic proxies.")

if len(protocol_proxies) > 0:
    print(GREEN + BOLD + "[i]" + RESET + f" Parsed " + GREEN + BOLD + str(len(protocol_proxies)) + RESET + " proxies with protocol.")
    create_text_file('parsed_type.txt', stripped_protocol)

else:
    print(YELLOW + BOLD + "[i]" + RESET + f" Parsed " + YELLOW + BOLD + "0" + RESET + " proxies with protocol.")

print("")


