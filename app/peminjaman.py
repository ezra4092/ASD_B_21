from app.sistem import *
from config import *
from datetime import datetime


class Node:
    """Representasi satu entitas data dalam struktur Linked List"""
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    """Struktur data linear dinamis untuk menyimpan antrean peminjaman sementara"""
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
    
    def hapus_terakhir(self):
        if self.head is None:
            return None
        # Kalau cuma ada 1 data
        if self.head.next is None:
            hapus = self.head.data
            self.head = None
            return hapus
        # Kalau data lebih dari 1, cari node sebelum node terakhir
        current = self.head
        while current.next.next:
            current = current.next
        hapus = current.next.data
        current.next = None
        return hapus
    
    def to_list(self):
        result = []
        current = self.head
        while current:
            result.append(current.data)
            current = current.next
        return result


class Stack:
    """Struktur data LIFO untuk mencatat dan membatalkan riwayat transaksi terakhir"""
    def __init__(self):
        self.items = []

    def push(self, data):
        self.items.append(data)

    def pop(self):
        if not self.kosong():
            return self.items.pop()
        return None

    def peek(self):
        if not self.kosong():
            return self.items[-1]
        return None

    def kosong(self):
        return len(self.items) == 0


def proses_peminjaman(ll_peminjaman, stack_riwayat):
    """Memvalidasi dan mencatat transaksi peminjaman baru ke Linked List dan Stack"""
    data_buku = baca_data(BUKU_FILE)
    cek_data(data_buku, "buku")
    
    username = input("\nMasukkan username pengunjung: ").strip()
    
    # Error handling jika username kosong
    if not username:
        print("\n[PERINGATAN] Username tidak boleh kosong!")
        pause()
        return

    # cek member
    if not cek_member(username):
        print("Pengunjung bukan member! Harus daftar dulu.")
        pause()
        return
        
    print("Member ditemukan.")
    input_buku = input("Masukkan ID / Judul Buku: ").strip()
    
    # Error handling jika input buku kosong
    if not input_buku:
        print("\n[PERINGATAN] ID atau Judul buku tidak boleh kosong!")
        pause()
        return

    buku = cari_buku(input_buku, data_buku)
    
    if not buku:
        print("Buku tidak ditemukan.")
        pause()
        return
        
    if int(buku["stok"]) <= 0:
        print("Stok buku habis.")
        pause()
        return
        
    konfirmasi = input("Izinkan peminjaman? (y/n): ").strip().lower()
    
    # Error handling jika konfirmasi kosong
    if not konfirmasi:
        print("\n[PERINGATAN] Pilihan konfirmasi tidak boleh kosong!")
        pause()
        return

    if konfirmasi == 'y':
        data_pinjam = {
            "username": username,
            "id_buku": buku["id_buku"],
            "judul_buku": buku["judul_buku"],
            "tanggal_peminjaman": datetime.now().strftime("%d-%m-%Y"),
            "tanggal_pengembalian": None
        }
        ll_peminjaman.tambah(data_pinjam)
        stack_riwayat.push(data_pinjam)
        buku["stok"] = int(buku["stok"]) - 1
        simpan_data(BUKU_FILE, data_buku)
        print("Buku berhasil dipinjam!")
        pause()
    else:
        print("Peminjaman dibatalkan.")
        pause()


def tampilkan_data_peminjaman():
    """Membaca dan menampilkan seluruh rekam jejak peminjaman dari file JSON"""
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


