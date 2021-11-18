from db import db
from flask import session

def login(username, password) -> boolean:
    # testikäyttäjä
    if username == "testi" and password == "salasana":
        return True
    return False