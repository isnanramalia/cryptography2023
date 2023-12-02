# ENIGMA MACHINE 1 1930

# Contoh pada komentar menggunakan settingan
# plain text = KELAS UG
# posisi ring = A K U
# plugboard = AX BR KF LG


# Caesar cipher (untuk memutar rotor sesuat notch )
def caesarShift(str, amount):
    output = ""
    # perulangan untuk memutar rotor
    for i in range(0, len(str)):
        char = str[i]
        code = ord(char)
        # pengkondisian sesuai ascii untuk alphabet
        if ((code >= 65) and (code <= 90)):
            # menambahkan alphabet rotor dengan index Notch,
            # contoh rotor = B(1) ditambah index Notch = U(20), hasilnya V(21) *dimulai dari index 0*
            char = chr(((code - 65 + amount) % 26) + 65)
        output = output + char
    # print(output) #hasil setelah diputar
    return output


def encode(plaintext):
    # ----------------- Enigma Settings -----------------
    rotors = ("I", "II", "III")
    reflector = "UKW-B"
    ringPositions = input("Masukkan Posisi Ring \t: ")
    plugboard = input("Masukkan Plugboard \t: ")
    # ---------------------------------------------------

    # mengubah ke Huruf Kapital
    ringPositions = ringPositions.upper()
    plugboard = plugboard.upper()

    # inisialisasi Enigma Rotor dan reflector
    rotor1 = "EKMFLGDQVZNTOWYHXUSPAIBRCJ"
    rotor1Notch = "Q"
    rotor2 = "AJDKSIRUXBLHWTMCQGZNPYFVOE"
    rotor2Notch = "E"
    rotor3 = "BDFHJLCPRTXVZNYEIWGAKMUSQO"
    rotor3Notch = "V"
    rotor4 = "ESOVPZJAYQUIRHXLNFTGKDCMWB"
    rotor4Notch = "J"
    rotor5 = "VZBRGITYUPSDNHLXAWMJQOFECK"
    rotor5Notch = "Z"

    # definisi rotor dan Notch
    rotorDict = {"I": rotor1, "II": rotor2,
                 "III": rotor3, "IV": rotor4, "V": rotor5}
    rotorNotchDict = {"I": rotor1Notch, "II": rotor2Notch,
                      "III": rotor3Notch, "IV": rotor4Notch, "V": rotor5Notch}

    # inisialisasi Reflektor B dan C
    reflectorB = {"A": "Y", "Y": "A", "B": "R", "R": "B", "C": "U", "U": "C", "D": "H", "H": "D", "E": "Q", "Q": "E", "F": "S", "S": "F",
                  "G": "L", "L": "G", "I": "P", "P": "I", "J": "X", "X": "J", "K": "N", "N": "K", "M": "O", "O": "M", "T": "Z", "Z": "T", "V": "W", "W": "V"}
    reflectorC = {"A": "F", "F": "A", "B": "V", "V": "B", "C": "P", "P": "C", "D": "J", "J": "D", "E": "I", "I": "E", "G": "O", "O": "G",
                  "H": "Y", "Y": "H", "K": "R", "R": "K", "L": "Z", "Z": "L", "M": "X", "X": "M", "N": "W", "W": "N", "Q": "T", "T": "Q", "S": "U", "U": "S"}

    # inisialisasi Alphabet dan  rotor False(belum diputar)
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    rotorANotch = False
    rotorBNotch = False
    rotorCNotch = False

    # pengkondisian cek reflektor yang dipakai UKW-B atau UKW-C
    if reflector == "UKW-B":
        reflectorDict = reflectorB
    else:
        reflectorDict = reflectorC

    # A = Left(rotor 1),  B = Mid(rotor 2),  C=Right(rotor 3)
    # inisialisasi Rotor dengan jenis rotor yang dipilih("I","II","III")
    rotorA = rotorDict[rotors[0]]
    rotorB = rotorDict[rotors[1]]
    rotorC = rotorDict[rotors[2]]

    # inisialisasi Notch sesuai jenis yang dipilih("I","II","III")
    rotorANotch = rotorNotchDict[rotors[0]]
    rotorBNotch = rotorNotchDict[rotors[1]]
    rotorCNotch = rotorNotchDict[rotors[2]]

    # inisialisasi posisi ring sesuai yang diinputkan
    rotorALetter = ringPositions[0]
    rotorBLetter = ringPositions[1]
    rotorCLetter = ringPositions[2]

    # print(rotorA)
    # print(rotorB)
    # print(rotorC)

    ciphertext = ""

    # mengubah setting kedalam kamus
    plugboardConnections = plugboard.upper().split(" ")
    plugboardDict = {}
    for pair in plugboardConnections:
        if len(pair) == 2:
            plugboardDict[pair[0]] = pair[1]
            plugboardDict[pair[1]] = pair[0]

    plaintext = plaintext.upper()
    for letter in plaintext:
        encryptedLetter = letter

        # print(encryptedLetter)
        if letter in alphabet:
            # putar Rotor - Terjadi saat keyboard/input ditekan, sebelum melakukan enkripsi
            rotorTrigger = False
            # rotor ketiga akan berputar 1 langkah untuk setiap ditekan
            if rotorCLetter == rotorCNotch:
                rotorTrigger = True
            rotorCLetter = alphabet[(alphabet.index(rotorCLetter) + 1) % 26]
            # Melakukan pengecekan jika rotor B(2) perlu pemutaran
            if rotorTrigger:
                rotorTrigger = False
                if rotorBLetter == rotorBNotch:
                    rotorTrigger = True
                rotorBLetter = alphabet[(
                    alphabet.index(rotorBLetter) + 1) % 26]

                # melakukan pengecekan jika rotor A(1) perlu pemutaran
                if (rotorTrigger):
                    rotorTrigger = False
                    rotorALetter = alphabet[(
                        alphabet.index(rotorALetter) + 1) % 26]

            else:
                # melakukan pengecekan ganda
                if rotorBLetter == rotorBNotch:
                    rotorBLetter = alphabet[(
                        alphabet.index(rotorBLetter) + 1) % 26]
                    rotorALetter = alphabet[(
                        alphabet.index(rotorALetter) + 1) % 26]

            # mengimplementasikan plugboard
            if letter in plugboardDict.keys():
                if plugboardDict[letter] != "":
                    encryptedLetter = plugboardDict[letter]
            # print("plug")
            # print(encryptedLetter)

            # Rotor dan Reflektor enkripsi!
            offsetA = alphabet.index(rotorALetter)
            offsetB = alphabet.index(rotorBLetter)
            offsetC = alphabet.index(rotorCLetter)

            # Rotor 3
            pos = alphabet.index(encryptedLetter)
            let = rotorC[(pos + offsetC) % 26]
            pos = alphabet.index(let)
            encryptedLetter = alphabet[(pos - offsetC + 26) % 26]
            # print("wheel 3")
            # print(encryptedLetter)

            # Rotor 2
            pos = alphabet.index(encryptedLetter)
            let = rotorB[(pos + offsetB) % 26]
            pos = alphabet.index(let)
            encryptedLetter = alphabet[(pos - offsetB + 26) % 26]
            # print("wheel 2")
            # print(encryptedLetter)

            # Rotor 1
            pos = alphabet.index(encryptedLetter)
            let = rotorA[(pos + offsetA) % 26]
            pos = alphabet.index(let)
            encryptedLetter = alphabet[(pos - offsetA + 26) % 26]
            # print("wheel 1")
            # print(encryptedLetter)

            # Reflektor
            if encryptedLetter in reflectorDict.keys():
                if reflectorDict[encryptedLetter] != "":
                    encryptedLetter = reflectorDict[encryptedLetter]
            # print("reflector")
            # print(encryptedLetter)

            # kembali ke rotor
            # rotor 1
            pos = alphabet.index(encryptedLetter)
            let = alphabet[(pos + offsetA) % 26]
            pos = rotorA.index(let)
            encryptedLetter = alphabet[(pos - offsetA + 26) % 26]
            # print("wheel 1")
            # print(encryptedLetter)

            # rotor 2
            pos = alphabet.index(encryptedLetter)
            let = alphabet[(pos + offsetB) % 26]
            pos = rotorB.index(let)
            encryptedLetter = alphabet[(pos - offsetB + 26) % 26]
            # print("wheel 2")
            # print(encryptedLetter)

            # rotor 3
            pos = alphabet.index(encryptedLetter)
            let = alphabet[(pos + offsetC) % 26]
            pos = rotorC.index(let)
            encryptedLetter = alphabet[(pos - offsetC + 26) % 26]
            # print("wheel 3")
            # print(encryptedLetter)

            # Implementasi Plugboard
            if encryptedLetter in plugboardDict.keys():
                if plugboardDict[encryptedLetter] != "":
                    encryptedLetter = plugboardDict[encryptedLetter]
            # print("plug")
            # print(encryptedLetter)
        ciphertext = ciphertext + encryptedLetter

    return ciphertext


# Main Program Dimulai Disini
def main():
    while (True):
        choice = input(
            "---------------Enkripsi Engima---------------\n1. Enkripsi\n2. Dekripsi\n3. Keluar\npilih : ")
        match choice:
            case "1":
                plaintext = input("Masukkan plain text \t: ")
                print("\nCipher text: \n " + encode(plaintext))
            case "2":
                plaintext = input("Masukkan Cipher text \t: ")
                print("\nPlaint text: \n " + encode(plaintext))
            case "3":
                exit()


if __name__ == "__main__":
    main()
