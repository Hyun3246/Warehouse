import cryptography as crypt
from cryptography.fernet import Fernet
from cryptography.fernet import Fernet

key = Fernet.generate_key()
print(key)

file = open("mykey.key", 'wb')
file.write(key)
file.close()

file = open("mykey.key", 'rb')
key = file.read()
file.close()

message = "Ottawa is really cold".encode()

f = Fernet(key)
encrypted = f.encrypt(message)

decrypted = f.decrypt(encrypted)

print(decrypted)
