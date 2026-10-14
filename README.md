# Sistem Pengelolaan Peminjaman Peralatan Laboratorium

## Anggota Kelompok
1. Dennis Pratama Saputra - K3525023
2. Allicya Nailah Fairuza - K3525048
3. Arofa Karindra Bimantara - K3525051

## Deskripsi Sistem
Aplikasi berbasis Python dengan pendekatan Object-Oriented Programming (OOP) untuk mengelola peminjaman dan pengembalian peralatan laboratorium. Sistem ini mengelola data mahasiswa, inventaris alat, transaksi peminjaman multi-item, pengembalian sebagian, serta pencatatan kondisi alat menggunakan *built-in collection* tanpa database external.

## Struktur Program
```text
Tugas Projek 1 Pemrograman/
│
├── models/
│   ├── alat.py
│   ├── kategori.py
│   ├── mahasiswa.py
│   └── transaksi.py
├── controllers/
│   └── sistem_peminjaman.py
├── ui/
│   └── menu_ui.py
├── utils/
│   └── logger.py
├── main.py
└── README.md
```
## Pembagian Kontribusi Anggota
Dennis Pratama Saputra (K3525023): models/mahasiswa.py

Allicya Nailah Fairuza (K3525048): models/transaksi.py

Arofa Karindra Bimantara (K3525051): models/alat.py, models/kategori.py