# SUPER ENSKRIPSI HILL CHIPER --> TRANSPOSISI SPIRAL
import string
import math
import numpy as np
import random

spasi = "_"
akhirHill = "@"
akhirSpiral = "ദ"

substitusi = {
    'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7, 'I': 8, 'J': 9, 'K': 10, 'L': 11, 'M': 12,
    'N': 13, 'O': 14, 'P': 15, 'Q': 16, 'R': 17, 'S': 18, 'T': 19, 'U': 20, 'V': 21, 'W': 22, 'X': 23, 'Y': 24, 'Z': 25,
    'a': 26, 'b': 27, 'c': 28, 'd': 29, 'e': 30, 'f': 31, 'g': 32, 'h': 33, 'i': 34, 'j': 35, 'k': 36, 'l': 37, 'm': 38,
    'n': 39, 'o': 40, 'p': 41, 'q': 42, 'r': 43, 's': 44, 't': 45, 'u': 46, 'v': 47, 'w': 48, 'x': 49, 'y': 50, 'z': 51,
    '0': 52, '1': 53, '2': 54, '3': 55, '4': 56, '5': 57, '6': 58, '7': 59, '8': 60, '9': 61,
    '.': 62, '/': 63, '?': 64, '!': 65, '_': 66, '@': 67, ',': 68, ':': 69, ';': 70, '-': 71, '=': 72, '+': 73, '*': 74,
    '&': 75, '^': 76, '%': 77, '$': 78, '#': 79, '(': 80, ')': 81, '{': 82, '}': 83, '[': 84, ']': 85, '<': 86, '>': 87,
    '|': 88, '\\': 89, '`': 90, '~': 91, "'": 92, '"': 93
}

panjang_subs = len(substitusi)

# Membalik Variabel Substitusi menjadi "Angka : Huruf" || 0 : 'A' dst.
inverse_substitution = {angka: huruf for huruf, angka in substitusi.items()}

# Fungsi untuk mencari modulo invers


def mod_inverse(a, m):
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None


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
        randomtext.append(random.randint(0, panjang_subs-1))
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
            modulo_inverse = mod_inverse(determinant, panjang_subs)
            # Jika Modulo Invers Ditemukan, return result. cek = 1 untuk keluar dari looping.
            if modulo_inverse is not None:
                result = text
                cek = 1
            if cek == 1:
                break
        if cek == 1:
            break
    return result


def cek_kunci():
    kunci = input('Insert Kunci : ')
    kunci = kunci.replace(' ', '_')
    key_matrix = buatkeymatrix(kunci)
    if key_matrix is None:
        return
    determinant = int(np.round(np.linalg.det(key_matrix)))
    result = mod_inverse(determinant, panjang_subs)
    if result is not None:
        kunciditemukan = 1
        print('Modulo Invers dari {kunci} adalah ', result)
    else:
        rekomendasi = cekrekomendasi(kunci)
        print('Kunci Tersebut Tidak Memiliki Modulo Invers.')
        print('Rekomendasi : ', rekomendasi)


def hill_encript():
    plain_text = input("Masukkan plain text: ")
    key = (input("Masukkan key :"))

    key_matrix = buatkeymatrix(key)

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
        plain_text += akhirHill * padding_length

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
        encrypted_vector = np.dot(key_matrix, block_vector) % 94
        print("Ciphertext : ", encrypted_vector)

        # Konversi Angka ke Huruf
        encrypted_block = ''.join([inverse_substitution[num]
                                  for num in encrypted_vector])
        print("Ciphertext : ", encrypted_block)

        # Cipher Text ditampung di variabel bernama cipher_text
        cipher_text += encrypted_block

    return cipher_text

# Encryption


