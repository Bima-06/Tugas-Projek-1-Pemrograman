from datetime import datetime, timedelta

from models.alat import DataAlat
from models.kategori import KategoriAlat
from models.mahasiswa import Mahasiswa
from models.transaksi import DetailPeminjaman, TransaksiPeminjaman
from utils.logger import Logger


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
        self.logger = Logger()

        # Panggil sampel data dummy otomatis
        self._muat_data_awal()

    def _muat_data_awal(self) -> None:
        """Mengisi sampel data awal ke dalam sistem."""
        self.tambah_kategori("KAT01", "Perangkat Komputasi")
        self.tambah_kategori("KAT02", "Perangkat Jaringan")
        self.tambah_kategori("KAT03", "Perangkat Multimedia")

        self.tambah_alat("ALT01", "Laptop Dell XPS 15", "KAT01", "Baik")
        self.tambah_alat("ALT02", "Router MikroTik RB750", "KAT02", "Baik")
        self.tambah_alat("ALT03", "Kamera DSLR Canon", "KAT03", "Baik")
        self.tambah_alat("ALT04", "Proyektor Epson", "KAT03", "Baik")

        self.tambah_mahasiswa("K3525023", "Dennis Pratama Saputra", "081234567890")
        self.tambah_mahasiswa("K3525048", "Allicya Nailah Fairuza", "082345678901")
        self.tambah_mahasiswa("K3525051", "Arofa Karindra Bimantara", "083456789012")

    # ---------- Helper Internal ----------
    def _transaksi_aktif(self, nim: str | None = None) -> list[TransaksiPeminjaman]:
        nim_clean = nim.strip().upper() if nim else None
        return [
            t for t in self.data_transaksi.values()
            if t.status_pinjam != self.STATUS_SELESAI and (nim_clean is None or t.peminjam.nim == nim_clean)
        ]

    def _alat_sedang_dipinjam(self) -> set[str]:
        sedang_dipinjam = set()
        for t in self._transaksi_aktif():
            for detail in t.daftar_alat_dipinjam:
                if detail.status_alat == "Dipinjam":
                    sedang_dipinjam.add(detail.alat.kode_alat)
        return sedang_dipinjam

    def _validasi_kondisi(self, kondisi: str) -> str:
        kondisi_title = kondisi.strip().title()
        if kondisi_title not in self.KONDISI_VALID:
            raise ValueError(f"Kondisi harus salah satu dari: {', '.join(self.KONDISI_VALID)}.")
        return kondisi_title

    # ---------- CRUD Kategori ----------
    def tambah_kategori(self, id_kategori: str, nama: str) -> KategoriAlat:
        id_clean = id_kategori.strip().upper()
        if id_clean in self.data_kategori:
            raise ValueError(f"Kategori {id_clean} sudah ada.")
        kat = KategoriAlat(id_clean, nama.strip())
        self.data_kategori[id_clean] = kat
        self.logger.info(f"Kategori ditambahkan: [{id_clean}] {nama}")
        return kat

    def hapus_kategori(self, id_kategori: str) -> None:
        id_clean = id_kategori.strip().upper()
        if id_clean not in self.data_kategori:
            raise KeyError(f"Kategori {id_clean} tidak ditemukan.")
        if any(a.kategori.id_kategori == id_clean for a in self.data_alat.values()):
            raise ValueError("Kategori masih dipakai oleh alat.")
        del self.data_kategori[id_clean]
        self.logger.info(f"Kategori dihapus: {id_clean}")

    def daftar_kategori(self) -> list[KategoriAlat]:
        return list(self.data_kategori.values())

    # ---------- CRUD Mahasiswa ----------
    def tambah_mahasiswa(self, nim: str, nama: str, no_hp: str) -> Mahasiswa:
        nim_clean = nim.strip().upper()
        if nim_clean in self.data_mahasiswa:
            raise ValueError(f"NIM {nim_clean} sudah terdaftar.")
        mhs = Mahasiswa(nim_clean, nama.strip(), no_hp.strip())
        self.data_mahasiswa[nim_clean] = mhs
        self.logger.info(f"Mahasiswa ditambahkan: [{nim_clean}] {nama}")
        return mhs

    def ubah_mahasiswa(self, nim: str, nama: str | None = None, no_hp: str | None = None) -> Mahasiswa:
        mhs = self.get_mahasiswa(nim)
        mhs.nama = nama.strip() if nama else mhs.nama
        mhs.no_hp = no_hp.strip() if no_hp else mhs.no_hp
        self.logger.info(f"Data Mahasiswa {mhs.nim} diperbarui")
        return mhs

    def hapus_mahasiswa(self, nim: str) -> None:
        nim_clean = nim.strip().upper()
        self.get_mahasiswa(nim_clean)
        if self._transaksi_aktif(nim_clean):
            raise ValueError("Mahasiswa masih memiliki transaksi aktif.")
        del self.data_mahasiswa[nim_clean]
        self.logger.info(f"Mahasiswa dihapus: {nim_clean}")

    def get_mahasiswa(self, nim: str) -> Mahasiswa:
        nim_clean = nim.strip().upper()
        if nim_clean not in self.data_mahasiswa:
            raise KeyError(f"Mahasiswa dengan NIM {nim_clean} tidak ditemukan.")
        return self.data_mahasiswa[nim_clean]

    def daftar_mahasiswa(self) -> list[Mahasiswa]:
        return list(self.data_mahasiswa.values())

    # ---------- CRUD Alat ----------
    def tambah_alat(self, kode: str, nama: str, id_kategori: str, kondisi: str = "Baik") -> DataAlat:
        kode_clean = kode.strip().upper()
        id_kat_clean = id_kategori.strip().upper()
        if kode_clean in self.data_alat:
            raise ValueError(f"Kode alat {kode_clean} sudah ada.")
        if id_kat_clean not in self.data_kategori:
            raise KeyError(f"Kategori {id_kat_clean} tidak ditemukan.")
        kondisi_valid = self._validasi_kondisi(kondisi)
        alat = DataAlat(kode_clean, nama.strip(), self.data_kategori[id_kat_clean], kondisi_valid)
        self.data_alat[kode_clean] = alat
        self.logger.info(f"Alat ditambahkan: [{kode_clean}] {nama}")
        return alat

    def ubah_kondisi_alat(self, kode: str, kondisi: str) -> DataAlat:
        kode_clean = kode.strip().upper()
        alat = self.get_alat(kode_clean)
        kondisi_valid = self._validasi_kondisi(kondisi)
        alat.perbarui_kondisi(kondisi_valid)
        self.logger.info(f"Kondisi alat {kode_clean} diubah menjadi {kondisi_valid}")
        return alat

    def hapus_alat(self, kode: str) -> None:
        kode_clean = kode.strip().upper()
        self.get_alat(kode_clean)
        if kode_clean in self._alat_sedang_dipinjam():
            raise ValueError("Alat sedang terlibat transaksi aktif.")
        del self.data_alat[kode_clean]
        self.logger.info(f"Alat dihapus: {kode_clean}")

    def get_alat(self, kode: str) -> DataAlat:
        kode_clean = kode.strip().upper()
        if kode_clean not in self.data_alat:
            raise KeyError(f"Alat {kode_clean} tidak ditemukan.")
        return self.data_alat[kode_clean]

    def daftar_alat(self) -> list[DataAlat]:
        return list(self.data_alat.values())

    def daftar_alat_tersedia(self) -> list[DataAlat]:
        dipinjam = self._alat_sedang_dipinjam()
        return [a for k, a in self.data_alat.items() if a.alat_tersedia() and k not in dipinjam]

    def daftar_alat_dipinjam(self) -> list[DataAlat]:
        dipinjam_kode = self._alat_sedang_dipinjam()
        return [self.data_alat[k] for k in dipinjam_kode if k in self.data_alat]

    # ---------- Transaksi Peminjaman ----------
    def pinjam(self, nim: str, kode_alat: list[str]) -> TransaksiPeminjaman:
        nim_clean = nim.strip().upper()
        mhs = self.get_mahasiswa(nim_clean)

        kode_clean_list = [k.strip().upper() for k in kode_alat if k.strip()]
        if not kode_clean_list or len(set(kode_clean_list)) != len(kode_clean_list):
            raise ValueError("Daftar alat kosong atau duplikat.")

        if len(self._transaksi_aktif(nim_clean)) >= self.MAKS_TRANSAKSI_AKTIF:
            raise ValueError(f"Maksimal {self.MAKS_TRANSAKSI_AKTIF} transaksi aktif per mahasiswa.")

        tersedia = {a.kode_alat for a in self.daftar_alat_tersedia()}
        for kode in kode_clean_list:
            self.get_alat(kode)
            if kode not in tersedia:
                raise ValueError(f"Alat {kode} tidak tersedia (rusak/sedang dipinjam).")

        self._counter_transaksi += 1
        id_trx = f"TRX{self._counter_transaksi:04d}"
        hari_ini = datetime.now()
        batas_waktu = hari_ini + timedelta(days=self.LAMA_PINJAM_HARI)

        trx = TransaksiPeminjaman(id_trx, mhs, hari_ini, batas_waktu, status_pinjam=self.STATUS_DIPINJAM)

        for kode in kode_clean_list:
            detail = DetailPeminjaman(self.get_alat(kode))
            trx.tambah_alat(detail)

        self.data_transaksi[id_trx] = trx
        self.logger.info(f"Transaksi {id_trx} dibuat untuk NIM {nim_clean} ({len(kode_clean_list)} alat)")
        return trx

    def kembalikan(self, id_transaksi: str, pengembalian: dict[str, str]) -> TransaksiPeminjaman:
        id_clean = id_transaksi.strip().upper()
        trx = self.get_transaksi(id_clean)

        if trx.status_pinjam == self.STATUS_SELESAI:
            raise ValueError("Transaksi sudah selesai.")
        if not pengembalian:
            raise ValueError("Tidak ada alat yang dikembalikan.")

        pengembalian_clean = {k.strip().upper(): v for k, v in pengembalian.items()}
        kode_alat_dalam_trx = [d.alat.kode_alat for d in trx.daftar_alat_dipinjam if d.status_alat == "Dipinjam"]

        for kode, kondisi in pengembalian_clean.items():
            if kode not in kode_alat_dalam_trx:
                raise ValueError(f"Alat {kode} tidak valid untuk dikembalikan pada transaksi ini.")
            self._validasi_kondisi(kondisi)

        sekarang = datetime.now()
        for detail in trx.daftar_alat_dipinjam:
            kode = detail.alat.kode_alat
            if kode in pengembalian_clean and detail.status_alat == "Dipinjam":
                kondisi_baru = self._validasi_kondisi(pengembalian_clean[kode])
                detail.proses_pengembalian(kondisi_baru, sekarang)

        semua_kembali = all(d.status_alat == "Dikembalikan" for d in trx.daftar_alat_dipinjam)
        trx.ubah_status(self.STATUS_SELESAI if semua_kembali else self.STATUS_SEBAGIAN)
        self.logger.info(f"Pengembalian diproses untuk {id_clean} | Status akhir: {trx.status_pinjam}")
        return trx

    def get_transaksi(self, id_transaksi: str) -> TransaksiPeminjaman:
        id_clean = id_transaksi.strip().upper()
        if id_clean not in self.data_transaksi:
            raise KeyError(f"Transaksi {id_clean} tidak ditemukan.")
        return self.data_transaksi[id_clean]

    def daftar_transaksi(self, hanya_aktif: bool = False) -> list[TransaksiPeminjaman]:
        return self._transaksi_aktif() if hanya_aktif else list(self.data_transaksi.values())