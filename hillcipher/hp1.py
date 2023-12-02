import numpy as np
import math
import random
import re

option = 0

# Kamus Huruf ke Angka
substitusi = {
    'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7, 'I': 8, 'J': 9,
    'K': 10, 'L': 11, 'M': 12, 'N': 13, 'O': 14, 'P': 15, 'Q': 16, 'R': 17, 'S': 18,
    'T': 19, 'U': 20, 'V': 21, 'W': 22, 'X': 23, 'Y': 24, 'Z': 25, '_': 26, 'a': 27,
    'b': 28, 'c': 29, 'd': 30, 'e': 31, 'f': 32, 'g': 33, 'h': 34, 'i': 35, 'j': 36,
    'k': 37, 'l': 38, 'm': 39, 'n': 40, 'o': 41, 'p': 42, 'q': 43, 'r': 44, 's': 45,
    't': 46, 'u': 47, 'v': 48, 'w': 49, 'x': 50, 'y': 51, 'z': 52, '!': 53, '?': 54,
    '.': 55, ',': 56, '"': 57, '1': 58, '2': 59, '3': 60, '4': 61, '5': 62, '6': 63,
    '7': 64, '8': 65, '9': 66, '0': 67, '-': 68, '(': 69, ';': 70}

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
        encrypted_vector = np.dot(key_matrix, block_vector) % 71
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

    determinant = determinant % 71
    print("K^-1 : ", determinant)

    # Mencari modulo invers dari determinan
    modulo_inverse = mod_inverse(determinant, 71)

    print("Invers Modulo : ", modulo_inverse)

    if modulo_inverse is None:
        return "Determinan tidak memiliki invers modulo 71"
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
        key_matrix_inv = (adjoint_matrix * modulo_inverse) % 71

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
        decrypted_vector = np.dot(key_matrix_inv, block_vector) % 71
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
        randomtext.append(random.randint(0, 70))
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
            modulo_inverse = mod_inverse(determinant, 71)
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
        result = mod_inverse(determinant, 71)
        if result is not None:
            kunciditemukan = 1
            print('Modulo Invers dari {kunci} adalah ', result)
        else:
            rekomendasi = cekrekomendasi(kunci)
            print('Kunci Tersebut Tidak Memiliki Modulo Invers.')
            print('Rekomendasi : ', rekomendasi)
    elif (option == "4"):
        exit()
