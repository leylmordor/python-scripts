import zipfile

# Open the zip file
with zipfile.ZipFile('protected.zip', 'r') as zip_file:
    # Try different passwords until one works - update the name for the dictionary
    with open('dictionary.txt', 'r') as password_file:
        for line in password_file:
            password = line.strip()
            try:
                zip_file.extractall(pwd=password)
                print(f'Password found: {password}')
                break
            except Exception:
                pass
    print('Password not found in dictionary')
