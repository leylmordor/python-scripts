# Import the required modules
import os
import urllib.request

# Read the URL path from the text file
with open('url_path.txt') as f:
    url_paths = f.readlines()

# Set the bearer token
bearer_token = 'YOUR_BEARER_TOKEN'

# Loop through the URL paths
for url_path in url_paths:
    # Strip the leading and trailing whitespace from the URL path
    url_path = url_path.strip()

    # Construct the full URL
    url = 'https://www.example.com/' + url_path

    # Create the destination directory if it doesn't exist
    destination_dir = 'downloads'
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    # Set the request headers
    headers = {
        'Authorization': 'Bearer ' + bearer_token
    }

    # Create the request object
    request = urllib.request.Request(url, headers=headers)

    # Download the file and save it to the destination directory
    destination_path = os.path.join(destination_dir, url_path)
    urllib.request.urlretrieve(request, destination_path)