def edit_data_peminjaman(ll_peminjaman):
    """Memperbarui status pengembalian buku beserta sinkronisasi stok secara real-time"""
    print("\n--- EDIT DATA PEMINJAMAN ---")
    data_peminjaman = tampilkan_data_peminjaman()
    if not data_peminjaman:
        pause()
        return
        
    try:
        raw_pilihan = input("\nMasukkan nomor data yang ingin diedit (0 untuk batal): ").strip()
        
        # Error handling jika input nomor kosong
        if not raw_pilihan:
            print("\n[PERINGATAN] Nomor data tidak boleh kosong!")
            pause()
            return

        pilihan = int(raw_pilihan)
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
            
            tgl_baru = input("Masukkan Tanggal Pengembalian (DD-MM-YYYY) [Tekan Enter untuk hari ini]: ").strip()
            # Jika input kosong, otomatis gunakan tanggal hari ini
            if not tgl_baru:
                tgl_baru = datetime.now().strftime("%d-%m-%Y")
                print(f"Tanggal pengembalian otomatis disetel ke: {tgl_baru}")
                
            # 1. Update data peminjaman di file JSON
            data_peminjaman[idx]['tanggal_pengembalian'] = tgl_baru
            simpan_data(PEMINJAMAN_FILE, data_peminjaman) 
            
            # 2. Update data yang sama di Linked List
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
            
        else:
            print("Nomor data tidak ditemukan.")
    except ValueError:
        print("Masukan tidak valid! Harap masukkan angka.")
    pause()


def undo_peminjaman(ll_peminjaman, stack_riwayat):
    """Membatalkan peminjaman terakhir, menghapusnya dari antrean, file JSON, dan memulihkan stok buku"""
    if stack_riwayat.kosong():
        print("\nTidak ada riwayat peminjaman yang bisa di-undo.")
        pause()
        return
        
    # 1. Ambil data terakhir dari stack (Pop)
    data_batal = stack_riwayat.pop()
    
    # 2. Hapus data dari Linked List (Memori Sementara)
    ll_peminjaman.hapus_terakhir()
    
    # 3. Hapus data dari file JSON (Penyimpanan Permanen)
    # Kita baca data lama, lalu simpan kembali SEMUA KECUALI data yang di-undo
    data_json = baca_data(PEMINJAMAN_FILE)
    if data_json:
        # Filter data: simpan data yang TIDAK cocok dengan kriteria data_batal
        data_json_baru = [
            item for item in data_json 
            if not (item['username'] == data_batal['username'] and 
                    item['id_buku'] == data_batal['id_buku'] and 
                    item['tanggal_peminjaman'] == data_batal['tanggal_peminjaman'])
        ]
        # Simpan kembali list yang sudah difilter ke JSON
        simpan_data(PEMINJAMAN_FILE, data_json_baru)

    # 4. Kembalikan stok buku ke database buku
    data_buku = baca_data(BUKU_FILE)
    buku = cari_buku(data_batal["id_buku"], data_buku)
    
    if buku:
        buku["stok"] = int(buku["stok"]) + 1
        simpan_data(BUKU_FILE, data_buku)
        
    print(f"\nBerhasil Undo! Peminjaman buku '{data_batal['judul_buku']}' "
          f"oleh {data_batal['username']} telah dibatalkan.")
    print("Data telah dihapus dari memori & JSON. Stok buku telah dikembalikan.")
    pause()
    
    
def peminjaman_menu(ll_peminjaman):
    """Sub-menu routing khusus untuk mengelola sirkulasi dan sinkronisasi peminjaman"""
    stack_riwayat = Stack()
    while True:
        clear_screen()
        print("=" * 50)
        print("Dashboard Admin - Peminjaman Buku")
        print("=" * 50)
        print("1. Proses Peminjaman")
        print("2. Tampilkan Data Peminjaman")
        print("3. Edit Data Peminjaman")
        print("4. Simpan Data Peminjaman ke file")
        print("5. Hapus Data Terakhir Peminjaman")
        print("0. Kembali")
        
        choice = input("\nPilih (0-5): ").strip()
        
        # Error handling jika pilihan menu kosong
        if not choice:
            print("\n[PERINGATAN] Pilihan tidak boleh kosong!")
            pause()
            continue

        if choice == "1":
            proses_peminjaman(ll_peminjaman, stack_riwayat)
        elif choice == "2":
            tampilkan_data_peminjaman()
            pause()
        elif choice == "3":
            edit_data_peminjaman(ll_peminjaman)
        elif choice == "4":
            data_list = ll_peminjaman.to_list()
            if not data_list:
                print("\nBelum ada data peminjaman. Tidak bisa disimpan.")
            else:
                simpan_peminjaman(ll_peminjaman, PEMINJAMAN_FILE)
            pause()
        elif choice == "5":
            undo_peminjaman(ll_peminjaman, stack_riwayat)
        elif choice == "0":
            break