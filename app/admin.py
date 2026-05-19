from app.sistem import *
from config import *
from app.peminjaman import peminjaman_menu, LinkedList
from datetime import datetime
from app.laporan import cetak_laporan_pdf

def admin_login():
    """Admin login"""
    clear_screen()

    print("=" * 50)
    print("Login Admin - Gie's Library")
    print("=" * 50)

    username = input("\nUsername: ").strip()
    password = input("Password: ").strip()

    # validasi input kosong
    if username == "" or password == "":
        print("\nUsername dan password tidak boleh kosong!")
        pause()
        return False

    # validasi login admin
    if username == ADMIN_USN and password == ADMIN_PW:
        print("\nLogin berhasil! Selamat datang, Admin!")
        pause()
        return True

    else:
        print("\nUsername atau password salah!")
        pause()
        return False

def tampil_data(file, item_type):
    clear_screen()
    print("=" * 50)
    print(f"Dashboard Admin - Tampil Data {item_type}")
    print("=" * 50)
    
    data = baca_data(file)

    # ubah string ke dict kalau perlu
    data = [eval(item) if isinstance(item, str) else item for item in data]

    if data:
        if item_type == "buku":
            print("\nUrutan tampilan:")
            print("1. Alfabet (judul buku)")
            print("2. Data terbaru")
            sort_choice = input("\nPilih urutan (1/2): ").strip()
            
            if sort_choice == "1":
                # SORT BERDASARKAN JUDUL
                data = sorted(data, key=lambda x: x['judul_buku'].lower())
            
            elif sort_choice == "2":
                # SORT BERDASARKAN TANGGAL TERBARU
                data = sorted(
                    data,
                    key=lambda x: datetime.strptime(x['tanggal'], "%d-%m-%Y"),
                    reverse=True
                )
            else:
                print("Input tidak sesuai, default A-Z")
                data = sorted(data, key=lambda x: x['judul_buku'].lower())

        elif item_type == "user":
            print("\nUrutan tampilan:")
            print("1. Alfabet (nama user)")
            print("2. ID User")
            print("3. Status Member")

            pilih = input("Pilih urutan (1/2/3): ").strip()

            if pilih == "1":
                data = sorted(data, key=lambda x: x['nama'].lower())

            elif pilih == "2":
                data = sorted(data, key=lambda x: x['id_user'])

            elif pilih == "3":
                data = sorted(data, key=lambda x: 0 if x['member'] == "ada" else 1)

            else:
                print("Default: Nama")
                data = sorted(data, key=lambda x: x['nama'].lower())


    cek_data(data, item_type)
    pause()

def tambah_data(file, item_type):
    """Generic add function"""
    clear_screen()
    print("=" * 50)
    print(f"Dashboard Admin - Tambah Data {item_type}")
    print("=" * 50)
    
    data = baca_data(file)
    
    if item_type == "buku":
        id_buku = input("\nKode Buku: ").strip().upper()
        kategori = input("Kategori: ").strip()
        judul_buku = input("Judul Buku: ").strip()
        nama_penulis = input("Nama Penulis: ").strip()
        stok = input("Stok: ").strip()
        tanggal = datetime.now().strftime("%d-%m-%Y")
        
        if any(item['id_buku'] == id_buku for item in data):
            print("\nKode Buku sudah ada! Gunakan kode lain.")
            pause()
            return
        
        new_item = {
            "id_buku": id_buku,
            "kategori": kategori,
            "judul_buku": judul_buku,
            "nama_penulis": nama_penulis,
            "stok": stok,
            "tanggal": tanggal
        }
        
    elif item_type == "user":
        while True:
            id_user = input("\nID User: ").strip().upper()
            if any(item['id_user'] == id_user for item in data):
                print("\nID User sudah ada! Gunakan ID lain.")
            else:
                break
        nama = input("Nama: ").strip()
        umur = input("Umur: ").strip()
        no_telp = input("No. Telp: ").strip()
        member = input("Member (ada/tidak ada): ").strip()
        while True:
            username = input("Username: ").strip()
            if username == "":
                print("Username tidak boleh kosong!")
            elif any(user["username"] == username for user in data):
                print("Username sudah digunakan!")
            else:
                break
        password = input("Password: ").strip()
        
        
        new_item = {
            "id_user": id_user,
            "nama": nama,
            "umur": umur,
            "no_telp": no_telp,
            "member": member,
            "username": username,
            "password": password
        }
    
    else:
        print("\nTipe data tidak dikenali!")
        pause()
        return
    
    data.append(new_item)
    simpan_data(file, data)
    print("\n✓ Data berhasil ditambahkan!")
    pause()

