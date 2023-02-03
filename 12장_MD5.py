from passlib.hash import md5_crypt

myHash = md5_crypt.hash("myPassword", salt = 'xE2')
print(myHash)

print(md5_crypt.verify('myPassword', myHash))