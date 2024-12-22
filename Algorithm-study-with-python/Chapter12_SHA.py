from passlib.hash import sha512_crypt

sha512_crypt.using(salt = 'qIo0fox5', rounds=5000).hash("myPassword")

myHash = sha512_crypt.using(salt = "qIo0foX5", rounds=5000).hash("myPassword")
print(myHash)
