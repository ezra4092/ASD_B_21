# Gie's Library - Sistem Peminjaman Perpustakaan
Gie's Library adalah aplikasi manajemen perpustakaan berbasis Command Line Interface (CLI) menggunakan python. Aplikasi ini dibuat untuk membantu proses pengelolaan data buku, data pengunjung, peminjaman buku, pengembalian buku, serta pembuatan laporan dalam bentuk PDF.

## Overview

Gie's Library menyediakan beberapa fitur utama, yaitu:

- Manajemen data buku
- Manajemen data pengunjung/member
- Login Admin dan Login Member
- Sistem peminjaman dan pengembalian buku
- Cetak laporan PDF
- Penyimpanan data menggunakan file JSON
- Implementasi struktur data Linked List dan Stack

## Features

- CLI-based application dengan tampilan terminal yang rapi
- Role-based access untuk Admin dan Pengunjung
- CRUD data buku
- CRUD data pengunjung
- Proses peminjaman buku
- Edit data peminjaman untuk pengembalian buku
- Undo peminjaman terakhir menggunakan Stack
- Linked List untuk menyimpan data peminjaman sementara
- File handling menggunakan JSON
- Sorting data buku dan pengunjung
- Searching data buku dan pengunjung
- Generate laporan PDF menggunakan ReportLab
- Error handling pada input pengguna

## Kelompok 21

| Nama | NIM |
| Ezra Faira Azzahra Faisal | J0403251030 |
| Shofia Aziza Iman | J0403251050 |
| Alyya Putri Sekarwangi | J0403251109 |

## Pembagian Tugas

### Ezra Faira Azzahra Faisal
- Admin Login
- Kelola Data Buku
- Kelola Data Pengunjung
- Kelola Data Peminjaman Buku
- Kelola Fitur Undo Peminjaman

### Shofia Aziza Iman
- Membuat Data Pengunjung
- Pengunjung Login
- Admin Cetak Laporan PDF
- Dokumentasi Program

### Alyya Putri Sekarwangi
- Membuat Data Buku
- Pengunjung Lihat Daftar Buku
- Pengunjung Lihat Status Peminjaman
- Dokumentasi Program

## Project Structure

