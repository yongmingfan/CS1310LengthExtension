import hashlib

SECRET = b"campuskey"

with open("request.txt", "r") as f:
    lines = f.read().splitlines()

message = lines[0].split("=", 1)[1]
token = lines[1].split("=", 1)[1]

expected_token = hashlib.md5(SECRET + message.encode()).hexdigest()

print("Message:")
print(message)
print()
print("Token:")
print(token)
print()

if token != expected_token:
    print("Authentication FAILED")
else:
    print("Authentication SUCCESS")
    if "admin=true" in message:
        print("Administrator access granted.")
    else:
        print("Normal user access granted.")
