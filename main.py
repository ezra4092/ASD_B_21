from app.sistem import clear_screen, pause
from app.admin import admin_login, admin_menu
from app.user import login_pengunjung, user_menu
from app.peminjaman import LinkedList
from app.sistem import baca_data, lihat_buku
from config import PEMINJAMAN_FILE


def main_menu():
    """Main menu aplikasi"""
    """Inisialisasi struktur data Linked List dan memuat riwayat data peminjaman dari file"""
    ll_peminjaman = LinkedList()
    data_lama = baca_data(PEMINJAMAN_FILE)
    
    if data_lama:
        for data in data_lama:
            ll_peminjaman.tambah(data)

    """Loop utama antarmuka Main Menu"""
    while True:
        clear_screen()
        print("=" * 50)
        print("Selamat Datang di Gie's Library!")
        print("=" * 50)
        print("1. Akses Perpustakaan")
        print("2. Login Admin")
        print("0. Exit")
        
        choice = input("\nPilih menu (0-2): ").strip()
        
        if choice == "1":
            """Sub-menu untuk akses publik pengunjung perpustakaan"""
            while True:
                clear_screen()
                print("=" * 50)
                print("AKSES PERPUSTAKAAN")
                print("=" * 50)
                print("1. Lihat Daftar Buku")
                print("2. Login Member")
                print("0. Kembali")
                
                pilihan_user = input("\nPilih menu (0-2): ").strip()
                
                if pilihan_user == "1":
                    """Menampilkan katalog buku yang tersedia tanpa perlu login"""
                    lihat_buku()
                    pause()
                    
                elif pilihan_user == "2":
                    """Meneruskan pengguna ke antarmuka login dan menu member"""
                    login_pengunjung(ll_peminjaman)
                    
                elif pilihan_user == "0":
                    break
                    
                else:
                    print("\nPilihan tidak valid!")
                    pause()
                    
        elif choice == "2":
            """Menangani proses autentikasi dan meneruskan ke menu Admin jika berhasil"""
            if admin_login():
                admin_menu(ll_peminjaman)
                
        elif choice == "0":
            clear_screen()
            print("=" * 50)
            print("Terima kasih. Sampai jumpa kembali!")
            print("=" * 50)
            break
            
        else:
            print("\nPilihan tidak valid!")
            pause()


"""Titik masuk awal untuk menjalankan seluruh eksekusi program"""
if __name__ == "__main__":
    main_menu()