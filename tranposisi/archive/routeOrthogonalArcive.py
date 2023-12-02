# matrik: kiri atas ke kanan
# ciphertext: kiri atas ke bawah
import math  # Import module math untuk fungsi ceil() dan floor()


def tampilkan_menu():  # Fungsi untuk menampilkan menu
    print(
        "PROGRAM ENKRIPSI-DEKRIPSI ORTHOGONAL TRANSPOSITION"
    )  # Menampilkan judul program
    print("\n[MENU]")  # Menampilkan menu
    print(" [1] Enkripsi")
    print(" [2] Dekripsi")
    print(" [3] Keluar")


def orthogonal_encrypt(plain_text, step_size):  # Fungsi untuk enkripsi
    matrix_representation = (
        []
    )  # Matriks kosong untuk menyimpan representasi matriks dari teks
    encrypted_text = ""  # Teks terenkripsi

    matrix_height = math.ceil(len(plain_text) / step_size)  # Tinggi matriks
    matrix_width = step_size  # Lebar matriks

    for i in range(matrix_height):  # Mengisi matriks dengan karakter dari teks
        matrix_row = []  # Baris matriks
        for j in range(matrix_width):
            index = (
                i * matrix_width
                + j  # i = indeks baris saat ini, matrix_width = jumlah kolom, j = indeks kolom saat ini
            )  # Indeks karakter yang akan dimasukkan ke dalam baris matriks
            if index < len(
                plain_text
            ):  # Jika masih ada karakter yang tersisa, masukkan karakter ke dalam baris matriks
                matrix_row.append(
                    plain_text[index]
                )  # Masukkan karakter ke dalam baris matriks
            else:  # Jika tidak ada karakter yang tersisa, masukkan karakter '@' ke dalam baris matriks
                matrix_row.append(
                    "@"
                )  # Masukkan karakter '@' ke dalam baris matriks
        matrix_representation.append(
            matrix_row
        )  # Masukkan baris matriks ke dalam matriks representasi

    print("Matrix:\n")  # Tampilkan matriks representasi
    for row in matrix_representation:  # Untuk setiap baris dalam matriks representasi
        print(row)  # Tampilkan baris

    # proses enkripsi
    for j in range(matrix_width):  # Bergerak dari kiri ke kanan
        for i in range(matrix_height):  # Bergerak dari atas ke bawah
            if matrix_representation[i][j] != "@":  # Jika bukan karakter '@'
                encrypted_text += matrix_representation[i][
                    j
                ]  # Tambahkan karakter ke dalam teks terenkripsi
            else:  # Jika karakter '@'
                encrypted_text += "@"  # Tambahkan karakter '@' ke dalam teks terenkripsi
    return encrypted_text


def orthogonal_decrypt(cipher_text, step_size):  # Fungsi untuk dekripsi
    matrix_height = math.ceil(len(cipher_text) / step_size)  # Tinggi matriks
    matrix_width = step_size  # Lebar matriks

    plain_text_matrix = (
        [  # Matriks kosong untuk menyimpan representasi matriks dari teks
            [" " for _ in range(matrix_width)] for _ in range(matrix_height)
        ]
    )

    idx = 0  # Indeks untuk mengakses karakter dalam teks terenkripsi

    for j in range(matrix_width):  # Bergerak dari kiri ke kanan
        for i in range(matrix_height):  # Bergerak dari atas ke bawah
            plain_text_matrix[i][j] = cipher_text[
                idx
            ]  # Masukkan karakter ke dalam matriks
            idx += 1  # Tambahkan indeks

    print("Matrix:\n")  # Tampilkan matriks representasi
    for row in plain_text_matrix:  # Untuk setiap baris dalam matriks representasi
        print(row)  # Tampilkan baris

    plain_text = ""  # Teks terdekripsi
    for i in range(matrix_height):  # Untuk setiap baris dalam matriks representasi
        for j in range(matrix_width):  # Untuk setiap kolom dalam matriks representasi
            if plain_text_matrix[i][j] != "@":  # Jika bukan karakter '@'
                plain_text += plain_text_matrix[i][
                    j
                ]  # Tambahkan karakter ke dalam teks terdekripsi

    return plain_text.replace("-", " ")  # Kembalikan - menjadi spasi


while True:
    tampilkan_menu()
    pilih = input("Pilih menu: ")

    if pilih == "1":
        plain_text = input("Masukan teks yang ingin dienkripsi: ")
        plain_text = plain_text.replace(
            " ", "-"
        )  # Ganti spasi dengan karakter '-' agar bisa dienkripsi
        step_size = int(input("Masukan kunci (angka): "))  # Masukan kunci
        cipher = orthogonal_encrypt(
            plain_text, step_size
        )  # Panggil fungsi orthogonal_encrypt()
        print("\nCiphertext: " + cipher)  # Tampilkan teks terenkripsi

        lanjut = input("Apakah ingin melanjutkan? (y/n): ")
        if lanjut.lower() != "y":
            print("Terima kasih, program telah keluar.")
            break

    elif pilih == "2":
        cipher_text = input(
            "Masukan teks yang ingin didenkripsi: "
        )  # Masukan teks terenkripsi
        step_size = int(input("Masukan kunci (angka): "))  # Masukan kunci
        deciphered_text = orthogonal_decrypt(
            cipher_text, step_size
        )  # Panggil fungsi orthogonal_decrypt()
        print("\nPlaintext: " + deciphered_text)  # Tampilkan teks terdekripsi

        lanjut = input("Apakah ingin melanjutkan? (y/n): ")
        if lanjut.lower() != "y":
            print("Terima kasih, program telah keluar.")
            break

    elif pilih == "3":
        print("Terima kasih, program telah keluar.")
        break  # Keluar dari loop utama dan program selesai.

    else:
        print("[!] Pilihan tidak valid. Silakan masukkan pilihan yang sesuai.")
