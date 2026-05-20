from app.sistem import baca_data, clear_screen, pause
from config import USER_FILE, PEMINJAMAN_FILE
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
    # Mengambil semua data dari file JSON agar data lebih akurat dan terupdate
    semua_data = baca_data(PEMINJAMAN_FILE) 
    
    # Filter data hanya untuk user yang sedang login
    buku_saya = [data for data in semua_data if data["username"] == username_login]

    # Sesuaikan lebar tabel menjadi 90 karena ada tambahan kolom
    lebar_tabel = 90
    print(f"\n{'📋 STATUS PEMINJAMAN KAMU 📋':^{lebar_tabel}}")
    print("=" * lebar_tabel)

    if not buku_saya:
        print(f"{'Kamu belum meminjam buku apa pun saat ini.':^{lebar_tabel}}")
    else:
        print(f"| {'No':<3} | {'ID Buku':<8} | {'Judul Buku':<25} | {'Tgl Pinjam':<14} | {'Tgl Kembali':<14} |")
        print("-" * lebar_tabel)
        
        for i, item in enumerate(buku_saya, start=1):
            id_buku = item.get("id_buku", "-")
            judul = item.get("judul_buku", "-")
            
            if len(judul) > 25:
                judul = judul[:22] + "..."
                
            tgl_pinjam = item.get("tanggal_peminjaman", "-")
            
            # Jika belum dikembalikan (null/None), tampilkan '-'
            tgl_kembali = item.get("tanggal_pengembalian")
            if not tgl_kembali:
                tgl_kembali = "-"
            
            print(f"| {i:<3} | {id_buku:<8} | {judul:<25} | {tgl_pinjam:<14} | {tgl_kembali:<14} |")
    
    print("=" * lebar_tabel)
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