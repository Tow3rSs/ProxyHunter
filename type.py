import subprocess
import threading
import queue
import math

RED = '\033[91m'
CYAN = '\033[96m'
GREEN = '\033[92m'
RESET = '\033[0m'
BOLD = '\033[1m'

print(GREEN + BOLD + "[i]" + RESET + " Running proxy protocol checker for only IP proxies...")

http = []
socks4 = []
socks5 = []

def read_urls_from_file(file_path):
    urls = []
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line: 
                urls
                urls.append(line)
    return urls

file_path = 'IPs.txt' 
proxies = read_urls_from_file(file_path)

expected_time = (165 * math.ceil(len(proxies) / 300))

print(GREEN + BOLD + "[i]" + RESET + " Parsed " + str(len(proxies)) + f" proxies, starting proxy analisys... This might take up to {expected_time} sec.\n")

def proxy_type(proxy, result_queue):

    commanda = f'curl -o /home/kali/ignore.txt --silent --max-time 15 --retry-delay 5 --retry 2 --write-out "%{{size_download}}" --proxy {"http://" + proxy} https://check-host.net/ip' #HTTPS proxy must be accessed as HTTP
    processa = subprocess.Popen(commanda, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    outputa, errora = processa.communicate()
    if (processa.returncode == 0 and int(outputa.decode()) < 18 and int(outputa.decode()) > 6): 
        result_queue.put(proxy)
        print(CYAN + BOLD + "[*]" + RESET + f" HTTPS {proxy}")
        http.append("http://" + proxy)
    else: () 

    commandb = f'curl -o /home/kali/ignore.txt --silent --max-time 15 --retry-delay 5 --retry 2 --write-out "%{{size_download}}" --preproxy {"socks4://" + proxy} https://check-host.net/ip'
    processb = subprocess.Popen(commandb, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    outputb, errorb = processb.communicate()
    if (processb.returncode == 0 and int(outputb.decode()) < 18 and int(outputb.decode()) > 6):
        result_queue.put(proxy)
        print(CYAN + BOLD + "[*]" + RESET + f" SOCKS4 {proxy}")
        socks4.append("socks4://" + proxy)
    else: ()

    commandc = f'curl -o /home/kali/ignore.txt --silent --max-time 15 --retry-delay 5 --retry 2 --write-out "%{{size_download}}" --preproxy {"socks5://" + proxy} https://check-host.net/ip'
    processc = subprocess.Popen(commandc, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    outputc, errorc = processc.communicate()
    if (processc.returncode == 0 and int(outputc.decode()) < 18 and int(outputc.decode()) > 6):
        result_queue.put(proxy)
        print(CYAN + BOLD + "[*]" + RESET + f" SOCKS5 {proxy}")
        socks5.append("socks5://" + proxy)
    else: ()

def test_proxies(proxies):
    result_queue = queue.Queue()
    threads = []
    max_threads = 300

    for proxy in proxies:
        if threading.active_count() <= max_threads:
            thread = threading.Thread(target=proxy_type, args=(proxy, result_queue))
            thread.start()
            threads.append(thread)
        else:
            for thread in threads:
                thread.join()
            threads = []
            thread = threading.Thread(target=proxy_type, args=(proxy, result_queue))
            thread.start()
            threads.append(thread)

    for thread in threads:
        thread.join()

    results = []
    while not result_queue.empty():
        results.append(result_queue.get())

    return results

tested_proxies = test_proxies(proxies)
results = http + socks4 + socks5

def create_text_file(file_name, data_list):
    try:
        with open(file_name, 'w') as file:
            for item in data_list:
                file.write(str(item) + '\n')
        print(GREEN + BOLD + "[i]" + RESET + f" Protocol proxies successfully added to '{file_name}'.")
    except Exception as e:
        print(RED + BOLD + "[!]" + RESET + f" Error during file generation: {e}")

print(GREEN + BOLD + "[i]" + RESET + f" Done!, Found {len(results)} available proxy protocols.")
create_text_file('checked_type.txt', results)

