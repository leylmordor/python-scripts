#You can Generate your Favorite password with a word that you like (If you want) 

import secrets
import string

random_word = input("Enter a random word(s) (optional): ").strip()
password_length = int(input("Enter the desired password length (> 24): "))

random_word = random_word.replace(" ", "")
# Generate a string of all uppercase and lowercase letters, digits, and special characters
characters = string.ascii_letters + string.digits + r"!@#$%^&*()_+-=[]{}\|;:'\"<>,.?/~`"

# Check if the password length is at least 20 characters
if password_length < 24:
  raise ValueError("Password length should be at least 24 characters")

# Check if the random word is not longer than 6 characters
if random_word and len(random_word) > 10:
  raise ValueError("Random word should be no longer than 10 characters")

# Generate a random password using the secrets module
password = "".join(secrets.choice(characters) for i in range(password_length))

# Insert the random word at a random index in the password
if random_word:
  index = secrets.randbelow(password_length)
  password = password[:index] + random_word + password[index:]

print(f"Generated password: {password}")