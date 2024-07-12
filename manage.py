#!/usr/bin/env python3
import requests
from sys import argv

"""
Create super user script

How to use:
---------------------------------------------------------------
python3 manage.py <firstname> <lastname> <email> <password>
---------------------------------------------------------------
Defaults <Admin> <HR> <admin@alx.com> <1234567890>
---------------------------------------------------------------
"""

firstname = argv[1] if len(argv) > 1 else "Admin"
lastname = argv[2] if len(argv) > 2 else "HR"
email = argv[3] if len(argv) > 3 else "admin@alx.com"
password = argv[4] if len(argv) > 4 else "1234567890"

payload = {
    "firstname": firstname,
    "lastname": lastname,
    "email": email,
    "password": password,
    "role": "admin"
}

url = "http://127.0.0.1:3000/auth/register"

response = requests.post(url, data=payload)

print(response.text)
