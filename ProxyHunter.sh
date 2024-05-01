#!/bin/bash

echo "
------------------------------------------------------------------
    ____                      _   _             _            
   |  _ \ _ __ _____  ___   _| | | |_   _ _ __ | |_ ___ _ __  ®
   | |_) | '__/ _ \ \/ / | | | |_| | | | | '_ \| __/ _ \ '__|
   |  __/| | | (_) >  <| |_| |  _  | |_| | | | | ||  __/ |   
   |_|   |_|  \___/_/\_\ __, |_| |_|\__,_|_| |_|\__\___|_|   
                        |___/

               Powerful HTTPS SOCKS4/5 Proxy Hunter

 Press Enter to start.                                By Tow3rSs.
------------------------------------------------------------------
"
touch IPs.txt > IPs.txt && touch parsed_type.txt > parsed_type.txt && touch checked_type.txt > checked_type.txt

echo -e "\033[93m\033[1m[i]\033[0m Check your internet connection before proceeding."
printf "\033[96m\033[1m[+]\033[0m Download and check proxies from proxyscrape? [Y/n] -> " && read input
#read -p "[+] Download and check proxies from proxyscrape? [Y/n] -> " input

if [ "$input" == "n" ]; then

printf "\033[93m\033[1m[i]\033[0m ProxyHunter will now extract all IP's from file stuff.txt. Make sure it's populated." && read input2
echo ""

python3 parser.py && python3 type.py && cat parsed_type.txt checked_type.txt > type.txt && python3 checker.py && sort -u Working_Proxies.txt > Sorted_Working_Proxies.txt

else

python3 Hunter.py && python3 checker.py && sort -u Working_Proxies.txt > Sorted_Working_Proxies.txt

fi
