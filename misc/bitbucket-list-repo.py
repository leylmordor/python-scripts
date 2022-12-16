import requests

org_name = "yourBitbucketOrgName"
headers = {
    'Authorization': 'Bearer XXXXXYXXXX',
    'Accept': 'application/json',
}
api_endpoint = f'https://api.bitbucket.org/2.0/repositories/{org_name}/?pagelen=100&page=2'
response = requests.get(api_endpoint, headers=headers)

if response.status_code != 200:
    print("An error occurred while trying to retrieve the repositories")
else:
    # Print the names of the repositories
    repos = response.json()["values"]
    for repo in repos:
        print(repo["name"])
