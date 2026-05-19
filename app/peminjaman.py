from app.sistem import *
from config import *
from datetime import datetime
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def tambah(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node

    def tampilkan(self):
        current = self.head
        if not current:
            print("\nBelum ada data peminjaman.")
            return
        
        print(f"{'📖 DATA PEMINJAMAN':^80}")
        print("=" * 80)
        print(f"| {'No':<3} | {'Username':<8} | {'ID Buku':<8} | {'Judul Buku':<25} | {'Tanggal':<12} |")
        print("=" * 80)

        no = 1
        while current:
            data = current.data

            # biar judul gak kepanjangan
            judul = data['judul_buku']
            if len(judul) > 25:
                judul = judul[:22] + "..."

            print(f"| {no:<3} | {data['username']:<8} | {data['id_buku']:<8} | {judul:<25} | {data['tanggal_peminjaman']:<12} |")

            current = current.next
            no += 1

        print("=" * 80)

    def to_list(self):
        result = []
        current = self.head

        while current:
            result.append(current.data)
            current = current.next

        return result

def proses_peminjaman(ll_peminjaman):
    data_buku = baca_data(BUKU_FILE)
    cek_data(data_buku, "buku")

    username = input("\nMasukkan username pengunjung: ")

    # cek member
    if not cek_member(username):
        print("Pengujung bukan member! Harus daftar dulu.")
        pause()
        return

    print("✅ Member ditemukan.")

    input_buku = input("Masukkan ID / Judul Buku: ")
    buku = cari_buku(input_buku, data_buku)

    if not buku:
        print("❌ Buku tidak ditemukan.")
        return

    if int(buku["stok"]) <= 0:
        print("❌ Stok buku habis.")
        return

    konfirmasi = input("Izinkan peminjaman? (y/n): ")
    if konfirmasi.lower() == 'y':

        data_pinjam = {
            "username": username,
            "id_buku": buku["id_buku"],
            "judul_buku": buku["judul_buku"],
            "tanggal_peminjaman": datetime.now().strftime("%d-%m-%Y")
        }

        ll_peminjaman.tambah(data_pinjam)
        buku["stok"] = int(buku["stok"]) - 1

        simpan_data(BUKU_FILE, data_buku)

        print("Buku berhasil dipinjam!")
        pause()
    else:
        print("Peminjaman dibatalkan.")
        pause()

def peminjaman_menu(ll_peminjaman):
    """Menu peminjaman buku"""
    while True:
        clear_screen()
        print("=" * 50)
        print("Dashboard Admin - Peminjaman Buku")
        print("=" * 50)
        print("1. Proses Peminjaman")
        print("2. Tampilkan Data Peminjaman")
        print("3. Simpan Data Peminjaman ke file")
        print("0. Kembali")
        
        choice = input("\nPilih (0-2): ").strip()
        
        if choice == "1":
            proses_peminjaman(ll_peminjaman)
        elif choice == "2":
            ll_peminjaman.tampilkan()
            pause()
        elif choice == "3":
            data_list = ll_peminjaman.to_list()

            if not data_list:
                print("\nBelum ada data peminjaman. Tidak bisa disimpan.")
            else:
                simpan_peminjaman(ll_peminjaman, PEMINJAMAN_FILE)
                print("\nData peminjaman berhasil disimpan.")
            pause()
        elif choice == "0":
            break
