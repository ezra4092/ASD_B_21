import json
import os
from config import *
from datetime import datetime


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def baca_data(filename):
    try:
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    except Exception as e:
        print(f"Error loading {filename}: {e}")
        return []
    
def simpan_data(filename, data):
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving {filename}: {e}")
        return False
    

def simpan_peminjaman(ll_peminjaman, PEMINJAMAN_FILE):
    data_list = ll_peminjaman.to_list()

    if not data_list:
        print("\nBelum ada data peminjaman. Tidak bisa disimpan.")
        return

    try:
        # cek kalau file sudah ada → append
        try:
            with open(PEMINJAMAN_FILE, "r") as f:
                data_lama = json.load(f)
        except:
            data_lama = []

        # gabungkan data lama + baru
        data_lama.extend(data_list)

        # simpan ke file
        with open(PEMINJAMAN_FILE, "w") as f:
            json.dump(data_lama, f, indent=4)

        print("\nData peminjaman berhasil disimpan ke JSON!")

    except Exception as e:
        print(f"Terjadi error saat menyimpan: {e}")
    
def cek_data(items, item_type):
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

def pause():
    """Pause and wait for user input"""
    input("\nTekan Enter untuk melanjutkan...")

def cek_member(username):
    data = baca_data(USER_FILE)
    
    for member in data:
        if member["username"] == username:
            if member["member"].lower() == "ada":
                return True
            else:
                return False
    
    return False


def cari_buku(input_buku, data_buku):
    for buku in data_buku:
        if buku["id_buku"] == input_buku or buku["judul_buku"].lower() == input_buku.lower():
            return buku  # ⬅️ ini referensi ke data asli
    return None