```text
Gies-Library/
├── main.py              # Entry point aplikasi
├── config.py            # Konfigurasi & konstanta (Path DB, Kredensial)
├── app/                 # Package modul utama
│   ├── admin.py         # Logika menu dan operasi khusus Admin
│   └── user.py          # Logika pengunjung (login, menu user)
│   ├── peminjaman.py    # Logika transaksi pinjam-kembali buku
│   └── laporan.py       # Mencetak laporan laporan dalam bentuk PDF
│   ├── sistem.py        # Utility functions (clear_screen, pause, dll)
└── data/                # JSON database
    ├── buku_perpus.json # Menyimpan data koleksi buku
    ├── peminjaman.json  # Menyimpan riwayat transaksi
    └── user.json        # Menyimpan akun pengunjung
```
## Modules
| Module | Fungsi |
|---------|---------|
| main.py | Entry point program dan menu utama aplikasi |
| config.py | Menyimpan path file JSON dan kredensial admin |
| app/sistem.py | Utility function seperti baca data, simpan data, clear screen, dan pause |
| app/admin.py | Login admin dan pengelolaan data oleh admin |
| app/user.py | Login pengunjung dan menu member |
| app/peminjaman.py | Proses peminjaman, pengembalian, Linked List, dan Stack |
| app/laporan.py | Generate laporan PDF menggunakan ReportLab |
| data/*.json | Penyimpanan data buku, user, dan peminjaman |

## Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/ezra4092/Gies-Library.git
cd Gies-Library
```

### 2. Install Library

Project ini menggunakan library eksternal ReportLab untuk membuat laporan PDF.
```bash
pip install reportlab
```

### 3. Jalankan Program
``` bash
python main.py
```

## Admin Login

Kredensial default admin:

```text
Username: `admin`
Password: `admin123`
```

## Usage

### User Flow (Pengunjung)

1. Pilih menu **Akses Perpustakaan**
2. Pilih **Login Member**
3. Masukkan username dan password
4. Sistem melakukan validasi data member
5. Jika berhasil login, pengguna masuk ke Menu Member
6. Pengguna dapat melihat status peminjaman buku yang dimiliki

### Admin Flow

1. Pilih menu **Login Admin**
2. Masukkan username dan password admin
3. Sistem melakukan validasi login
4. Jika berhasil login, admin masuk ke Dashboard Admin
5. Admin dapat:
   - Mengelola Data Buku
   - Mengelola Data Pengunjung
   - Mengelola Data Peminjaman
   - Melakukan Undo Peminjaman
   - Mencetak Laporan PDF

## Data Structure

Aplikasi menggunakan 3 file JSON utama untuk meniru *Relational Database*.

### 1. Buku (`buku_perpus.json`)
Menyimpan detail katalog buku.
```json
{
  "id_buku": "BKU01",
  "kategori": "Novel",
  "judul_buku": "Bumi Manusia",
  "nama_penulis": "Pramoedya Ananta Toer",
  "stok": 2,
  "tanggal": "20-02-2018"
}
```

### 2. User (`user.json`)
Menyimpan data otentikasi pengunjung.
```json
{
  "id_user": "U001",
  "nama": "Shofia",
  "umur": "17",
  "no_telp": "008123456778",
  "member": "ada",
  "username": "shofia",
  "password": "123"
}
```

### 3. Peminjaman (`peminjaman.json`)
Melacak relasi antara *User* dan *Buku*.
```json
{
  "username": "shofia",
  "id_buku": "BKU20",
  "judul_buku": "The Jakarta Method",
  "tanggal_peminjaman": "20-05-2026",
  "tanggal_pengembalian": "20-05-2026"
}
```
## Data Structures & Algorithms

### Linked List

Linked list digunakan untuk menyimpan data sementara selama program berjalan

### Stack

Stack digunakan untuk menyimpan riwayat transaksi peminjaman terakhir menggunakan konsep LIFO (*Last In First Out*), sehingga admin dapat melakukan fitur Undo terhadap transaksi terakhir.

### Sorting

Sorting digunakan pada fitur tampil data.

#### Data Buku
- Berdasarkan Judul Buku (Ascending)
- Berdasarkan Tanggal Terbaru (Descending)

#### Data Pengunjung
- Berdasarkan Nama
- Berdasarkan ID User
- Berdasarkan Status Member

### Searching

Searching digunakan untuk pencarian data berdasarkan keyword.

#### Data Buku
- Judul Buku
- Nama Penulis

#### Data Pengunjung
- Nama Pengunjung
- Username

## PDF Report Generation

Aplikasi dapat menghasilkan laporan PDF menggunakan library ReportLab.

### Jenis Laporan

#### 1. Laporan Buku
Berisi:
- Nomor Data
- ID Buku
- Judul Buku
- Nama Penulis
- Kategori
- Stok
- Tanggal Data

#### 2. Laporan Pengunjung
Berisi:
- Nomor Data
- ID User
- Nama
- Umur
- Nomor Telepon
- Username
- Status Member

#### 3. Laporan Peminjaman
Berisi:
- Nomor Data
- Username
- ID Buku
- Judul Buku
- Tanggal Peminjaman
- Tanggal Pengembalian

### Format Nama File PDF

Laporan disimpan secara otomatis menggunakan timestamp sehingga tidak menimpa file sebelumnya.

Contoh:

```text
laporan_buku_23-06-2026_09-15-20.pdf
laporan_pengunjung_23-06-2026_09-16-12.pdf
laporan_peminjaman_23-06-2026_09-17-05.pdf
```

## Libraries

### External Library

```bash
pip install reportlab
```

### Built-in Python Libraries

- json
- os
- datetime

## Requirements Checklist

- [x] Aplikasi berbasis CLI
- [x] Bahasa Pemrograman Python
- [x] File Handling JSON
- [x] CRUD Operations
- [x] Login Admin
- [x] Login Pengunjung
- [x] Linked List
- [x] Stack
- [x] Sorting
- [x] Searching
- [x] Error Handling
- [x] Generate PDF
- [x] Modular Programming

## Video Demonstrasi

Link Video:

```text
https://youtu.be/_nJqKNKlqbE
```

Video mencakup:
- Penjelasan alur program
- Demonstrasi fitur
- Penjelasan struktur data
- Penjelasan input dan output
- Demonstrasi cetak laporan PDF

## Learning Outcomes

Melalui project ini kami berhasil mengimplementasikan:

- Modular Programming
- JSON File Handling
- CRUD Operations
- Authentication System
- Linked List
- Stack (LIFO)
- Sorting Algorithm
- Searching Algorithm
- Error Handling
- PDF Report Generation

ke dalam sebuah aplikasi Sistem Manajemen Perpustakaan berbasis Command Line Interface (CLI) menggunakan Python.

## Conclusion

Gie's Library merupakan aplikasi manajemen perpustakaan berbasis Python CLI yang membantu proses pengelolaan data buku, data pengunjung, peminjaman, pengembalian, serta pembuatan laporan PDF. Aplikasi ini menerapkan konsep struktur data, algoritma pencarian dan pengurutan, modular programming, serta file handling JSON sebagai media penyimpanan data.

Repository: ASD_B_21