def edit_data(file, item_type):
    """Generic edit function"""
    clear_screen()
    print("=" * 50)
    print(f"Dashboard Admin - Edit Data {item_type}")
    print("=" * 50)
    
    data = baca_data(file)
    
    if not cek_data(data, item_type):
        pause()
        return
    
    try:
        idx = int(input("\nPilih nomor data yang ingin diedit: ").strip())
        if idx < 1 or idx > len(data):
            raise ValueError
    except ValueError:
        print("\nInput tidak valid!")
        pause()
        return
    
    item = data[idx - 1]
    
    if item_type == "buku":
        print("\nKosongkan input untuk mempertahankan nilai lama.")
        kategori = input(f"Kategori ({item['kategori']}): ").strip() or item['kategori']
        judul_buku = input(f"Judul Buku ({item['judul_buku']}): ").strip() or item['judul_buku']
        nama_penulis = input(f"Nama Penulis ({item['nama_penulis']}): ").strip() or item['nama_penulis']
        stok = input(f"Stok ({item['stok']}): ").strip() or item['stok']
        
        # Update data
        item.update({
            "kategori": kategori,
            "judul_buku": judul_buku,
            "nama_penulis": nama_penulis,
            "stok": stok,
            "tanggal": datetime.now().strftime("%d-%m-%Y") 
        })
    elif item_type == "user":
        print("\nKosongkan input untuk mempertahankan nilai lama.")
        nama = input(f"Nama ({item['nama']}): ").strip() or item['nama']
        umur = input(f"Umur ({item['umur']}): ").strip() or item['umur']
        no_telp = input(f"No. Telp ({item['no_telp']}): ").strip() or item['no_telp']
        member = input(f"Member ({item['member']}): ").strip() or item['member']
        
        # Update data
        item.update({
            "nama": nama,
            "umur": umur,
            "no_telp": no_telp,
            "member": member
        })
        
    simpan_data(file, data)
    print("\nData berhasil diperbarui!")
    pause()

def hapus_data(file, item_type):   
    """Generic delete function"""
    clear_screen()
    print("=" * 50)
    print(f"Dashboard Admin - Hapus Data {item_type}")
    print("=" * 50)
    
    data = baca_data(file)
    
    if not cek_data(data, item_type):
        pause()
        return
    
    try:
        idx = int(input("\nPilih nomor data yang ingin dihapus: ").strip())
        if idx < 1 or idx > len(data):
            raise ValueError
    except ValueError:
        print("\nInput tidak valid!")
        pause()
        return
    
    confirm = input("\nApakah Anda yakin ingin menghapus data ini? (y/n): ").strip().lower()
    if confirm == 'y':
        del data[idx - 1]
        simpan_data(file, data)
        print("\nData berhasil dihapus!")
    else:
        print("\nPenghapusan dibatalkan.")
    
    pause()

def cari_data(file, item_type):
    clear_screen()
    print("=" * 50)
    print(f"Dashboard Admin - Cari Data {item_type}")
    print("=" * 50)
    
    data = baca_data(file)

    # ubah ke dict kalau masih string
    data = [eval(item) if isinstance(item, str) else item for item in data]

    if not data:
        print(f"\nBelum ada data {item_type}.")
        pause()
        return
    
    
    if item_type == "buku":
        keyword = input("\nMasukkan judul buku atau nama penulis: ").strip().lower()
        hasil = [
            item for item in data
            if keyword in item['judul_buku'].lower()
            or keyword in item['nama_penulis'].lower()
        ]
    elif item_type == "user":
        keyword = input("\nMasukkan nama atau username: ").strip().lower()
        hasil = [
            item for item in data
            if keyword in item['nama'].lower()
            or keyword in item['username'].lower()
        ]
    
    # ✅ LANGSUNG TAMPILKAN HASIL
    if hasil:
        cek_data(hasil, item_type)
    else:
        print("\n❌ Data tidak ditemukan.")
    
    pause()

def crud_menu(file, item_type):
    """Generic CRUD menu"""
    while True:
        clear_screen()
        print("=" * 50)
        print(f"Dashboard Admin - Data {item_type}")
        print("=" * 50)
        print("1. Tampilkan Daftar")
        print("2. Tambah Data")
        print("3. Edit Data")
        print("4. Hapus Data")
        print("5. Cari Data")
        print("0. Kembali")
        
        choice = input("\nPilih (0-4): ").strip()
        
        if choice == "1":
            tampil_data(file, item_type)
        elif choice == "2":
            tambah_data(file, item_type)
        elif choice == "3":
            edit_data(file, item_type)
        elif choice == "4":
            hapus_data(file, item_type)
        elif choice == "5":
            cari_data(file, item_type)
        elif choice == "0":
            break

def admin_menu(ll_peminjaman):
    """Admin main menu"""
    ll_peminjaman = LinkedList()
    while True:
        clear_screen()
        print("=" * 50)
        print("Dashboard Admin - Gie's Library")
        print("=" * 50)
        print("1. Kelola Data Buku")
        print("2. Kelola Data Pengunjung")
        print("3. Kelola Data Peminjaman")
        print("4. Cetak Laporan PDF")
        print("0. Logout")
        
        choice = input("\nPilih (0-2): ").strip()
        
        if choice == "1":
            crud_menu(BUKU_FILE, "buku")
        elif choice == "2":
            crud_menu(USER_FILE, "user")
        elif choice == "3":
            peminjaman_menu(ll_peminjaman)
        elif choice == "4":
            cetak_laporan_pdf()
        elif choice == "0":
            print("\nLogging out...")
            pause()
            break
    