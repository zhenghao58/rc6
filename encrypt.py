def ROR(x, n, bits = 16):
    mask = (2L**n) - 1
    mask_bits = x & mask
    return (x >> n) | (mask_bits << (bits - n))

# rotate left input x, by n bits
def ROL(x, n, bits = 16):
    return ROR(x, bits - n,bits)

def zero(x):
    if len(x) <4:
        x = "0"*(4-len(x)) + x
    return x

def encrypt(sentence, s):

    A = long(sentence[:4], 16)
    B = long(sentence[4:8], 16)
    C = long(sentence[8:12], 16)
    D = long(sentence[12:], 16)
    orgi = []
    orgi.append(A)
    orgi.append(B)
    orgi.append(C)
    orgi.append(D)
    r = 20
    modulo = 2 ** 16
    lgw = 4
    B = (B + s[0]) % modulo
    D = (D + s[1]) % modulo
    for i in range(1, r + 1):
        t_temp = (B * (2 * B + 1)) % modulo
        t = ROL(t_temp, lgw, 16)
        u_temp = (D * (2 * D + 1)) % modulo
        u = ROL(u_temp, lgw, 16)
        tmod = t % 16
        umod = u % 16
        A = (ROL(A ^ t, umod, 16) + s[2 * i]) % modulo
        C = (ROL(C ^ u, tmod, 16) + s[2 * i + 1]) % modulo
        (A, B, C, D) = (B, C, D, A)

    A = (A + s[2 * r + 2]) % modulo
    C = (C + s[2 * r + 3]) % modulo
    ahex = hex(A)[2:].replace("L", "")
    bhex = hex(B)[2:].replace("L", "")
    chex = hex(C)[2:].replace("L", "")
    dhex = hex(D)[2:].replace("L", "")
    cipher = []
    cipher.append(zero(ahex))
    cipher.append(zero(bhex))
    cipher.append(zero(chex))
    cipher.append(zero(dhex))
    cipherStr = cipher[0] + cipher[1] + cipher[2] + cipher[3]
    return orgi, cipher, cipherStr


def main():
    # print "ENCRYPTION: "

    s = ["B7E1", "0DF9", "720A", "4825", "6665", "EB0A", "5AB9", "2521", "14AA", "18DD", "35ED", "88EA", "64D1", "A589",
         "8BCA", "FDD5", "6DB5", "4B4A", "7429", "1131", "BF6A", "2D0D", "C7BD", "2A2A", "B6C1", "FA19", "378A", "AC85",
         "CE05", "BD8A", "00E2", "451C", "CE72", "263A", "A43C", "C67A", "AF32", "471C", "2622", "2B4A", "4D88", "BD4E",
         "7A9C", "F538"]
    for i in range(0, len(s)):
        s[i] = long(s[i], 16)
    sentence = "0001000200030004"
    fc = open("rc6_ct.txt", "w")
    fp = open("rc6_pt.txt", "w")
    fk = open("rc6_key.txt", "w")
    for i in range(1, 10001):
        fp.write(sentence + "\n")
        orgi, cipher, cipherStr = encrypt(sentence, s)
        cipherStr = str(cipherStr).replace("L", "")
        sentence = cipherStr
        # print "Original String list: ", orgi
        # print "Length of Input String: ", len(sentence)
        # print "\nEncrypted String: ", cipherStr
        # print "\nEncrypted String list: ", cipher
        fc.write(cipherStr+"\n")
        fk.write("0000"+"\n")
    fc.close()
    fk.close()
    fp.close()


if __name__ == "__main__":
    main()