def spiral_encrypt(plain_text):  # Fungsi untuk enkripsi
    # Menghitung akar kuadrat dari panjang plain text
    square_root = math.sqrt(len(plain_text))

    # Pembulatan ke atas akar kuadrat untuk mendapatkan ukuran langkah yang dibutuhkan
    rounded_step_size = math.ceil(square_root)

    # Menggunakan ukuran langkah yang dibulatkan sebagai ukuran matriks yang akan digunakan
    step_size = rounded_step_size

    matrix_representation = (
        []
    )  # Matriks kosong untuk menyimpan representasi matriks dari teks
    encrypted_text = ""  # Teks terenkripsi
    print("Panjang Matrix nya (m x m) : ", step_size)

    for i in range(step_size):  # Mengisi matriks dengan karakter dari teks
        matrix_row = []  # Baris matriks
        # Loop ini akan mengulangi sebanyak kolom yang diperlukan dalam matriks, dan jumlah kolom dihitung dengan
        # membagi panjang teks (len(plain_text)) dengan step_size, dan menggunakan math.ceil()
        # untuk memastikan hasil pembagian dibulatkan ke atas agar semua karakter teks dapat masuk.
        for j in range(step_size):
            index = (
                j * step_size
                + i  # j = indeks kolom saat ini, step_size = jumlah baris, i = indeks baris saat ini
            )  # Indeks karakter yang akan dimasukkan ke dalam baris matriks
            if index < len(
                plain_text
            ):  # Jika masih ada karakter yang tersisa, masukkan karakter ke dalam baris matriks
                matrix_row.append(
                    plain_text[index]
                )  # Masukkan karakter ke dalam baris matriks
            else:  # Jika tidak ada karakter yang tersisa, masukkan karakter '@' ke dalam baris matriks
                # Masukkan karakter '@' ke dalam baris matriks
                matrix_row.append(akhirSpiral)
        matrix_representation.append(
            matrix_row
        )  # Masukkan baris matriks ke dalam matriks representasi

    print("Matrix:\n")  # Tampilkan matriks representasi
    for row in matrix_representation:  # Untuk setiap baris dalam matriks representasi
        print(row)  # Tampilkan baris

    # proses enkripsi
    matrix_height = step_size  # Tinggi matriks
    matrix_width = step_size  # Lebar matriks
    mid = step_size // 2  # Nilai Tengah matriks
    x1 = 0  # Inisiasi banyaknya step/isi matrix

    for i in range(mid):  # Looping sebanyak setengah matriks
        if step_size % 2 == 0:  # Perulangan ketika `step_size`/panjang matriks genap
            # Loop untuk mengambil elemen matriks dan menambahkannya ke teks terenkripsi, Bergerak keatas dengan mid + i sebagai nilai awal dan mid - i - 1 sebagai nilai akhir dan -1 digunakan untuk mengakomodasi perubahan arah pergerakan ke atas dalam matriks.
            for x in range(mid + i, mid - i - 1, -1):
                # bergerak keatas sehingga y nya tidak berubah(kolomnya), tetapi x nya berubah (barisnya) dengan iterasi -1 sehingga bergerak keatas
                encrypted_text += matrix_representation[x][mid+i]
                x1 += 1
                print(x1, matrix_representation[x]
                      [mid+i], "(", x, ",", mid+i, ")")
            # Loop untuk mengambil elemen matriks dan menambahkannya ke teks terenkripsi, Bergerak kekiri dengan mid + 1 sebagai nilai awal dan mid - i - 1 sebagai nilai akhir dan -1 digunakan untuk mengakomodasi perubahan arah pergerakan ke kiri dalam matriks.
            for y in range(mid + i, mid - i - 1, -1):
                # bergerak kekiri sehingga x nya tidak berubah(barisnya), tetapi y nya berubah (kolomnya) dengan iterasi -1 sehingga bergerak kekiri
                encrypted_text += matrix_representation[mid-i-1][y]
                x1 += 1
                print(x1, matrix_representation[mid-i-1]
                      [y], "(", mid-i-1, ",", y, ")")
            # Loop untuk mengambil elemen matriks dan menambahkannya ke teks terenkripsi, Bergerak kebawah dengan mid -i -1 sebagai nilai awal dan mid + i + 1 sebagai nilai akhir
            for x in range(mid - i - 1, mid + i + 1):
                # bergerak kebawah sehingga y nya tidak berubah(kolomnya), tetapi x nya berubah(barisnya)
                encrypted_text += matrix_representation[x][mid-i-1]
                x1 += 1
                print(x1, matrix_representation[x]
                      [mid-i-1], "(", x, ",", mid-i-1, ")")
            if (i+1 != mid):  # untuk memeriksa apakah iterasi saat ini bukan iterasi terakhir dalam proses enkripsi(mengecek apakah sudah membentuk full spiral atau belum)
                # Loop untuk mengambil elemen matriks dan menambahkannya ke teks terenkripsi, Bergerak kekanan dengan mid - i - 1 sebagai nilai awal dan mid + i + 1 sebagai nilai akhir
                for y in range(mid - i - 1, mid + i + 1, +1):
                    # bergerak kekanan sehingga x nya tidak berubah(barisnya), tetapi y nya berubah(kolomnya)
                    encrypted_text += matrix_representation[mid+i+1][y]
                    x1 += 1
                    print(
                        x1, matrix_representation[mid+i+1][y], "(", mid+i+1, ",", y, ")")
        else:  # Perulangan ketika `step_size`/panjang matriks ganjil
            # Loop untuk mengambil elemen matriks dan menambahkannya ke teks terenkripsi, Bergerak kebawah dengan mid - i sebagai nilai awal dan mid + i + 1 sebagai nilai akhir
            for x in range(mid - i, mid + i + 1):
                # bergerak kebawah sehingga y nya tidak berubah(kolomnya), tetapi x nya berubah(barisnya)
                encrypted_text += matrix_representation[x][mid-i]
                x1 += 1
                print(x1, matrix_representation[x]
                      [mid-i], "(", x, ",", mid-i, ")")
            # Loop untuk mengambil elemen matriks dan menambahkannya ke teks terenkripsi, Bergerak kekanan dengan mid - i sebagai nilai awal dan mid + i + 1 sebagai nilai akhir
            for y in range(mid - i, mid + i + 1, +1):
                # bergerak kekanan sehingga x nya tidak berubah(barisnya), tetapi y nya berubah(kolomnya)
                encrypted_text += matrix_representation[mid+i+1][y]
                x1 += 1
                print(x1, matrix_representation[mid+i+1]
                      [y], "(", mid+i+1, ",", y, ")")
            # Loop untuk mengambil elemen matriks dan menambahkannya ke teks terenkripsi, Bergerak keatas dengan mid + i + 1 sebagai nilai awal dan mid - i - 1 sebagai nilai akhir dan -1 digunakan untuk mengakomodasi perubahan arah pergerakan ke atas dalam matriks.
            for x in range(mid + i + 1, mid - i - 1, -1):
                # bergerak keatas sehingga y nya tidak berubah(kolomnya), tetapi x nya berubah (barisnya) dengan iterasi -1 sehingga bergerak keatas
                encrypted_text += matrix_representation[x][mid+i+1]
                x1 += 1
                print(x1, matrix_representation[x]
                      [mid+i+1], "(", x, ",", mid+i+1, ")")
            # Loop untuk mengambil elemen matriks dan menambahkannya ke teks terenkripsi, Bergerak kekiri dengan mid + i + 1 sebagai nilai awal dan mid - i - 1 sebagai nilai akhir dan -1 digunakan untuk mengakomodasi perubahan arah pergerakan ke kiri dalam matriks.
            for y in range(mid + i + 1, mid - i - 1, -1):
                # bergerak kekiri sehingga x nya tidak berubah(barisnya), tetapi y nya berubah (kolomnya) dengan iterasi -1 sehingga bergerak kekiri
                encrypted_text += matrix_representation[mid-i-1][y]
                x1 += 1
                print(x1, matrix_representation[mid-i-1]
                      [y], "(", mid-i-1, ",", y, ")")
            if (i+1 == mid):
                i += 1
                for x in range(mid - i, mid + i + 1):
                    encrypted_text += matrix_representation[x][mid-i]
                    x1 += 1
                    print(x1, matrix_representation[x]
                          [mid-i], "(", x, ",", mid-i, ")")

    return encrypted_text


