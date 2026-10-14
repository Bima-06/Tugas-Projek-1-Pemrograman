from datetime import datetime
from typing import List, Optional
from models.alat import DataAlat
from models.mahasiswa import Mahasiswa


class DetailPeminjaman:
    def __init__(
        self,
        alat: DataAlat,
        kondisi_pengembalian_alat: Optional[str] = None,
        tanggal_pengembalian: Optional[datetime] = None,
        status_alat: str = "Dipinjam"
    ):
        self.alat = alat
        self.kondisi_pengembalian_alat = kondisi_pengembalian_alat
        self.tanggal_pengembalian = tanggal_pengembalian
        self.status_alat = status_alat

    def proses_pengembalian(self, kondisi: str, tanggal: datetime):
        self.kondisi_pengembalian_alat = kondisi
        self.tanggal_pengembalian = tanggal
        self.status_alat = "Dikembalikan"
        self.alat.perbarui_kondisi(kondisi)

    def __str__(self) -> str:
        tgl_kembali = self.tanggal_pengembalian.strftime("%Y-%m-%d %H:%M") if self.tanggal_pengembalian else "-"
        return f"Alat: {self.alat.nama_alat} | Status: {self.status_alat} | Kembali: {tgl_kembali}"


class TransaksiPeminjaman:
    def __init__(
        self,
        id_transaksi: str,
        peminjam: Mahasiswa,
        tanggal_pinjam: datetime,
        batas_waktu: datetime,
        status_pinjam: str = "Aktif"
    ):
        self.id_transaksi = id_transaksi
        self.peminjam = peminjam
        self.daftar_alat_dipinjam: List[DetailPeminjaman] = []
        self.tanggal_pinjam = tanggal_pinjam
        self.batas_waktu = batas_waktu
        self.status_pinjam = status_pinjam

    def tambah_alat(self, detail: DetailPeminjaman):
        self.daftar_alat_dipinjam.append(detail)
        detail.alat.ketersediaan_alat = False

    def ubah_status(self, status_baru: str):
        self.status_pinjam = status_baru

    def __str__(self) -> str:
        tgl_pinjam_str = self.tanggal_pinjam.strftime("%Y-%m-%d")
        batas_str = self.batas_waktu.strftime("%Y-%m-%d")
        return f"[{self.id_transaksi}] Peminjam: {self.peminjam.nama} ({self.peminjam.nim}) | Pinjam: {tgl_pinjam_str} | Batas: {batas_str} | Status: {self.status_pinjam}"