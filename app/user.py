from app.sistem import baca_data, clear_screen, pause
from config import USER_FILE, BUKU_FILE
# from datetime import datetime  # hapus kalau tidak dipakai


from app.sistem import baca_data, clear_screen, pause
from config import USER_FILE


def login_pengunjung(ll_peminjaman):
    data_user = baca_data(USER_FILE)

    clear_screen()
    print("=" * 50)
    print("LOGIN MEMBER")
    print("=" * 50)

    username = input("Username: ").strip()
    password = input("Password: ").strip()

    # validasi input kosong
    if username == "" or password == "":
        print("\nUsername dan password tidak boleh kosong!")
        pause()
        return

    user_ditemukan = None

    # cari user berdasarkan username dan password
    for user in data_user:
        if (
            user["username"] == username
            and user["password"] == password
        ):
            user_ditemukan = user
            break

    # kalau akun tidak ditemukan
    if user_ditemukan is None:
        print("\nUsername atau password salah!")
        pause()
        return

    # cek status member
    if user_ditemukan["member"].lower() != "ada":
        print("\nKamu belum terdaftar sebagai member!")
        print("Silakan daftar member ke admin perpustakaan.")
        pause()
        return

    # login berhasil
    print(f"\nLogin berhasil! Selamat datang, {user_ditemukan['nama']}")
    pause()

    # masuk menu member
    user_menu(username, ll_peminjaman, True)



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


def user_menu(username_login, ll_peminjaman, is_member):
    while True:
        clear_screen()

        print("=" * 50)
        print("MENU MEMBER")
        print("=" * 50)

        print("1. Lihat status peminjaman")
        print("0. Logout")

        choice = input("\nPilih menu: ")

        if choice == "1":
            lihat_status_peminjaman(username_login, ll_peminjaman)

        elif choice == "0":
            print("\nLogout berhasil.")
            pause()
            break

        else:
            print("\nPilihan tidak valid!")
            pause()