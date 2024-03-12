from cryptography.fernet import Fernet

key = Fernet.generate_key() #this is your "password"
cipher_suite = Fernet(key)
encoded_text = cipher_suite.encrypt(b"Hello stackoverflow!")
print(encoded_text)
decoded_text = cipher_suite.decrypt(encoded_text)
print(decoded_text.decode("utf-8"))