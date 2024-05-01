import subprocess
import threading
import queue
import math
import re

RED = '\033[91m'
CYAN = '\033[96m'
GREEN = '\033[92m'
RESET = '\033[0m'
BOLD = '\033[1m'

print("")
print(GREEN + BOLD + "[i]" + RESET + " Running proxy checker for only protocol IP proxies...")

print(GREEN + BOLD + "[i]" + RESET + " Proxy check will be performed trying to download a sample file from a remote server\n    at https://freetestdata.com/wp-content/uploads/2021/09/Free_Test_Data_2MB_MP3.mp3.")

askuser = input(CYAN + BOLD + "[+]" + RESET + " Do you want to use a custom download link? [y/N] -> ")
if (askuser == "y"):
    link = input(CYAN + BOLD + "[+]" + RESET + " Paste the link: ") 
    sample_size = input(CYAN + BOLD + "[+]" + RESET + " Insert the size of the custom file in bytes -> ")
else: 
    link = "https://freetestdata.com/wp-content/uploads/2021/09/Free_Test_Data_2MB_MP3.mp3"
    sample_size = 2104472 

selected_threads = input(CYAN + BOLD + "[+]" + RESET + " Number of threads for simultaneous checking [300] -> ")
if selected_threads == "":
    selected_threads = 300
if (int(selected_threads) > 300):
    input(RED + BOLD + "[!]" + RESET + " WARNING: Using more than 300 threads might make the script unstable.")

m = input(CYAN + BOLD + "[+]" + RESET + " Set max time for each proxy download [25] -> ")
if (m == ""): m = 25

r = input(CYAN + BOLD + "[+]" + RESET + " Set the max number of connection retries [1] -> ")    
if (r == ""): r = 1

rdelay = input(CYAN + BOLD + "[+]" + RESET + " Set retry delay [5] -> ")
if (rdelay == ""): rdelay = 5

def read_urls_from_file(file_path):
    urls = []
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()  
            if line: 
                urls
                urls.append(line)
    return urls

file_path = 'type.txt'  
proxies = read_urls_from_file(file_path)

expected_time = ((int(m)*(int(r)+1) + int(rdelay)*int(r)) * math.ceil(len(proxies) / int(selected_threads)))

print("")
print(GREEN + BOLD + "[i]" + RESET + " Parsed " + str(len(proxies)) + f" proxies, starting proxy check... This might take up to {expected_time} sec.\n")

def test_proxy_speed(proxy, result_queue):
    cmd = f"curl -o /home/kali/ignore.txt --silent --max-time {m} --retry-delay {rdelay} --retry {r} --write-out '%{{speed_download}} %{{size_download}}' --preproxy {proxy} {link}"
    try:
        output = subprocess.check_output(cmd, shell=True, text=True, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        return None, None

    match = re.match(r"([\d.]+) ([\d.]+)", output)
    if match:
        download_speed = 8 * float(match.group(1)) / (1024 * 1024)
        download_size = int(match.group(2))
     
        if download_size == int(sample_size):
            result_queue.put(proxy)
            print(CYAN + BOLD + "[*]" + RESET + f" {proxy} - Speed: {download_speed:.2f} Mb/s")
        else: ()
    else:
        print(RED + BOLD + "[!]" + RESET + " Failed to parse output:", output)

def test_proxies(proxies):
    result_queue = queue.Queue()
    threads = []
    max_threads = int(selected_threads)

    for proxy in proxies:
        if threading.active_count() <= max_threads:
            thread = threading.Thread(target=test_proxy_speed, args=(proxy, result_queue))
            thread.start()
            threads.append(thread)
        else:
            for thread in threads:
                thread.join()
            threads = []
            thread = threading.Thread(target=test_proxy_speed, args=(proxy, result_queue))
            thread.start()
            threads.append(thread)

    for thread in threads:
        thread.join()

    results = []
    while not result_queue.empty():
        results.append(result_queue.get())

    return results

tested_proxies = test_proxies(proxies)

def create_text_file(file_name, data_list):
    try:
        with open(file_name, 'w') as file:
            for item in data_list:
                file.write(str(item) + '\n')
        print(GREEN + BOLD + "[i]" + RESET + f" File '{file_name}' created successfully.")
    except Exception as e:
        print(RED + BOLD + "[!]" + RESET + f" Error during file generation: {e}")

print("")
print(GREEN + BOLD + "[i]" + RESET + f" Done!, Found {len(tested_proxies)} working proxies.")
create_text_file('Working_Proxies.txt', tested_proxies)

