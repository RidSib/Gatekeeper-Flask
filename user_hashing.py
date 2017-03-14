from werkzeug.security import generate_password_hash, \
     check_password_hash
from passlib.hash import sha256_crypt

class User(object):

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)
    


password = sha256_crypt.encrypt("test")
password2 = sha256_crypt.encrypt("test")

print(password)
print(password2)

print(sha256_crypt.verify("test", '$5$rounds=80000$myG4z08w1h.l5MyD$F3Yb7p4zG3LvZKzAaOwvut/BkoiH1f8WW4kzIpjCQaD'))

