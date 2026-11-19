from datetime import datetime
from database import Database
from models.kategori import KategoriAlat
from models.mahasiswa import Mahasiswa
from models.alat import DataAlat
from models.transaksi import TransaksiPeminjaman, DetailPeminjaman


class DatabaseHandler:
    _db = Database()

    # ==================== MUAT DATA (SELECT) ====================
    @classmethod
    def muat_kategori(cls) -> dict[str, KategoriAlat]:
        conn = cls._db.connect()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT kode_kategori, nama_kategori FROM kategori ORDER BY kode_kategori")
                rows = cur.fetchall()
            return {r["kode_kategori"]: KategoriAlat(r["kode_kategori"], r["nama_kategori"]) for r in rows}
        finally:
            conn.close()

    @classmethod
    def muat_mahasiswa(cls) -> dict[str, Mahasiswa]:
        conn = cls._db.connect()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT nim, nama, no_telp FROM mahasiswa ORDER BY nim")
                rows = cur.fetchall()
            return {r["nim"]: Mahasiswa(r["nim"], r["nama"], r["no_telp"]) for r in rows}
        finally:
            conn.close()

    @classmethod
    def muat_alat(cls, data_kategori: dict[str, KategoriAlat]) -> dict[str, DataAlat]:
        conn = cls._db.connect()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT kode_alat, nama_alat, kode_kategori, kondisi FROM alat ORDER BY kode_alat")
                rows = cur.fetchall()
            alat_dict = {}
            for r in rows:
                kat = data_kategori.get(r["kode_kategori"])
                if kat:
                    alat_dict[r["kode_alat"]] = DataAlat(r["kode_alat"], r["nama_alat"], kat, r["kondisi"])
            return alat_dict
        finally:
            conn.close()

    @classmethod
    def muat_transaksi(
        cls, data_mahasiswa: dict[str, Mahasiswa], data_alat: dict[str, DataAlat]
    ) -> tuple[dict[str, TransaksiPeminjaman], int]:
        conn = cls._db.connect()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM transaksi ORDER BY kode_transaksi")
                trx_rows = cur.fetchall()
                cur.execute("SELECT * FROM detail_transaksi ORDER BY id_detail")
                det_rows = cur.fetchall()

            transaksi_dict = {}
            counter_max = 0

            for r in trx_rows:
                mhs = data_mahasiswa.get(r["nim"])
                if not mhs:
                    continue
                tgl_p = r["tanggal_pinjam"]
                batas_p = r["tanggal_rencana_kembali"]
                if not isinstance(tgl_p, datetime):
                    tgl_p = datetime.combine(tgl_p, datetime.min.time())
                if not isinstance(batas_p, datetime):
                    batas_p = datetime.combine(batas_p, datetime.min.time())

                id_trx = r["kode_transaksi"]
                transaksi_dict[id_trx] = TransaksiPeminjaman(id_trx, mhs, tgl_p, batas_p, r["status"])

                if id_trx.startswith("TRX"):
                    num = int(id_trx.replace("TRX", ""))
                    if num > counter_max:
                        counter_max = num

            for d in det_rows:
                trx = transaksi_dict.get(d["kode_transaksi"])
                alat_obj = data_alat.get(d["kode_alat"])
                if trx and alat_obj:
                    detail = DetailPeminjaman(
                        alat_obj,
                        d["kondisi_kembali"],
                        d["waktu_kembali"],
                        d["status_item"]
                    )
                    trx.daftar_alat_dipinjam.append(detail)
                    if d["status_item"] == "Dipinjam":
                        alat_obj.ketersediaan_alat = False

            return transaksi_dict, counter_max
        finally:
            conn.close()

    # ==================== KATEGORI (CRUD) ====================
    @classmethod
    def insert_kategori(cls, kat: KategoriAlat) -> None:
        conn = cls._db.connect()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO kategori (kode_kategori, nama_kategori) VALUES (%s, %s)",
                    (kat.id_kategori, kat.nama_kategori)
                )
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    @classmethod
    def delete_kategori(cls, id_kategori: str) -> None:
        conn = cls._db.connect()
        try:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM kategori WHERE kode_kategori = %s", (id_kategori,))
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    # ==================== MAHASISWA (CRUD) ====================
    @classmethod
    def insert_mahasiswa(cls, mhs: Mahasiswa) -> None:
        conn = cls._db.connect()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO mahasiswa (nim, nama, no_telp) VALUES (%s, %s, %s)",
                    (mhs.nim, mhs.nama, mhs.no_hp)
                )
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    @classmethod
    def update_mahasiswa(cls, mhs: Mahasiswa) -> None:
        conn = cls._db.connect()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE mahasiswa SET nama = %s, no_telp = %s WHERE nim = %s",
                    (mhs.nama, mhs.no_hp, mhs.nim)
                )
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    @classmethod
    def delete_mahasiswa(cls, nim: str) -> None:
        conn = cls._db.connect()
        try:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM mahasiswa WHERE nim = %s", (nim,))
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    # ==================== ALAT (CRUD) ====================
    @classmethod
    def insert_alat(cls, alat: DataAlat) -> None:
        conn = cls._db.connect()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO alat (kode_alat, nama_alat, kode_kategori, kondisi) VALUES (%s, %s, %s, %s)",
                    (alat.kode_alat, alat.nama_alat, alat.kategori.id_kategori, alat.kondisi_alat)
                )
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    @classmethod
    def update_kondisi_alat(cls, kode_alat: str, kondisi: str) -> None:
        conn = cls._db.connect()
        try:
            with conn.cursor() as cur:
                cur.execute("UPDATE alat SET kondisi = %s WHERE kode_alat = %s", (kondisi, kode_alat))
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    @classmethod
    def delete_alat(cls, kode_alat: str) -> None:
        conn = cls._db.connect()
        try:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM alat WHERE kode_alat = %s", (kode_alat,))
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    # ==================== TRANSAKSI (ACID TRANSACTION) ====================
    @classmethod
    def insert_transaksi(cls, trx: TransaksiPeminjaman) -> None:
        conn = cls._db.connect()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    """INSERT INTO transaksi 
                       (kode_transaksi, nim, tanggal_pinjam, tanggal_rencana_kembali, status)
                       VALUES (%s, %s, %s, %s, %s)""",
                    (
                        trx.id_transaksi,
                        trx.peminjam.nim,
                        trx.tanggal_pinjam.strftime("%Y-%m-%d"),
                        trx.batas_waktu.strftime("%Y-%m-%d"),
                        trx.status_pinjam
                    )
                )
                for d in trx.daftar_alat_dipinjam:
                    cur.execute(
                        """INSERT INTO detail_transaksi 
                           (kode_transaksi, kode_alat, status_item, kondisi_kembali, waktu_kembali)
                           VALUES (%s, %s, %s, %s, %s)""",
                        (trx.id_transaksi, d.alat.kode_alat, d.status_alat, None, None)
                    )
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    @classmethod
    def update_pengembalian(cls, trx: TransaksiPeminjaman) -> None:
        conn = cls._db.connect()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE transaksi SET status = %s WHERE kode_transaksi = %s",
                    (trx.status_pinjam, trx.id_transaksi)
                )
                for d in trx.daftar_alat_dipinjam:
                    if d.status_alat == "Dikembalikan":
                        tgl_k = d.tanggal_pengembalian.strftime("%Y-%m-%d %H:%M:%S") if d.tanggal_pengembalian else None
                        cur.execute(
                            """UPDATE detail_transaksi 
                               SET status_item = %s, kondisi_kembali = %s, waktu_kembali = %s
                               WHERE kode_transaksi = %s AND kode_alat = %s""",
                            (d.status_alat, d.kondisi_pengembalian_alat, tgl_k, trx.id_transaksi, d.alat.kode_alat)
                        )
                        cur.execute(
                            "UPDATE alat SET kondisi = %s WHERE kode_alat = %s",
                            (d.alat.kondisi_alat, d.alat.kode_alat)
                        )
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()