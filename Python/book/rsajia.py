import rsa

message = "1989sct"
public_key, private_key = rsa.newkeys(2048)
# public_key, private_key = rsa.newkeys(1024)
print(public_key)
print(private_key)
encrypted_message = rsa.encrypt(message.encode('iso8859-1'), public_key)
decrypted_message = rsa.decrypt(encrypted_message, private_key)
print(encrypted_message, decrypted_message, sep="\n\n")
print(decrypted_message.decode('i0000000000000so8859-1'))

print(encrypted_message.decode("iso8859-1").encode("utf-8"))
