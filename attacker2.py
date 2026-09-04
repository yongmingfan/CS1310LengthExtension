import struct
import math

# ============================================================
# Provided: raw MD5 compression function.
# You do NOT need to read or modify this section.
# ============================================================

def _lrot(x, c):
    x &= 0xFFFFFFFF
    return ((x << c) | (x >> (32 - c))) & 0xFFFFFFFF

_S = [7, 12, 17, 22] * 4 + [5, 9, 14, 20] * 4 + [4, 11, 16, 23] * 4 + [6, 10, 15, 21] * 4
_K = [int(abs(math.sin(i + 1)) * 2**32) & 0xFFFFFFFF for i in range(64)]

def _compress(state, block):
    A, B, C, D = state
    M = struct.unpack("<16I", block)
    for i in range(64):
        if i < 16:
            F = (B & C) | ((~B & 0xFFFFFFFF) & D); g = i
        elif i < 32:
            F = (D & B) | ((~D & 0xFFFFFFFF) & C); g = (5 * i + 1) % 16
        elif i < 48:
            F = B ^ C ^ D; g = (3 * i + 5) % 16
        else:
            F = C ^ (B | ((~D) & 0xFFFFFFFF)); g = (7 * i) % 16
        F = (F + A + _K[i] + M[g]) & 0xFFFFFFFF
        A, D, C = D, C, B
        B = (B + _lrot(F, _S[i])) & 0xFFFFFFFF
    return [(state[j] + [A, B, C, D][j]) & 0xFFFFFFFF for j in range(4)]

def continue_md5(token_hex, data):
    """
    Resume MD5 from the internal state encoded in `token_hex`,
    and process `data` (which MUST be a multiple of 64 bytes).
    Returns the resulting hex digest.
    """
    if len(data) % 64 != 0:
        raise ValueError("data length must be a multiple of 64 bytes, got %d" % len(data))
    state = list(struct.unpack("<4I", bytes.fromhex(token_hex)))
    for i in range(0, len(data), 64):
        state = _compress(state, data[i:i + 64])
    return struct.pack("<4I", *state).hex()

def length_field(total_len_bytes):
    """
    Encode `total_len_bytes` (a byte count) as the 8-byte
    little-endian bit-length field MD5 puts at the end of its
    padding. You do NOT need to do this byte conversion by hand --
    just compute total_len_bytes on paper and call this function.
    """
    return (total_len_bytes * 8).to_bytes(8, "little")

# ============================================================
# Read the captured message and token.
# ============================================================

with open("request.txt", "r", encoding="latin-1") as f:
    lines = f.read().splitlines()

message = lines[0].split("=", 1)[1]
token = lines[1].split("=", 1)[1]

print("=== Captured Message and Token ===")
print("Message (%d bytes):" % len(message))
print(message)
print()
print("Token:", token)
print()

# ============================================================
# Known facts for this exercise:
#   SECRET_LEN = 5   (already determined, e.g. from Part 1)
#   You want to inject APPEND into the message.
# ============================================================

SECRET_LEN = 5
APPEND = "&admin=true"

