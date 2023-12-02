import numpy as np
import math
import random
import re

option = 0

# Kamus Huruf ke Angka
substitusi = {
    'A': 0, 'a': 1, 'B': 2, 'b': 3, 'C': 4, 'c': 5, 'D': 6, 'd': 7, 'E': 8, 'e': 9, 'F': 10, 'f': 11,
    'G': 12, 'g': 13, 'H': 14, 'h': 15, 'I': 16, 'i': 17, 'J': 18, 'j': 19, 'K': 20, 'k': 21, 'L': 22,
    'l': 23, 'M': 24, 'm': 25, 'N': 26, 'n': 27, 'O': 28, 'o': 29, 'P': 30, 'p': 31, 'Q': 32, 'q': 33,
    'R': 34, 'r': 35, 'S': 36, 's': 37, 'T': 38, 't': 39, 'U': 40, 'u': 41, 'V': 42, 'v': 43, 'W': 44,
    'w': 45, 'X': 46, 'x': 47, 'Y': 48, 'y': 49, 'Z': 50, 'z': 51,
    '0': 52, '1': 53, '2': 54, '3': 55, '4': 56, '5': 57, '6': 58, '7': 59, '8': 60, '9': 61,
    '.': 62, '/': 63, '?': 64, '!': 65, '_': 66, '@': 67, ',': 68, ':': 69, ';': 70, '-': 71, '=': 72, '+': 73, '*': 74, '&': 75, '^': 76, '%': 77, '$': 78,
    '#': 79, '@': 80, '!': 81, '(': 82, ')': 83, '{': 84, '}': 85, '[': 86, ']': 87,
    '<': 88, '>': 89, '|': 90, '\\': 91, '`': 92, '~': 93, "'": 94, '"': 95}

# Membalik Variabel Substitusi menjadi "Angka : Huruf" || 0 : 'A' dst.
inverse_substitution = {angka: huruf for huruf, angka in substitusi.items()}


def encrypt(plain_text, key_matrix):
    # Convert Plain Text ke Huruf Besar
    plain_text = plain_text

    # Merubah karakter Spasi menjadi simbol "_"
    plain_text = plain_text.replace(" ", "_")

    # Menghilangkan karakter selain yang ada di variabel substitusi
    hasil = ""

    for i in plain_text:
        if i in substitusi:
            hasil += i

    plain_text = hasil

    # Jika panjang Plain Text tidak sekelipatan dengan besar matriks kita tambahkan huruf 'X'
    # Jika matriksnya 2x2, contoh : "BA MB AN G" maka akan dirubah menjadi "BA MB AN GX"
    # Jika matriksnya 3x3, contoh : "BAM BAN G" maka akan dirubah menjadi "BAM BAN GXX"
    if len(plain_text) % len(key_matrix) != 0:
        padding_length = len(key_matrix) - (len(plain_text) % len(key_matrix))
        plain_text += 'X' * padding_length

    # Tempat untuk menyimpan Cipher Text
    cipher_text = ''

    print('Plain Text Bersih : ', plain_text)
    print('Key Matrix : \n', key_matrix)

    # Looping Enkripsi
    for i in range(0, len(plain_text), len(key_matrix)):
        # Mengambil plaintext huruf ke i sampai i + len(key_matrix)
        block = plain_text[i:i+len(key_matrix)]

        # Konversi plaintext menjadi angka.
        block_vector = np.array([substitusi[text] for text in block])
        print("\nPlaintext : ", block_vector)

        # Perkalian Vector, kemudian di modulokan 27. 26 dari alphabet 1 untuk karakter spasi.
        # encrypted_vector = np.dot(block_vector, key_matrix) % 27
        encrypted_vector = np.dot(key_matrix, block_vector) % 96
        print("Ciphertext : ", encrypted_vector)

        # Konversi Angka ke Huruf
        encrypted_block = ''.join([inverse_substitution[num]
                                  for num in encrypted_vector])
        print("Ciphertext : ", encrypted_block)

        # Cipher Text ditampung di variabel bernama cipher_text
        cipher_text += encrypted_block

    return cipher_text

