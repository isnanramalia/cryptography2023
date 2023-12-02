import math  # Import module math untuk fungsi ceil() dan floor()


def tampilkan_menu():  # Fungsi untuk menampilkan menu
    print(
        "PROGRAM ENKRIPSI-DEKRIPSI ORTHOGONAL TRANSPOSITION"
    )  # Menampilkan judul program
    print("\n[MENU]")  # Menampilkan menu
    print(" [1] Enkripsi")
    print(" [2] Dekripsi")
    print(" [3] Keluar")


def orthogonal_encrypt(plain_text, step_size):
    matrix_representation = []
    encrypted_text = ""

    for i in range(step_size):
        matrix_row = []
        for j in range(math.ceil(len(plain_text) / step_size)):
            index = j * step_size + i
            if index < len(plain_text):
                matrix_row.append(plain_text[index])
            else:
                matrix_row.append("@")
        matrix_representation.append(matrix_row)

    print("Matrix:\n")
    for row in matrix_representation:
        print(row)

    matrix_height = step_size
    matrix_width = math.ceil(len(plain_text) / matrix_height)

    for j in range(matrix_width):
        if j % 2 == 0:  # Jika kolom genap, bergerak dari bawah ke atas
            for i in range(matrix_height):
                if matrix_representation[i][j] != "@":
                    encrypted_text += matrix_representation[i][j]
        else:  # Jika kolom ganjil, bergerak dari atas ke bawah
            for i in range(matrix_height - 1, -1, -1):
                if matrix_representation[i][j] != "@":
                    encrypted_text += matrix_representation[i][j]

    return encrypted_text


def orthogonal_decrypt(cipher_text, step_size):  # Fungsi untuk dekripsi
    matrix_height = step_size  # Tinggi matriks
    matrix_width = math.ceil(len(cipher_text) / matrix_height)  # Lebar matriks

    plain_text_matrix = (
        [  # Matriks kosong untuk menyimpan representasi matriks dari teks
            [" " for _ in range(matrix_width)] for _ in range(matrix_height)
        ]
    )

    idx = 0  # Indeks untuk mengakses karakter dalam teks terenkripsi

    for i in range(matrix_height - 1, -1, -1):  # Mulai dari baris terakhir
        if matrix_height % 2 == 0:  # Jika tinggi matriks genap
            if i % 2 != 0:  # Jika baris genap
                for j in range(matrix_width - 1, -1, -1):  # Bergerak dari kanan ke kiri
                    plain_text_matrix[i][j] = cipher_text[
                        idx
                    ]  # Masukkan karakter ke dalam matriks
                    idx += 1  # Tambahkan indeks
            else:  # Jika baris ganjil
                for j in range(matrix_width):  # Bergerak dari kiri ke kanan
                    plain_text_matrix[i][j] = cipher_text[
                        idx
                    ]  # Masukkan karakter ke dalam matriks
                    idx += 1  # Tambahkan indeks
        else:
            if i % 2 == 0:  # Jika baris genap
                for j in range(matrix_width - 1, -1, -1):  # Bergerak dari kanan ke kiri
                    plain_text_matrix[i][j] = cipher_text[
                        idx
                    ]  # Masukkan karakter ke dalam matriks
                    idx += 1  # Tambahkan indeks
            else:  # Jika baris ganjil
                for j in range(matrix_width):  # Bergerak dari kiri ke kanan
                    plain_text_matrix[i][j] = cipher_text[
                        idx
                    ]  # Masukkan karakter ke dalam matriks
                    idx += 1  # Tambahkan indeks

    print("Matrix:\n")  # Tampilkan matriks representasi
    for row in plain_text_matrix:  # Untuk setiap baris dalam matriks representasi
        print(row)  # Tampilkan baris

    plain_text = ""  # Teks terdekripsi
    for j in range(matrix_width):  # Untuk setiap kolom dalam matriks representasi
        for i in range(matrix_height):  # Untuk setiap baris dalam matriks representasi
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
