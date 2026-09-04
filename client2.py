import hashlib

SECRET = b"XY123"  # 5 bytes

BASE_MESSAGE = "user=student&action=view"
FILLER = "0" * (85 - len(BASE_MESSAGE))
message = BASE_MESSAGE + FILLER  # always exactly 85 characters

token = hashlib.md5(SECRET + message.encode("latin-1")).hexdigest()

with open("request.txt", "w", encoding="latin-1") as f:
    f.write("message=" + message + "\n")
    f.write("token=" + token + "\n")

print("Message (%d bytes):" % len(message))
print(message)
print()
print("Token:")
print(token)
print()
print("Message and token saved to request.txt")