# Fungsi untuk mencari modulo invers


def mod_inverse(a, m):
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None


def decrypt(cipher_text, key_matrix):

    # Convert Cipher Text ke Huruf Besar
    cipher_text = cipher_text

    # Mencari determinan dengan menggunakan numpy, kemudian angkanya di bulatkan.
    determinant = int(np.round(np.linalg.det(key_matrix)))
    print("\nDeterminan : ", determinant)

    determinant = determinant % 96
    print("K^-1 : ", determinant)

    # Mencari modulo invers dari determinan
    modulo_inverse = mod_inverse(determinant, 96)

    print("Invers Modulo : ", modulo_inverse)

    if modulo_inverse is None:
        return "Determinan tidak memiliki invers modulo 96"
    else:
        # Membuat variabel penampung baru, besarnya sama seperti key_matrix.
        # Jika key_matrix berukuran 3x3, maka adjoint_matrix akan berukuran 3x3 juga.
        adjoint_matrix = np.zeros_like(key_matrix, dtype=np.int64)

        # key_matrix.shape isinya yaitu ukuran matriks.
        # Jika key_matrix berukuran 3x3, maka key_matrix.shape akan bernilai [3,3]
        for i in range(key_matrix.shape[0]):
            for j in range(key_matrix.shape[1]):
                # Axis 0 artinya baris, Axis 1 artinya kolom.
                # Untuk mendapatkan sub_matrix, kita menghapus baris dan kolom pada matriks itu.
                # Contoh : 2 1 1 | Misal pada posisi pertama i = 0 ; j = 0, kita akan menghapus
                #          3 5 2 | baris dan kolom "2" menyisakan | 5 2 | sebagai sub_matrix nya.
                #          3 3 3 |                                | 3 3 |
                sub_matrix = np.delete(
                    np.delete(key_matrix, i, axis=0), j, axis=1)
                # Kemudian, mencari determinan dari sub_matrix tersebut.
                cofactor = int(np.round(np.linalg.det(sub_matrix)))
                # Melihat apakah i+j ganjil/genap. Jika i+j ganjil, maka angka didepan menjadi "1"
                # Jika i+j genap, maka angka didepan menjadi "-1"
                adjoint_matrix[j, i] = ((-1) ** (i + j)) * cofactor

        # Mencari Kunci Matriks Invers dengan mengalikan adjoint_matrix dengan Modulo Invers dan di modulo 27.
        key_matrix_inv = (adjoint_matrix * modulo_inverse) % 96

    # Tempat untuk menyimpan Plain Text hasil dekripsi
    plain_text = ''

    # Looping Dekripsi
    for i in range(0, len(cipher_text), len(key_matrix)):
        # Mengambil Cipher Text huruf ke i sampai i + len(key_matrix)
        block = cipher_text[i:i+len(key_matrix)]

        # Konversi Cipher Text menjadi angka.
        block_vector = np.array([substitusi[text] for text in block])
        print("\nCiphertext : ", block_vector)

        # Dekripsi dengan mengalikan matriks kunci invers dengan vektor ciphertext
        # decrypted_vector = np.dot(block_vector, key_matrix_inv) % 27
        decrypted_vector = np.dot(key_matrix_inv, block_vector) % 96
        print("Plaintext : ", decrypted_vector)

        # Konversi vektor hasil dekripsi menjadi huruf
        decrypted_block = ''.join([inverse_substitution[num]
                                  for num in decrypted_vector])
        print("Plaintext : ", decrypted_block)

        # Plain Text ditampung di variabel bernama plain_text
        plain_text += decrypted_block

    # Mengreplace karakter "_" dengan spasi " ".
    return plain_text.replace('_', ' ')


