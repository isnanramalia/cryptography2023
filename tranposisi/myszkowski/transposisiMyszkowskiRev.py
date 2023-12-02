# Import library NumPy
# NumPy adalah library yang sangat berguna untuk melakukan operasi numerik dan manipulasi data.
import numpy as np
# Import class 'Counter' dari modul 'Collection', untuk menghitung frekuensi kemunculan elemen
from collections import Counter


# Tampilkan judul program dan menu pilihan.
def tampilkan_menu():
    print("PROGRAM ENKRIPSI-DEKRIPSI MYSZKOWSKI TRANSPOSITION")
    print("\n[MENU]")
    print(" [1] Enkripsi")
    print(" [2] Dekripsi")
    print(" [3] Keluar")

# Fungsi untuk mengonversi kunci
def konversi_kunci():
    # Membuat list kosong.
    sortkunci = []  
    # Menambahkan kunci ke list sortkunci.
    sortkunci.append(kunci)  
    # Menambahkan list kosong ke list sortkunci.
    sortkunci.append([])
    # Loop untuk menambahkan indeks ke list sortkunci.
    i = 0
    while i < len(kunci):  
        sortkunci[1].append(i + 1)  
        i += 1
    # Mengubah list sortkunci menjadi array, di mana baris pertama berisi elemen-elemen list kunci dan baris kedua berisi nilai-nilai dari 1 hingga panjang kunci.
    sortkunci = np.array(sortkunci)  
    # Mengurutkan kunci yang ditampung pada variabel newsortkunci
    newsortkunci = sortkunci[:, sortkunci[0].argsort()] 
    # Mengubah array menjadi list. Hasilnya adalah sortkunci yang kini berisi data yang telah diurutkan.
    sortkunci = newsortkunci.tolist()  
    # Menambahkan list kosong ke list sortkunci.
    sortkunci.append([])  
    # Menghitung jumlah huruf yang sama.
    hitung = Counter(sortkunci[0])  
    # Loop untuk menambahkan indeks ke list sortkunci
    i = 0
    n = 1
    while i < len(kunci):  
        # Mengecek jika ada elemen yang sama
        if hitung[sortkunci[0][i]] > 1:  
            for j in range(hitung[sortkunci[0][i]]):  
                sortkunci[2].append(n)
            # Menambahkan nilai i dengan jumlah huruf yang sama dikurangi 1. Sehingga huruf yang sama memiliki nilai urutan yang sama
            i += (hitung[sortkunci[0][i]] - 1)
        else:
            sortkunci[2].append(n)
        n += 1
        i += 1
    # Mengubah list sortkunci menjadi array.
    sortkunci = np.array(sortkunci)  
    # Mengurutkan indeks berdasarkan urutan elemen awal yang terdapat pada kunci 
    newsortkunci = sortkunci[:, sortkunci[1].argsort()]  
    print("\nK:"
            # Mengonversi array newsortkunci menjadi string
            + np.array2string(newsortkunci[2],
            # 'str_kind' digunakan untuk mengonfigurasi cara elemen-elemen string dalam array
            # 'lamda x: x' digunakan untuk mempertahankan elemen-elemen string apaadanya
            formatter={"str_kind": lambda x: x},
            # Menambahakan pemisah antar elemen
            separator=" ",
            # Menghilangkan format tampilan kurung siku
            )[1:-1]
    )
    
