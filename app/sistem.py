import json
import os
from config import *
from datetime import datetime


def clear_screen():
    """Membersihkan layar terminal secara dinamis berdasarkan sistem operasi (Windows/Linux/Mac)"""
    os.system('cls' if os.name == 'nt' else 'clear')


def baca_data(filename):
    """Membaca data dari file JSON dengan sistem error handling jika file tidak ada atau rusak"""
    try:
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    except Exception as e:
        print(f"Error loading {filename}: {e}")
        return []


def simpan_data(filename, data):
    """Menyimpan atau menimpa (overwrite) data ke dalam file JSON dengan format yang rapi"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving {filename}: {e}")
        return False


def simpan_peminjaman(ll_peminjaman, PEMINJAMAN_FILE):
    """Menyinkronkan data peminjaman dari Linked List (memori sementara) ke file JSON secara aman tanpa duplikasi"""
    data_list = ll_peminjaman.to_list()
    if not data_list:
        print("\nBelum ada data peminjaman di memori. Tidak bisa disimpan.")
        return
    try:
        # 1. Baca data lama dari file
        try:
            with open(PEMINJAMAN_FILE, "r") as f:
                data_lama = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data_lama = []
        # 2. Gabungkan data (Cegah Duplikat)
        for data_baru in data_list:
            ditemukan = False
            for i, data_file in enumerate(data_lama):
                # Kita anggap sebuah transaksi unik berdasarkan username, id buku, dan tgl peminjaman
                if (data_file['username'] == data_baru['username'] and 
                    data_file['id_buku'] == data_baru['id_buku'] and 
                    data_file['tanggal_peminjaman'] == data_baru['tanggal_peminjaman']):
                    # Update datanya jika ternyata ada perubahan (misal dari Linked List sudah dikembalikan)
                    data_lama[i] = data_baru
                    ditemukan = True
                    break
            # Jika tidak ditemukan di file JSON (berarti pinjaman baru), tambahkan
            if not ditemukan:
                data_lama.append(data_baru)
        # 3. Simpan kembali secara utuh ke file
        with open(PEMINJAMAN_FILE, "w") as f:
            json.dump(data_lama, f, indent=4)
        print("\nData peminjaman berhasil disinkronkan dan disimpan ke JSON!")
    except Exception as e:
        print(f"Terjadi error saat menyimpan: {e}")


def cek_data(items, item_type):
    """Memeriksa eksistensi data dan menampilkannya dalam bentuk tabel sesuai tipenya (buku/user)"""
    if not items:
        print(f"\nBelum ada data {item_type}.")
        return False
    items = [eval(item) if isinstance(item, str) else item for item in items]
    if item_type == "buku":
        print(f"{'📚 DAFTAR BUKU GIE\'S LIBRARY 📚':^{130}}")
        print("=" * 130)
        print(f"| {'No':<3} | {'ID':<8} | {'Judul':<30} | {'Penulis':<25} | {'Stok':^5} | {'Kategori':<20} | {'Tanggal':<12} |")
        print("=" * 130)
        for i, buku in enumerate(items, start=1):
            print(f"| {i:<3} | {buku['id_buku']:<8} | {buku['judul_buku']:<30} | {buku['nama_penulis']:<25} | {buku['stok']:^5} | {buku['kategori']:<20} | {buku['tanggal']:<12} |")
        print("=" * 130)
    elif item_type == "user":
        print(f"{'👤 DAFTAR USER':^{110}}")
        print("=" * 110)
        print(f"| {'No':<3} | {'ID':<8} | {'Nama':<20} | {'Umur':^5} | {'No. Telp':<15} | {'Member':<8} | {'Username':<15} |")
        print("=" * 110)
        for i, user in enumerate(items, start=1):
            print(f"| {i:<3} | {user['id_user']:<8} | {user['nama']:<20} | {user['umur']:^5} | {user['no_telp']:<15} | {user['member']:<10} | {user['username']:<15} |")
        print("=" * 110)
    return True


def lihat_buku():
    """Mengambil dan menampilkan seluruh katalog buku untuk pengunjung yang sudah diurutkan berdasarkan abjad judul"""
    data_buku = baca_data(BUKU_FILE)
    if not data_buku:
        print("\nTidak ada data buku.")
        pause()
        return
    data_buku.sort(key=lambda buku: buku.get("judul_buku", "").lower())
    judul = "📚 DAFTAR BUKU GIE'S LIBRARY 📚"
    print(f"{judul:^{106}}")
    print("=" * 106)
    print(f"| {'No':<5} | {'Judul':<30} | {'Penulis':<25} | {'Stok':^10} | {'Kategori':^20} |")
    print("=" * 106)
    for i, buku in enumerate(data_buku, start=1):
        judul_buku = buku.get("judul_buku", "-")
        nama_penulis = buku.get("nama_penulis", "-")
        stok = buku.get("stok", "-")
        kategori = buku.get("kategori", "-")
        print(f"| {i:<5} | {judul_buku:<30} | {nama_penulis:<25} | {stok:^10} | {kategori:^20} |")
    print("=" * 106)


def pause():
    """Menjeda eksekusi program dan menunggu respons pengguna sebelum melanjutkan"""
    input("\nTekan Enter untuk melanjutkan...")


def cek_member(username):
    """Memverifikasi validitas pengunjung dengan memeriksa username dan status keanggotaannya di database"""
    data = baca_data(USER_FILE)
    for member in data:
        if member["username"] == username:
            if member["member"].lower() == "ada":
                return True
            else:
                return False
    return False


def cari_buku(input_buku, data_buku):
    """Mencari objek buku secara sekuensial berdasarkan ID atau Judul, lalu mengembalikan referensinya"""
    for buku in data_buku:
        if buku["id_buku"].lower() == input_buku.lower() or buku["judul_buku"].lower() == input_buku.lower():
            return buku  
    return None