# ============================================================
# STUDENT TODO
#
# Recall MD5's padding rule: given TOTAL_LEN bytes of real data,
# MD5 appends:
#   1. one 0x80 byte
#   2. some 0x00 bytes
#   3. the 8-byte little-endian encoding of (TOTAL_LEN * 8)
#
# To find out how many 0x00 bytes are needed, figure out how many
# bytes of real data fall into the block that is not yet full:
#
#   LEFTOVER = TOTAL_LEN - (number of full 64-byte blocks already used) * 64
#
# Then:
#   zero_count = 64 - LEFTOVER - 1 - 8
#   (this works whenever LEFTOVER <= 55, which is always true in
#   this exercise)
#
# ---- Part A: ORIGINAL_PADDING ----
# This is the padding MD5 added after `secret + message` when
# the client computed `token`.
#   TOTAL_LEN = SECRET_LEN + len(message) = 5 + 85 = 90
#   90 bytes = one full block (64 bytes) + 26 leftover bytes,
#   so LEFTOVER = 90 - 64 = 26.
# Work out zero_count on paper, then fill in:
#   ORIGINAL_PADDING = b"\x80" + b"\x00" * zero_count + length_field(TOTAL_LEN)
#
# ---- Part B: NEW_PADDING ----
# This is the padding YOU need in order to keep hashing forward
# from the token: it is the padding that would be required after
# `secret + message + ORIGINAL_PADDING + APPEND`
#   TOTAL_LEN = SECRET_LEN + len(message) + len(ORIGINAL_PADDING) + len(APPEND)
#   Once ORIGINAL_PADDING is correct, secret + message + ORIGINAL_PADDING
#   is exactly 2 full blocks (128 bytes) -- so LEFTOVER for this part
#   is just len(APPEND).
# Work this out on paper the same way, then fill in:
#   NEW_PADDING = b"\x80" + b"\x00" * zero_count + length_field(TOTAL_LEN)
#
# IMPORTANT: NEW_PADDING is used ONLY to let you continue the MD5
# computation locally (see resume_data below). It is NOT written
# into the forged message sent to the server -- server.py calls
# hashlib.md5(SECRET + message) itself, and hashlib automatically
# appends this exact same padding when it hashes. If you were to
# also write NEW_PADDING into the forged message, the server would
# end up padding twice and verification would fail.
#
# The two placeholders below already have the CORRECT LENGTH
# (38 bytes and 53 bytes) so the code will run without crashing --
# but every byte is currently wrong, so the forged token will NOT
# be valid yet, and server.py will print "Authentication FAILED".
#
# Your job: replace each placeholder with
#   b"\x80" + b"\x00" * <your zero_count> + length_field(<your TOTAL_LEN>)
# keeping the TOTAL number of bytes in each variable unchanged.
#
# If you DO change the length of either variable, the checks below
# will catch it immediately and tell you exactly what's wrong.
# ============================================================


# TODO: fix the length_field(...) argument (and double-check the zero-count)
ORIGINAL_PADDING = b"\x80" + b"\x00" * 29 + length_field(0)

# TODO: fix the length_field(...) argument (and double-check the zero-count)
NEW_PADDING = b"\x80" + b"\x00" * 44 + length_field(0)


# ============================================================
# Do not modify anything below this line.
# ============================================================

expected_original_total = SECRET_LEN + len(message) + len(ORIGINAL_PADDING)
if expected_original_total % 64 != 0:
    raise ValueError(
        "ORIGINAL_PADDING has the wrong length.\n"
        "SECRET_LEN(%d) + len(message)(%d) + len(ORIGINAL_PADDING)(%d) = %d,\n"
        "which is not a multiple of 64. Recheck your padding calculation."
        % (SECRET_LEN, len(message), len(ORIGINAL_PADDING), expected_original_total)
    )

resume_data = APPEND.encode("latin-1") + NEW_PADDING

expected_new_total = expected_original_total + len(resume_data)
if expected_new_total % 64 != 0:
    raise ValueError(
        "NEW_PADDING has the wrong length.\n"
        "Previous total(%d) + len(APPEND)(%d) + len(NEW_PADDING)(%d) = %d,\n"
        "which is not a multiple of 64. Recheck your padding calculation."
        % (expected_original_total, len(APPEND), len(NEW_PADDING), expected_new_total)
    )

new_token = continue_md5(token, resume_data)

# NOTE: NEW_PADDING is deliberately NOT included here. The server
# will apply the equivalent padding itself when it hashes
# SECRET + forged_message, via hashlib.md5(). NEW_PADDING was only
# needed above, in resume_data, so that YOU could correctly continue
# the MD5 computation to get new_token.
forged_message = (
    message
    + ORIGINAL_PADDING.decode("latin-1")
    + APPEND
)

with open("request.txt", "w", encoding="latin-1") as f:
    f.write("message=" + forged_message + "\n")
    f.write("token=" + new_token + "\n")

print("=== Forged Message and Token ===")
print("Message (%d bytes):" % len(forged_message))
print(repr(forged_message))
print()
print("Token:", new_token)
print()
print("Forged message and token saved to request.txt")
