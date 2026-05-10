from app.sistem import baca_data, clear_screen, pause
from config import USER_FILE, BUKU_FILE
from datetime import datetime


def login_pengunjung(ll_peminjaman):
    data_user = baca_data(USER_FILE)

    username = input("Username: ").strip()
    password = input("Password: ").strip()

    user_ditemukan = None

    for user in data_user:
        if user["username"] == username:
            user_ditemukan = user
            break
    
    if user_ditemukan is None:
        print("\nAkun tidak ditemukan! Silakan registrasi terlebih dahulu.")
        pause()
        return False
    
    if user_ditemukan["password"] == password:
        print(f"\nLogin berhasil! Selamat datang, {user_ditemukan['nama']}")
        pause()
        user_menu(username, ll_peminjaman)
        return True
    
    else:
        print("\n  ✗ Username atau Password salah!")
        pause()
        return False
    
def lihat_buku():
    data_buku = baca_data(BUKU_FILE)

    if not data_buku:
        print("\nTidak ada data buku.")
        pause()
        return

    print(f"{'📚 DAFTAR BUKU GIE\'S LIBRARY 📚':^{106}}")
    print("=" * 106)
    print(f"| {'No':<5} | {'Judul':<30} | {'Penulis':<25} | {'Stok':^10} | {'Kategori':^20} |")
    print("=" * 106)

    for i, buku in enumerate(data_buku, start=1):
        judul_buku = buku.get("judul_buku", "-")
        nama_penulis = buku.get("nama_penulis", "-")
        stok = buku.get("stok", "-")
        kategori = buku.get("kategori", "-")

        print(f"| {i:<5} | {judul_buku:<30} | {nama_penulis:<25} | {stok:^10} | {kategori:^20} | ")

    print("=" * 106)

def lihat_status_peminjaman(username_login, ll_peminjaman):
    semua_data = ll_peminjaman.to_list()
    
    buku_saya = [data for data in semua_data if data["username"] == username_login]

    print(f"\n{'📋 STATUS PEMINJAMAN KAMU 📋':^{72}}")
    print("=" * 72)

    if not buku_saya:
        print(f"{'Kamu belum meminjam buku apa pun saat ini.':^72}")
    else:
        print(f"| {'No':<3} | {'ID Buku':<8} | {'Judul Buku':<25} | {'Tanggal Pinjam':<14} |")
        print("-" * 72)
        
        for i, item in enumerate(buku_saya, start=1):
            id_buku = item.get("id_buku", "-")
            judul = item.get("judul_buku", "-")
            
            if len(judul) > 25:
                judul = judul[:22] + "..."
                
            tanggal = item.get("tanggal_peminjaman", "-")
            
            print(f"| {i:<3} | {id_buku:<8} | {judul:<25} | {tanggal:<14} |")
    
    print("=" * 72)
    pause()

def user_menu(username_login, ll_peminjaman):
    while True:
        clear_screen()
        print("=" * 50)
        print("Menu Pengunjung")
        print("=" * 50)
        print("1. Lihat daftar buku")
        print("2. Lihat status peminjaman")
        print("0. Logout")

        choice = input("\nPilih: ")

        if choice == "1":
            lihat_buku()
            pause()
        elif choice == "2":
            lihat_status_peminjaman(username_login, ll_peminjaman)
            pause()
        elif choice == "0":
            print("\nLogout berhasil. Sampai jumpa!")
            pause()
            break