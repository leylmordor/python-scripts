import requests
import urllib.parse
import threading

def check_xss(url, method, payload, stored=False):
    try:
        if method == 1: # GET
            if stored:
                r = requests.get(url + payload.strip())
            else:
                r = requests.get(url + urllib.parse.quote(payload.strip()))
        elif method == 2: # POST
            if stored:
                r = requests.post(url, data={'payload': payload.strip()})
            else:
                r = requests.post(url, data={'payload': urllib.parse.quote(payload.strip())})
        else:
            print("[-] Invalid request method")
            return

        if payload.strip() in r.text:
            print(f"[+] XSS vulnerability found in {url} with payload: {payload.strip()}")
    except Exception as e:
        print(f"[-] Exception occured: {e}")

def run_checks(url, method, payloads, stored):
    threads = []
    for payload in payloads:
        t = threading.Thread(target=check_xss, args=(url, method, payload, stored))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

url = input("Enter the URL to test: ")
method = int(input("Enter the request method (1 for GET, 2 for POST): "))
payloads_file = input("Enter the path to the payloads file: ")
stored = input("Check for stored XSS? (y/n)").lower() == 'y'

try:
    with open(payloads_file, 'r') as f:
        payloads = f.readlines()
except Exception as e:
    print(f"[-] Exception occured while reading payloads file: {e}")
    payloads = []

run_checks(url, method, payloads, stored)