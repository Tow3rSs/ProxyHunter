# ProxyHunter
Powerful HTTPS SOCKS4 / 5 Proxy Hunter

This is not the average proxy checker that simply pings the proxy to show you if it's up or not. 
ProxyHunter uses system threading to download a sample file to test every proxy individually. This ensures valid results.
It consists of 4 separate pyhton modules that can run individually as needed or a single bash script to automate the process.

HOW TO USE:

IMPORTANT! ProxyHunter does not check for HTTP proxies, meaning that only proxies capable of connecting to the server hosting the sample file via HTTPS will pass the check. By the way the connection to the proxy from your PC is always made via simple HTTP, meaning that in both input and output files you won't find any https even if all checked proxies support it.

You can run the script ProxyHunter.sh to retrieve proxylist from proxyscape.com or you can add your proxies to check to the file stuff.txt before starting the script. (format ip:port or protocol://ip:port with protocol = http, socks4 or socks5 NOT https!)
parser.py will exctract all ip's from the file, you can paste your own list or directly the HTML code of a web page containing the proxies. Even just higliting the whole page, copying and pasting it in .txt will work.

NOTE: ProxyHunter works by downloading a sample file and it needs to know what kind of protocol the proxy uses. So every proxy inserted in the form ip:port without protocol will be also checked for that and this takes some extra time.

Tested on Kali Linux 2024.1



      

           