# Decryption
def spiral_decrypt():  # Fungsi untuk dekripsi
    cipher_text = input("Masukkan Cipher text : ")

    # Menghitung akar kuadrat dari panjang cipher text
    square_root = math.sqrt(len(cipher_text))

    # Pembulatan ke atas akar kuadrat untuk mendapatkan ukuran langkah yang dibutuhkan
    rounded_step_size = math.ceil(square_root)

    # Menggunakan ukuran langkah yang dibulatkan sebagai ukuran matriks yang akan digunakan
    step_size = rounded_step_size

    matrix_height = step_size  # Tinggi matriks
    matrix_width = step_size  # Lebar matriks
    mid = step_size // 2  # nilai tengah matriks
    x1 = 0  # Inisiasi banyaknya step/isi matrix
    plain_text_matrix = (
        [  # Matriks kosong untuk menyimpan representasi matriks dari teks
            [" " for _ in range(matrix_width)] for _ in range(matrix_height)
        ]
    )

    idx = 0  # Indeks untuk mengakses karakter dalam teks terenkripsi

    for i in range(mid):  # Mulai dari tengah
        if matrix_height % 2 == 0:  # Jika tinggi matriks genap
            # Loop untuk mengambil posisi matrix dan Bergerak keatas dengan mid + i sebagai nilai awal dan mid - i - 1 sebagai nilai akhir dan -1 digunakan untuk mengakomodasi perubahan arah pergerakan ke atas dalam matriks.
            for x in range(mid + i, mid - i - 1, -1):
                plain_text_matrix[x][mid+i] = cipher_text[  # bergerak keatas sehingga y nya tidak berubah(kolomnya), tetapi x nya berubah (barisnya) dengan iterasi -1 sehingga bergerak keatas
                    idx
                ]  # Masukkan karakter ke dalam matriks
                idx += 1  # Tambahkan indeks
                x1 += 1
                print(x1, plain_text_matrix[x][mid+i], "(", x, ",", mid+i, ")")
            # Loop untuk mengambil posisi matrix dan bergerak kekiri dengan mid + 1 sebagai nilai awal dan mid - i - 1 sebagai nilai akhir dan -1 digunakan untuk mengakomodasi perubahan arah pergerakan ke kiri dalam matriks.
            for y in range(mid + i, mid - i - 1, -1):
                plain_text_matrix[mid-i-1][y] = cipher_text[  # bergerak kekiri sehingga x nya tidak berubah(barisnya), tetapi y nya berubah (kolomnya) dengan iterasi -1 sehingga bergerak kekiri
                    idx
                ]  # Masukkan karakter ke dalam matriks
                idx += 1  # Tambahkan indeks
                x1 += 1
                print(x1, plain_text_matrix[mid-i-1]
                      [y], "(", mid-i-1, ",", y, ")")
            # Loop untuk mengambil posisi matrix dan Bergerak kebawah dengan mid -i -1 sebagai nilai awal dan mid + i + 1 sebagai nilai akhir
            for x in range(mid - i - 1, mid + i + 1):
                plain_text_matrix[x][mid-i-1] = cipher_text[  # bergerak kebawah sehingga y nya tidak berubah(kolomnya), tetapi x nya berubah(barisnya)
                    idx
                ]  # Masukkan karakter ke dalam matriks
                idx += 1  # Tambahkan indeks
                x1 += 1
                print(x1, plain_text_matrix[x]
                      [mid-i-1], "(", x, ",", mid-i-1, ")")
            if (i+1 != mid):  # untuk memeriksa apakah iterasi saat ini bukan iterasi terakhir dalam proses enkripsi(mengecek apakah sudah membentuk full spiral atau belum)
                # Loop untuk mengambil posisi matrix dan Bergerak kekanan dengan mid - i - 1 sebagai nilai awal dan mid + i + 1 sebagai nilai akhir
                for y in range(mid - i - 1, mid + i + 1, +1):
                    plain_text_matrix[mid+i+1][y] = cipher_text[  # bergerak kekanan sehingga x nya tidak berubah(barisnya), tetapi y nya berubah(kolomnya)
                        idx
                    ]  # Masukkan karakter ke dalam matriks
                    idx += 1  # Tambahkan indeks
                    x1 += 1
                    print(x1, plain_text_matrix[mid+i+1]
                          [y], "(", mid+i+1, ",", y, ")")
        else:  # Jika tinggi matriks ganjil
            # Loop untuk mengambil posisi matrix dan Bergerak kebawah dengan mid - i sebagai nilai awal dan mid + i + 1 sebagai nilai akhir
            for x in range(mid - i, mid + i + 1):
                plain_text_matrix[x][mid-i] = cipher_text[  # bergerak kebawah sehingga y nya tidak berubah(kolomnya), tetapi x nya berubah(barisnya)
                    idx
                ]  # Masukkan karakter ke dalam matriks
                idx += 1  # Tambahkan indeks
                x1 += 1
                print(x1, plain_text_matrix[x][mid-i], "(", x, ",", mid-i, ")")
            # Loop untuk mengambil posisi matrix dan Bergerak kekanan dengan mid - i sebagai nilai awal dan mid + i + 1 sebagai nilai akhir
            for y in range(mid - i, mid + i + 1, +1):
                plain_text_matrix[mid+i+1][y] = cipher_text[  # bergerak kekanan sehingga x nya tidak berubah(barisnya), tetapi y nya berubah(kolomnya)
                    idx
                ]  # Masukkan karakter ke dalam matriks
                idx += 1  # Tambahkan indeks
                x1 += 1
                print(x1, plain_text_matrix[mid+i+1]
                      [y], "(", mid+i+1, ",", y, ")")
            # Loop untuk mengambil posisi matrix dan Bergerak keatas dengan mid + i + 1 sebagai nilai awal dan mid - i - 1 sebagai nilai akhir dan -1 digunakan untuk mengakomodasi perubahan arah pergerakan ke atas dalam matriks.
            for x in range(mid + i + 1, mid - i - 1, -1):
                plain_text_matrix[x][mid+i+1] = cipher_text[  # bergerak keatas sehingga y nya tidak berubah(kolomnya), tetapi x nya berubah (barisnya) dengan iterasi -1 sehingga bergerak keatas
                    idx
                ]  # Masukkan karakter ke dalam matriks
                idx += 1  # Tambahkan indeks
                x1 += 1
                print(x1, plain_text_matrix[x]
                      [mid+i+1], "(", x, ",", mid+i+1, ")")
            # Loop untuk mengambil posisi matrix dan Bergerak kekiri dengan mid + i + 1 sebagai nilai awal dan mid - i - 1 sebagai nilai akhir dan -1 digunakan untuk mengakomodasi perubahan arah pergerakan ke kiri dalam matriks.
            for y in range(mid + i + 1, mid - i - 1, -1):
                plain_text_matrix[mid-i-1][y] = cipher_text[  # bergerak kekiri sehingga x nya tidak berubah(barisnya), tetapi y nya berubah (kolomnya) dengan iterasi -1 sehingga bergerak kekiri
                    idx
                ]  # Masukkan karakter ke dalam matriks
                idx += 1  # Tambahkan indeks
                x1 += 1
                print(x1, plain_text_matrix[mid-i-1]
                      [y], "(", mid-i-1, ",", y, ")")
            if (i+1 == mid):  # untuk memeriksa apakah iterasi saat ini bukan iterasi terakhir dalam proses enkripsi(mengecek apakah sudah membentuk full spiral atau belum)
                i += 1
                # Loop untuk mengambil posisi matrix dan Bergerak kebawah dengan mid - i sebagai nilai awal dan mid + i + 1 sebagai nilai akhir
                for x in range(mid - i, mid + i + 1):
                    plain_text_matrix[x][mid-i] = cipher_text[  # bergerak kebawah sehingga y nya tidak berubah(kolomnya), tetapi x nya berubah(barisnya)
                        idx
                    ]  # Masukkan karakter ke dalam matriks
                    idx += 1  # Tambahkan indeks
                    x1 += 1
                    print(x1, plain_text_matrix[x]
                          [mid-i], "(", x, ",", mid-i, ")")

    print("Matrix:\n")  # Tampilkan matriks representasi
    for row in plain_text_matrix:  # Untuk setiap baris dalam matriks representasi
        print(row)  # Tampilkan baris

    plain_text = ""  # Teks terdekripsi
    for j in range(matrix_width):  # Untuk setiap kolom dalam matriks representasi
        for i in range(matrix_height):  # Untuk setiap baris dalam matriks representasi
            # Jika bukan karakter akhirSpiral
            if plain_text_matrix[i][j] != akhirSpiral:
                plain_text += plain_text_matrix[i][
                    j
                ]  # Tambahkan karakter ke dalam teks terdekripsi
    print(plain_text)
    return plain_text  # Kembalikan - menjadi spasi


