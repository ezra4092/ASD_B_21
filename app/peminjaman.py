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

    # Fungsi tampilkan() dari LinkedList bisa dihapus atau dibiarkan
    # karena kita akan menggunakan fungsi baru yang membaca dari JSON
    
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
        print("Pengunjung bukan member! Harus daftar dulu.")
        pause()
        return

    print("Member ditemukan.")

    input_buku = input("Masukkan ID / Judul Buku: ")
    buku = cari_buku(input_buku, data_buku)

    if not buku:
        print("Buku tidak ditemukan.")
        return

    if int(buku["stok"]) <= 0:
        print("Stok buku habis.")
        return

    konfirmasi = input("Izinkan peminjaman? (y/n): ")
    if konfirmasi.lower() == 'y':

        data_pinjam = {
            "username": username,
            "id_buku": buku["id_buku"],
            "judul_buku": buku["judul_buku"],
            "tanggal_peminjaman": datetime.now().strftime("%d-%m-%Y"),
            "tanggal_pengembalian": None
        }

        ll_peminjaman.tambah(data_pinjam)
        buku["stok"] = int(buku["stok"]) - 1

        simpan_data(BUKU_FILE, data_buku)

        print("Buku berhasil dipinjam!")
        pause()
    else:
        print("Peminjaman dibatalkan.")
        pause()

# ... (kode class Node, LinkedList, proses_peminjaman, dll tetap sama)

def tampilkan_data_peminjaman():
    """Membaca dan menampilkan data peminjaman dari file JSON"""
    data_peminjaman = baca_data(PEMINJAMAN_FILE)
    
    if not data_peminjaman:
        print("\nBelum ada data peminjaman di file.")
        return None
    
    print(f"{'📖 DATA PEMINJAMAN':^100}")
    print("=" * 100)
    print(f"| {'No':<3} | {'Username':<12} | {'ID Buku':<8} | {'Judul Buku':<25} | {'Tgl Pinjam':<12} | {'Tgl Kembali':<12} |")
    print("=" * 100)

    for no, data in enumerate(data_peminjaman, start=1):
        judul = data['judul_buku']
        if len(judul) > 25:
            judul = judul[:22] + "..."

        tgl_pinjam = data.get('tanggal_peminjaman', '-')
        tgl_kembali = data.get('tanggal_pengembalian') or '-'

        print(f"| {no:<3} | {data['username']:<12} | {data['id_buku']:<8} | {judul:<25} | {tgl_pinjam:<12} | {tgl_kembali:<12} |")

    print("=" * 100)
    return data_peminjaman


# --- FUNGSI DIPERBARUI: Menambah parameter ll_peminjaman & logika penambahan stok ---
def edit_data_peminjaman(ll_peminjaman):
    """Mengedit tanggal pengembalian buku dari file JSON dan Linked List"""
    print("\n--- EDIT DATA PEMINJAMAN ---")
    data_peminjaman = tampilkan_data_peminjaman()
    
    if not data_peminjaman:
        pause()
        return

    try:
        pilihan = int(input("\nMasukkan nomor data yang ingin diedit (0 untuk batal): "))
        
        if pilihan == 0:
            print("Pengeditan dibatalkan.")
            pause()
            return
            
        if 1 <= pilihan <= len(data_peminjaman):
            idx = pilihan - 1
            data_edit = data_peminjaman[idx]
            
            # Cegah edit jika buku sudah dikembalikan sebelumnya
            if data_edit.get('tanggal_pengembalian'):
                print("\nBuku ini sudah dikembalikan! Tidak perlu diedit lagi.")
                pause()
                return

            print(f"\nData terpilih:")
            print(f"Buku     : {data_edit['judul_buku']}")
            print(f"Peminjam : {data_edit['username']}")
            print(f"Tgl Kembali Saat Ini : Belum dikembalikan")
            
            # --- PERUBAHAN INPUT TANGGAL ---
            tgl_baru = input("Masukkan Tanggal Pengembalian (DD-MM-YYYY) [Tekan Enter untuk hari ini]: ").strip()
            
            # Jika input kosong, otomatis gunakan tanggal hari ini
            if not tgl_baru:
                tgl_baru = datetime.now().strftime("%d-%m-%Y")
                print(f"Tanggal pengembalian otomatis disetel ke: {tgl_baru}")
            
            # 1. Update data peminjaman di file JSON
            data_peminjaman[idx]['tanggal_pengembalian'] = tgl_baru
            simpan_data(PEMINJAMAN_FILE, data_peminjaman) 

            # 2. Update data yang sama di Linked List agar saat disave (opsi 4) tidak nimpa jadi null lagi
            current = ll_peminjaman.head
            while current:
                if (current.data['username'] == data_edit['username'] and 
                    current.data['id_buku'] == data_edit['id_buku'] and 
                    current.data['tanggal_peminjaman'] == data_edit['tanggal_peminjaman']):
                    current.data['tanggal_pengembalian'] = tgl_baru
                current = current.next

            # 3. Tambahkan Stok Buku + 1
            data_buku = baca_data(BUKU_FILE)
            for buku in data_buku:
                if str(buku['id_buku']) == str(data_edit['id_buku']):
                    buku['stok'] = int(buku['stok']) + 1
                    break
            simpan_data(BUKU_FILE, data_buku)

            print("\nData peminjaman berhasil diperbarui dan Stok buku bertambah!")
            # -------------------------------

        else:
            print("Nomor data tidak ditemukan.")
    except ValueError:
        print("Masukan tidak valid! Harap masukkan angka.")
    
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
        print("3. Edit Data Peminjaman")
        print("4. Simpan Data Peminjaman ke file")
        print("0. Kembali")
        
        choice = input("\nPilih (0-4): ").strip()
        
        if choice == "1":
            proses_peminjaman(ll_peminjaman)
        elif choice == "2":
            tampilkan_data_peminjaman()
            pause()
        elif choice == "3":
            # Pass ll_peminjaman agar bisa diupdate
            edit_data_peminjaman(ll_peminjaman)
        elif choice == "4":
            data_list = ll_peminjaman.to_list()

            if not data_list:
                print("\nBelum ada data peminjaman. Tidak bisa disimpan.")
            else:
                # Pastikan memberikan DUA parameter: LinkedList dan nama filenya
                simpan_peminjaman(ll_peminjaman, PEMINJAMAN_FILE)
            pause()
        elif choice == "0":
            break