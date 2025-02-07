from cryptography.fernet import Fernet

key = b'08snHLRwosIsOoMQR6I8x_ppif1l_MSxdLaHRkNCG-U='
suite = Fernet(key)
t = suite.encrypt(b'testing1')
print(t)