def hill_decript(msg):
    # Convert Cipher Text ke Huruf Besar
    cipher_text = msg

    key = (input("Masukkan key :"))

    key_matrix = buatkeymatrix(key)

    # Mencari determinan dengan menggunakan numpy, kemudian angkanya di bulatkan.
    determinant = int(np.round(np.linalg.det(key_matrix)))
    print("\nDeterminan : ", determinant)

    determinant = determinant % panjang_subs
    print("K^-1 : ", determinant)

    # Mencari modulo invers dari determinan
    modulo_inverse = mod_inverse(determinant, panjang_subs)

    print("Invers Modulo : ", modulo_inverse)

    if modulo_inverse is None:
        return "Determinan tidak memiliki invers modulo", panjang_subs
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
                adjoint_matrix[j, i] = (
                    (-1) ** (i + j)) * (cofactor % panjang_subs)

        # Mencari Kunci Matriks Invers dengan mengalikan adjoint_matrix dengan Modulo Invers dan di modulo 27.
        key_matrix_inv = (adjoint_matrix * modulo_inverse) % panjang_subs

        print("Adj matrix : ")
        print(adjoint_matrix)
        print("Kunci matrix invers : ")
        print(key_matrix_inv)

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
        decrypted_vector = np.dot(key_matrix_inv, block_vector) % panjang_subs
        print("Plaintext : ", decrypted_vector)

        # Konversi vektor hasil dekripsi menjadi huruf
        decrypted_block = ''.join([inverse_substitution[num]
                                  for num in decrypted_vector])
        print("Plaintext : ", decrypted_block)

        # Plain Text ditampung di variabel bernama plain_text
        # plain_text += decrypted_block
        for char in decrypted_block:
            if char != akhirHill:
                plain_text += char

    # Mengreplace karakter "_" dengan spasi " ".
    return plain_text.replace(spasi, ' ')


def main():
    while (1):
        choice = int(
            input("\n----------------\nSuper Enkripsi (Hill Cipher & Route Crab Spiral)\n----------------\n1. Enkripsi \n2. Dekripsi \n3. Cek Kunci \n4. Keluar \nPilihan: "))
        if choice == 1:
            print("----------------")
            # memanggil function transposisi dengan parameter substitusi
            # function substitusi akan dieksekusi terlebih dahulu, untuk mendapatkan nilai yang akan digunakan sebagai parameter transposisi
            print("Cipher text Hill Cipher & RC Spiral: ",
                  spiral_encrypt(hill_encript()))
        elif choice == 2:
            print("----------------")
            # memanggil function substitusi dengan parameter transposisi
            # function transposisi akan dieksekusi terlebih dahulu, untuk mendapatkan nilai yang akan digunakan sebagai parameter substitusi
            print("Plain text : ", hill_decript(spiral_decrypt()))

        elif choice == 3:
            cek_kunci()
        elif choice == 4:
            exit()
        else:
            print("\nChoose correct choice: ")


if __name__ == "__main__":
    main()
