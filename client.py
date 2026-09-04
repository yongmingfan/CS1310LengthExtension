import hashlib

SECRET = b"campuskey"

message = "user=student&action=view"

token = hashlib.md5(SECRET + message.encode()).hexdigest()

with open("request.txt", "w") as f:
    f.write("message=" + message + "\n")
    f.write("token=" + token + "\n")

print("Message:")
print(message)
print()
print("Token:")
print(token)
print()
print("Message and token saved to request.txt")
