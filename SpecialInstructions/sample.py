import numpy as np

state = np.uint32(0x92d68ca2)
def xorshift():
    global state
    state ^= np.uint32(state << 13);
    state ^= np.uint32(state >> 17);
    state ^= np.uint32(state << 15);
    return np.uint32(state);

flag = "6d72c3e2cf95549db6ac0384c3c23593c3d77ce2ddd4ac5e99c9a534de064e00".decode("hex")
r = "3d05dc31d18aaf2996facb1b01ece2f715706cf47ea19e0e01f9c24cbaa0a108".decode("hex")

s = ""
for i, c in enumerate(flag):
    if c == "\x00":
        break
    xorshift()
    s += chr((ord(c) ^ ord(r[i]) ^ state) & 0xff)
print s