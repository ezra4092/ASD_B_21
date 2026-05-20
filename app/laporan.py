from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer
)

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

from app.sistem import *
from config import BUKU_FILE, USER_FILE, PEMINJAMAN_FILE


def cetak_laporan_pdf():
    while True:
        clear_screen()
        print("\n" + "=" * 50)
        print("Cetak Laporan PDF")
        print("=" * 50)
        print("1. Laporan Buku")
        print("2. Laporan Pengunjung")
        print("3. Laporan Peminjaman")
        print("0. Kembali")

        pilihan = input("\nPilih: ").strip()

        if pilihan == "1":
            laporan_buku_pdf()

        elif pilihan == "2":
            laporan_user_pdf()

        elif pilihan == "3":
            laporan_peminjaman_pdf()

        elif pilihan == "0":
            break

        else:
            print("\nPilihan tidak valid!")
            pause()

def laporan_buku_pdf():
    data = baca_data(BUKU_FILE)
    from datetime import datetime

    pdf = SimpleDocTemplate("laporan_buku.pdf")

    elements = []
    styles = getSampleStyleSheet()

    title = Paragraph("LAPORAN DATA BUKU", styles['Title'])
    elements.append(title)
    elements.append(Spacer(1, 12))

    tanggal_cetak = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    tanggal = Paragraph(
        f"Tanggal Cetak: {tanggal_cetak}",
        styles['Normal']
    )

    elements.append(tanggal)
    elements.append(Spacer(1, 12))

    table_data = [
        ["No", "ID Buku", "Judul Buku", "Penulis", "Kategori", "Stok", "Tanggal"]
    ]

    for i, buku in enumerate(data, start=1):
        table_data.append([
            str(i),
            buku["id_buku"],
            buku["judul_buku"],
            buku["nama_penulis"],
            buku["kategori"],
            str(buku["stok"]),
            buku["tanggal"]
        ])

    table = Table(table_data, colWidths=[40, 60, 140, 110, 90, 40, 80])

    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),

        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),

        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),

        ('GRID', (0, 0), (-1, -1), 1, colors.black),

        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),

        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
    ]))

    elements.append(table)

    pdf.build(elements)

    print("\nPDF laporan buku berhasil dibuat!")
    pause()

def laporan_user_pdf():
    data = baca_data(USER_FILE)
    from datetime import datetime

    pdf = SimpleDocTemplate("laporan_pengunjung.pdf")

    elements = []
    styles = getSampleStyleSheet()

    title = Paragraph("LAPORAN DATA PENGUNJUNG", styles['Title'])
    elements.append(title)
    elements.append(Spacer(1, 12))

    tanggal_cetak = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    tanggal = Paragraph(
        f"Tanggal Cetak: {tanggal_cetak}",
        styles['Normal']
    )

    elements.append(tanggal)
    elements.append(Spacer(1, 12))

    table_data = [
        ["No", "ID User", "Nama", "Umur", "No Telp", "Username", "Member"]
    ]

    for i, user in enumerate(data, start=1):
        table_data.append([
            str(i),
            user["id_user"],
            user["nama"],
            user["umur"],
            user["no_telp"],
            user["username"],
            user["member"]
        ])

    table = Table(
        table_data,
        colWidths=[35, 55, 100, 45, 90, 100, 55]
    )

    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkgreen),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),

        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),

        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),

        ('GRID', (0, 0), (-1, -1), 1, colors.black),

        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),

        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
    ]))

    elements.append(table)

    pdf.build(elements)

    print("\nPDF laporan pengunjung berhasil dibuat!")
    pause()

def laporan_peminjaman_pdf():
    data = baca_data(PEMINJAMAN_FILE)
    from datetime import datetime

    pdf = SimpleDocTemplate("laporan_peminjaman.pdf")

    elements = []
    styles = getSampleStyleSheet()

    title = Paragraph("LAPORAN DATA PEMINJAMAN", styles['Title'])
    elements.append(title)
    elements.append(Spacer(1, 12))

    tanggal_cetak = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    tanggal = Paragraph(
        f"Tanggal Cetak: {tanggal_cetak}",
        styles['Normal']
    )

    elements.append(tanggal)
    elements.append(Spacer(1, 12))

    table_data = [
        ["No", "Username", "ID Buku", "Judul Buku", "Tanggal Pinjam"]
    ]

    for i, item in enumerate(data, start=1):
        table_data.append([
            str(i),
            item["username"],
            item["id_buku"],
            item["judul_buku"],
            item["tanggal_peminjaman"]
        ])

    table = Table(
        table_data,
        colWidths=[35, 60, 90, 180, 100]
    )

    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkred),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),

        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),

        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),

        ('GRID', (0, 0), (-1, -1), 1, colors.black),

        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),

        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
    ]))

    elements.append(table)

    pdf.build(elements)

    print("\nPDF laporan peminjaman berhasil dibuat!")
    pause()