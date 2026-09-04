with open("request.txt", "r") as f:
    lines = f.read().splitlines()

message = lines[0].split("=", 1)[1]
token = lines[1].split("=", 1)[1]

print("=== Original Message and Token ===")
print()
print("Message:")
print(message)

print()
print("Token:")
print(token)

# ==========================================================
# STUDENT TODO
#
# You are the attacker.
#
# Modify the message to obtain administrator access.
# You do not know the secret, so you cannot simply
# calculate a new valid token.
#
# Keep the original token unchanged.
# ==========================================================

ADD_TO_MESSAGE = ""

# ==========================================================
# Do not modify anything below this line.
# ==========================================================

modified_message = message + ADD_TO_MESSAGE

with open("request.txt", "w") as f:
    f.write("message=" + modified_message + "\n")
    f.write("token=" + token + "\n")

print()
print("=== Modified Message and Token ===")
print()
print("Message:")
print(modified_message)

print()
print("Token:")
print(token)

print()
print("Modified message and original token saved to request.txt")