def buatkeymatrix(string_input):
    # Menghitung panjang string
    panjang_string = len(string_input)

    # Menghitung ukuran matriks m x m
    m = int(math.sqrt(panjang_string))

    # Memastikan bahwa panjang string sesuai dengan ukuran matriks m x m
    if m * m != panjang_string:
        print("Panjang string tidak cocok dengan ukuran matriks m x m.")
        return
    else:
        # Membuat matriks m x m dengan huruf dari string input
        key_matrix = np.array([substitusi[text]
                              for text in string_input]).reshape(m, m)

        return key_matrix


def generatekey(panjang):
    randomtext = []
    # Mengulang berdasarkan panjang yang diinginkan
    for i in range(panjang):
        # Menghasilkan angka acak dari 0-26, kemudian disimpan kedalam array.
        randomtext.append(random.randint(0, 26))
    # Mengubah angka menjadi huruf sesuai substitusi.
    randomtext_array = np.array(
        [inverse_substitution[text] for text in randomtext])
    # Mengabungkan array menjadi satu string utuh.
    result = ''.join(randomtext_array)

    return result


def cekrekomendasi(kunci):
    result = ""
    cek = 0

    # Looping berdasarkan panjang kunci.
    for i in range(len(kunci)):
        # Looping mencoba kombinasi huruf sebanyak 10000 kali.
        for j in range(10000):
            # Menghasilkan huruf untuk mengreplace bagian belakang.
            huruf = generatekey(i+1)
            # Menghapus string belakang yang kemudian di replace oleh huruf random.
            text = kunci[0:len(kunci)-i-1] + huruf
            # Mengubah text menjadi matriks m x m
            text_vector = np.array([substitusi[huruf] for huruf in text]).reshape(
                int(math.sqrt(len(text))), int(math.sqrt(len(text))))
            # Mencari Determinan
            determinant = int(np.round(np.linalg.det(text_vector)))
            # Mencari Modulo Invers
            modulo_inverse = mod_inverse(determinant, 96)
            # Jika Modulo Invers Ditemukan, return result. cek = 1 untuk keluar dari looping.
            if modulo_inverse is not None:
                result = text
                cek = 1
            if cek == 1:
                break
        if cek == 1:
            break
    return result


while (option != "1" or option != "2" or option != "3"):
    option = input(
        '\nHill Cipher\n1. Encrypt\n2. Decrypt\n3. Cek Kunci\n4. Exit\nInput : ')

    if (option == "1"):
        plain_text = input('Insert Plain Text : ')
        kunci = input('Insert Kunci : ')
        kunci = kunci.replace(' ', '_')
        key_matrix = buatkeymatrix(kunci)
        if key_matrix is None:
            break
        cipher_text = encrypt(plain_text, key_matrix)
        print("\nCipher Text : ", cipher_text)
    elif (option == "2"):
        cipher_text = input('Insert Cipher Text : ')
        kunci = input('Insert Kunci : ')
        kunci = kunci.replace(' ', '_')
        key_matrix = buatkeymatrix(kunci)
        if key_matrix is None:
            break
        plain_text_decrypted = decrypt(cipher_text, key_matrix)
        print("\nPlain Text : ", plain_text_decrypted)
    elif (option == "3"):
        kunci = input('Insert Kunci : ')
        kunci = kunci.replace(' ', '_')
        key_matrix = buatkeymatrix(kunci)
        if key_matrix is None:
            break
        determinant = int(np.round(np.linalg.det(key_matrix)))
        result = mod_inverse(determinant, 96)
        if result is not None:
            kunciditemukan = 1
            print('Modulo Invers dari {kunci} adalah ', result)
        else:
            rekomendasi = cekrekomendasi(kunci)
            print('Kunci Tersebut Tidak Memiliki Modulo Invers.')
            print('Rekomendasi : ', rekomendasi)
    elif (option == "4"):
        exit()
