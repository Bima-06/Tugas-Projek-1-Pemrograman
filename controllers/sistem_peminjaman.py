from datetime import datetime, timedelta

from models.alat import DataAlat
from models.kategori import KategoriAlat
from models.mahasiswa import Mahasiswa
from models.transaksi import DetailPeminjaman, TransaksiPeminjaman


class SistemPeminjaman:
    MAKS_TRANSAKSI_AKTIF: int = 2
    LAMA_PINJAM_HARI: int = 7
    KONDISI_VALID: tuple[str, ...] = ("Baik", "Rusak Ringan", "Rusak Berat")
    STATUS_DIPINJAM: str = "Aktif"
    STATUS_SEBAGIAN: str = "Sebagian dikembalikan"
    STATUS_SELESAI: str = "Selesai"

    def __init__(self) -> None:
        self.data_mahasiswa: dict[str, Mahasiswa] = {}
        self.data_alat: dict[str, DataAlat] = {}
        self.data_kategori: dict[str, KategoriAlat] = {}
        self.data_transaksi: dict[str, TransaksiPeminjaman] = {}
        self._counter_transaksi: int = 0

    #  Helper Internal 
    def _transaksi_aktif(self, nim: str | None = None) -> list[TransaksiPeminjaman]:
        return [
            t for t in self.data_transaksi.values()
            if t.status_pinjam != self.STATUS_SELESAI and (nim is None or t.peminjam.nim == nim)
        ]

    def _alat_sedang_dipinjam(self) -> set[str]:
        sedang_dipinjam = set()
        for t in self._transaksi_aktif():
            for detail in t.daftar_alat_dipinjam:
                if detail.status_alat == "Dipinjam":
                    sedang_dipinjam.add(detail.alat.kode_alat)
        return sedang_dipinjam

    #  CRUD Kategori 
    def tambah_kategori(self, id_kategori: str, nama: str) -> KategoriAlat:
        if id_kategori in self.data_kategori:
            raise ValueError(f"Kategori {id_kategori} sudah ada.")
        kat = KategoriAlat(id_kategori, nama)
        self.data_kategori[id_kategori] = kat
        return kat

    def hapus_kategori(self, id_kategori: str) -> None:
        if id_kategori not in self.data_kategori:
            raise KeyError(f"Kategori {id_kategori} tidak ditemukan.")
        if any(a.kategori.id_kategori == id_kategori for a in self.data_alat.values()):
            raise ValueError("Kategori masih dipakai oleh alat.")
        del self.data_kategori[id_kategori]

    def daftar_kategori(self) -> list[KategoriAlat]:
        return list(self.data_kategori.values())

    #  CRUD Mahasiswa 
    def tambah_mahasiswa(self, nim: str, nama: str, no_hp: str) -> Mahasiswa:
        if nim in self.data_mahasiswa:
            raise ValueError(f"NIM {nim} sudah terdaftar.")
        mhs = Mahasiswa(nim, nama, no_hp)
        self.data_mahasiswa[nim] = mhs
        return mhs

    def ubah_mahasiswa(self, nim: str, nama: str | None = None, no_hp: str | None = None) -> Mahasiswa:
        mhs = self.get_mahasiswa(nim)
        mhs.nama = nama or mhs.nama
        mhs.no_hp = no_hp or mhs.no_hp
        return mhs

    def hapus_mahasiswa(self, nim: str) -> None:
        self.get_mahasiswa(nim)
        if self._transaksi_aktif(nim):
            raise ValueError("Mahasiswa masih memiliki transaksi aktif.")
        del self.data_mahasiswa[nim]

    def get_mahasiswa(self, nim: str) -> Mahasiswa:
        if nim not in self.data_mahasiswa:
            raise KeyError(f"Mahasiswa dengan NIM {nim} tidak ditemukan.")
        return self.data_mahasiswa[nim]

    def daftar_mahasiswa(self) -> list[Mahasiswa]:
        return list(self.data_mahasiswa.values())

    #  CRUD Alat 
    def tambah_alat(self, kode: str, nama: str, id_kategori: str, kondisi: str = "Baik") -> DataAlat:
        if kode in self.data_alat:
            raise ValueError(f"Kode alat {kode} sudah ada.")
        if id_kategori not in self.data_kategori:
            raise KeyError(f"Kategori {id_kategori} tidak ditemukan.")
        self._validasi_kondisi(kondisi)
        alat = DataAlat(kode, nama, self.data_kategori[id_kategori], kondisi)
        self.data_alat[kode] = alat
        return alat

    def ubah_kondisi_alat(self, kode: str, kondisi: str) -> DataAlat:
        alat = self.get_alat(kode)
        self._validasi_kondisi(kondisi)
        alat.perbarui_kondisi(kondisi)
        return alat

    def hapus_alat(self, kode: str) -> None:
        self.get_alat(kode)
        if kode in self._alat_sedang_dipinjam():
            raise ValueError("Alat sedang terlibat transaksi aktif.")
        del self.data_alat[kode]

    def get_alat(self, kode: str) -> DataAlat:
        if kode not in self.data_alat:
            raise KeyError(f"Alat {kode} tidak ditemukan.")
        return self.data_alat[kode]

    def daftar_alat(self) -> list[DataAlat]:
        return list(self.data_alat.values())

    def daftar_alat_tersedia(self) -> list[DataAlat]:
        dipinjam = self._alat_sedang_dipinjam()
        return [a for k, a in self.data_alat.items() if a.alat_tersedia() and k not in dipinjam]

    def daftar_alat_dipinjam(self) -> list[DataAlat]:
        dipinjam_kode = self._alat_sedang_dipinjam()
        return [self.data_alat[k] for k in dipinjam_kode if k in self.data_alat]

    def _validasi_kondisi(self, kondisi: str) -> None:
        if kondisi not in self.KONDISI_VALID:
            raise ValueError(f"Kondisi harus salah satu dari: {', '.join(self.KONDISI_VALID)}.")

    #  Transaksi Peminjaman 
    def pinjam(self, nim: str, kode_alat: list[str]) -> TransaksiPeminjaman:
        mhs = self.get_mahasiswa(nim)
        if not kode_alat or len(set(kode_alat)) != len(kode_alat):
            raise ValueError("Daftar alat kosong atau duplikat.")
        if len(self._transaksi_aktif(nim)) >= self.MAKS_TRANSAKSI_AKTIF:
            raise ValueError(f"Maksimal {self.MAKS_TRANSAKSI_AKTIF} transaksi aktif per mahasiswa.")

        tersedia = {a.kode_alat for a in self.daftar_alat_tersedia()}
        for kode in kode_alat:
            self.get_alat(kode)
            if kode not in tersedia:
                raise ValueError(f"Alat {kode} tidak tersedia (rusak/sedang dipinjam).")

        self._counter_transaksi += 1
        id_trx = f"TRX{self._counter_transaksi:04d}"
        hari_ini = datetime.now()
        batas_waktu = hari_ini + timedelta(days=self.LAMA_PINJAM_HARI)

        trx = TransaksiPeminjaman(id_trx, mhs, hari_ini, batas_waktu, status_pinjam=self.STATUS_DIPINJAM)

        for kode in kode_alat:
            detail = DetailPeminjaman(self.get_alat(kode))
            trx.tambah_alat(detail)

        self.data_transaksi[id_trx] = trx
        return trx

    def kembalikan(self, id_transaksi: str, pengembalian: dict[str, str]) -> TransaksiPeminjaman:
        """pengembalian: {kode_alat: kondisi_saat_kembali}; boleh sebagian."""
        trx = self.get_transaksi(id_transaksi)
        if trx.status_pinjam == self.STATUS_SELESAI:
            raise ValueError("Transaksi sudah selesai.")
        if not pengembalian:
            raise ValueError("Tidak ada alat yang dikembalikan.")

        kode_alat_dalam_trx = [d.alat.kode_alat for d in trx.daftar_alat_dipinjam if d.status_alat == "Dipinjam"]
        for kode, kondisi in pengembalian.items():
            if kode not in kode_alat_dalam_trx:
                raise ValueError(f"Alat {kode} tidak valid untuk dikembalikan pada transaksi ini.")
            self._validasi_kondisi(kondisi)

        sekarang = datetime.now()
        for detail in trx.daftar_alat_dipinjam:
            kode = detail.alat.kode_alat
            if kode in pengembalian and detail.status_alat == "Dipinjam":
                kondisi_baru = pengembalian[kode]
                detail.proses_pengembalian(kondisi_baru, sekarang)

        semua_kembali = all(d.status_alat == "Dikembalikan" for d in trx.daftar_alat_dipinjam)
        trx.ubah_status(self.STATUS_SELESAI if semua_kembali else self.STATUS_SEBAGIAN)
        return trx

    def get_transaksi(self, id_transaksi: str) -> TransaksiPeminjaman:
        if id_transaksi not in self.data_transaksi:
            raise KeyError(f"Transaksi {id_transaksi} tidak ditemukan.")
        return self.data_transaksi[id_transaksi]

    def daftar_transaksi(self, hanya_aktif: bool = False) -> list[TransaksiPeminjaman]:
        return self._transaksi_aktif() if hanya_aktif else list(self.data_transaksi.values())