# Loop utama program.
while True:
    tampilkan_menu()
    pilih = input("Pilih menu: ")
    # -------------------- OPERASI ENKRIPSI ------------------------
    if pilih == "1":
        teks = input("\nMasukkan teks yang ingin dienkripsi: ")
        # Mengganti spasi dengan dash.
        teks = teks.replace(" ", "-")  
        # Mengubah teks menjadi huruf kapital.
        teks = teks.upper()  
        kunci = input("Masukkan kunci: ")
        # Mengubah kunci menjadi huruf kapital.
        kunci = list(kunci.upper())  
        # Membuat list kosong untuk menyimpan kunci yang sudah diurutkan.
        
        # Masuk ke konversi kunci
        konversi_kunci()
        
        #------------------------ MEMBUAT MATRIKS ---------------------------
        # Membuat list kosong untuk menyimpan hasil enkripsi.
        enkripsi = []  
        # Menambahkan kunci ke list enkripsi.
        enkripsi.append(kunci)
        # Membuat range angka yang dimulai dari 0, berakhir sebelum panjang teks, dan dengan langkah sepanjang kunci
        for i in range(0, len(teks), len(kunci)):
            # Memotong teks dengan panjang teks sama dengan panjang kunci
            x = teks[i : i + len(kunci)]  
            # Mengubah teks menjadi list. Ini dilakukan agar setiap karakter dalam potongan teks dapat diakses secara terpisah.
            x = list(x) 
            # Menambahkan teks yang sudah dipotong ke list enkripsi.
            enkripsi.append(x)  
        # Loop untuk menambahkan dash ke bagian terakhir teks.
        while len(enkripsi[len(enkripsi) - 1]) < len(kunci): 
            enkripsi[len(enkripsi) - 1].append("@")
        # Mengubah list enkripsi menjadi array.
        enkripsi = np.array(enkripsi) 
        # Menampilkan teks yang sudah dipotong.
        print(" "+ np.array2string(enkripsi[1 : len(enkripsi)],
                formatter={"str_kind": lambda x: x},  
                separator=" ",
                )[1:-1]
        )
        #------------------------ MEMBUAT MATRIKS END ---------------------------
        
        #------------------------ PROSES ENKRIPSI ---------------------------
        # Mengurutkan teks enkripsi berdasarkan kunci
        newenkripsi = enkripsi[:, enkripsi[0].argsort()] 
        # Menghitung jumlah huruf yang sama.
        hitung = Counter(newenkripsi[0])  
        hasil = []  
        # Loop untuk mengambil huruf dari teks yang sudah diurutkan.
        i = 0
        while i < len(newenkripsi[0]):  
            # Jika tidak ada huruf yang sama.
            if hitung[newenkripsi[0][i]] == 1:  
                # Loop sebanyak jumlah baris teks dan menambahkannya pada list hasil
                for j in range(1, len(newenkripsi)):  
                    hasil.append(newenkripsi[j][i])  
            else:
                # Loop sebanyak jumlah baris teks.
                for j in range(1, len(newenkripsi)):  
                    # Loop sebanyak jumlah huruf yang sama.
                    for k in range(i, hitung[newenkripsi[0][i]] + i):  
                        hasil.append(newenkripsi[j][k])
                # Menambahkan nilai i dengan jumlah huruf yang sama dikurangi 1.
                # Ini dilakukan untuk bisa melanjutkan dengan elemen yang belum di proses sebelumnya
                i += (hitung[newenkripsi[0][i]] - 1)  
            i += 1
        # Setelah operasi enkripsi, tampilkan hasil enkripsi.
        # Menggabungkan list hasil menjadi string.
        hasil_enkripsi = "".join(hasil)  
        # Menghapus spasi.
        hasil_enkripsi = hasil_enkripsi.replace(" ", "")  
        print("\nHasil enkripsi =", hasil_enkripsi)

        # Tanya pengguna apakah ingin melanjutkan atau keluar.
        lanjut = input("Apakah ingin melanjutkan? (y/n): ")
        if lanjut.lower() != "y":
            print("Terima kasih, program telah keluar.")
            break  # Keluar dari loop utama dan program selesai.
    #------------------------ PROSES ENKRIPSI END ---------------------------

    # -------------------- OPERASI DEKRIPSI ------------------------
    elif pilih == "2":
        teks = input("\nMasukkan teks yang ingin didekripsi: ")
        # Mengubah teks menjadi huruf kapital.
        teks = list(teks.upper())  
        kunci = input("Masukkan kunci: ")
        # Mengubah kunci menjadi huruf kapital.
        kunci = list(kunci.upper())  
        # Membuat list kosong untuk menyimpan kunci yang sudah diurutkan.
        
        # Masuk ke konversi kunci
        konversi_kunci()
        #--------------------Membuat matrix-----------------
        # Membuat list kosong untuk menyimpan hasil dekripsi.
        dekripsi = []  
        # Menambahkan kunci ke list dekripsi.
        dekripsi.append(kunci)  
        # Menambahkan list kosong ke list dekripsi.
        dekripsi.append([])  
        # Loop untuk menambahkan indeks ke list dekripsi.
        i = 0
        while i < len(kunci):  
            dekripsi[1].append(i + 1)  
            i += 1  
        # Mengubah list dekripsi menjadi array.
        dekripsi = np.array(dekripsi)  
        # Mengurutkan teks dekripsi sesuai urutan abjad.
        newdekripsi = dekripsi[:, dekripsi[0].argsort()]  #indeks 0 merujuk pd kunci 
        # Mengubah array menjadi list.
        dekripsi = newdekripsi.tolist()  
        # Loop untuk menambahkan list kosong ke list dekripsi.
        for i in range(int(len(teks) / len(kunci))):  
            #append untuk menambahkan elemen
            dekripsi.append([])  
        # Menghitung jumlah huruf yang sama.
        hitung = Counter(dekripsi[0])  
        # Loop untuk menambahkan huruf ke list dekripsi.
        #------------------Proses memasukkan huruf kedalam list-------------
        indeks = 0
        i = 0
        while i < len(kunci):  
            # Jika ada huruf yang sama.
            if hitung[dekripsi[0][i]] > 1:  
                # Loop sebanyak jumlah baris teks. menentukan jumlah baris untuk proses dekripsi
                for k in range(2, int((len(teks) / len(kunci)) + 2)):  
                    # Loop sebanyak jumlah huruf yang sama.
                    for j in range(hitung[dekripsi[0][i]]):  
                        dekripsi[k].append(teks[indeks])  
                        indeks += 1
                # Menambahkan nilai i dengan jumlah huruf yang sama dikurangi 1.
                # Ini dilakukan untuk bisa melanjutkan dengan elemen yang belum di proses sebelumnya
                i += (hitung[dekripsi[0][i]] - 1)
            else:
                # Loop sebanyak jumlah baris teks.
                for k in range(2, int((len(teks) / len(kunci)) + 2)):
                    #menambah elemen dari teks yg diambil dengan indeks 
                    #Setiap iterasi loop akan menambahkan elemen dari teks ke daftar dekripsi[k]
                    dekripsi[k].append(teks[indeks])  
                    indeks += 1
            i += 1
        
        # Mengubah list dekripsi menjadi array.
        dekripsi = np.array(dekripsi)  
        # Mengembalikan urutan teks 
        hasil = dekripsi[:, dekripsi[1].argsort()] 
        # Menampilkan teks yang sudah dipotong dan yg sudah diurutkan
        #mencetak hasil array 
        print(" "+ np.array2string(hasil[2 : len(hasil)],
                formatter={"str_kind": lambda x: x},
                separator=" ",  
                )[1:-1]
        )
        #--------------------Matrix end----------------
        print("\nHasil dekripsi =", end=" ")
        # Loop untuk menampilkan hasil dekripsi.
        #dimulai dari index ke 2 hingga akhir array(hasil)
        #digunakan untuk mengakses setiap baris dalam array hasil,
        for i in range(2, len(hasil)):  
            #mengakses stiap karakter dalam index dalam baris tsb
            for j in range(len(hasil[0])):
                # Jika ada dash diganti spasi.
                if hasil[i][j] == "-":  
                    print(" ", end="") 
                # Jika ada at dihilangkan
                elif hasil[i][j] == "@":  
                    print("", end="")  
                # Jika tidak ada dash atau at.
                else:  
                    print(hasil[i][j], end="")

        lanjut = input("\nApakah ingin melanjutkan? (y/n): ")
        if lanjut.lower() != "y":
            print("Terima kasih, program telah keluar.")
            break
    elif pilih == "3":
        print("Terima kasih, program telah keluar.")
        break  # Keluar dari loop utama dan program selesai.

    else:
        print("[!] Pilihan tidak valid. Silakan masukkan pilihan yang sesuai.")
