import os
from datetime import datetime
from models.kategori import KategoriAlat
from models.mahasiswa import Mahasiswa
from models.alat import DataAlat
from models.transaksi import TransaksiPeminjaman, DetailPeminjaman

class FileHandler:
    DATA_DIR = "data"

    @classmethod
    def _pastikan_folder_ada(cls) -> None:
        if not os.path.exists(cls.DATA_DIR):
            os.makedirs(cls.DATA_DIR)

    @classmethod
    def _baca_baris(cls, nama_file: str) -> list[list[str]]:
        cls._pastikan_folder_ada()
        path = os.path.join(cls.DATA_DIR, nama_file)
        if not os.path.exists(path):
            with open(path, "w", encoding="utf-8") as f:
                pass
            return []
        
        hasil = []
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line_str = line.strip()
                if not line_str or line_str.startswith("#"):
                    continue
                parts = [p.strip() for p in line_str.split("|")]
                hasil.append(parts)
        return hasil

    # --- Kategori ---
    @classmethod
    def simpan_kategori(cls, data_kategori: dict) -> None:
        cls._pastikan_folder_ada()
        path = os.path.join(cls.DATA_DIR, "kategori.txt")
        with open(path, "w", encoding="utf-8") as f:
            for k in data_kategori.values():
                f.write(f"{k.id_kategori}|{k.nama_kategori}\n")

    @classmethod
    def muat_kategori(cls) -> dict[str, KategoriAlat]:
        baris_list = cls._baca_baris("kategori.txt")
        kategori_dict = {}
        for parts in baris_list:
            try:
                if len(parts) >= 2:
                    kategori_dict[parts[0]] = KategoriAlat(parts[0], parts[1])
            except Exception as e:
                print(f"[Peringatan] Baris kategori dilewati: {parts} ({e})")
        return kategori_dict

    # --- Mahasiswa ---
    @classmethod
    def simpan_mahasiswa(cls, data_mahasiswa: dict) -> None:
        cls._pastikan_folder_ada()
        path = os.path.join(cls.DATA_DIR, "mahasiswa.txt")
        with open(path, "w", encoding="utf-8") as f:
            for m in data_mahasiswa.values():
                f.write(f"{m.nim}|{m.nama}|{m.no_hp}\n")

    @classmethod
    def muat_mahasiswa(cls) -> dict[str, Mahasiswa]:
        baris_list = cls._baca_baris("mahasiswa.txt")
        mhs_dict = {}
        for parts in baris_list:
            try:
                if len(parts) >= 3:
                    mhs_dict[parts[0]] = Mahasiswa(parts[0], parts[1], parts[2])
            except Exception as e:
                print(f"[Peringatan] Baris mahasiswa dilewati: {parts} ({e})")
        return mhs_dict

    # --- Alat ---
    @classmethod
    def simpan_alat(cls, data_alat: dict) -> None:
        cls._pastikan_folder_ada()
        path = os.path.join(cls.DATA_DIR, "alat.txt")
        with open(path, "w", encoding="utf-8") as f:
            for a in data_alat.values():
                f.write(f"{a.kode_alat}|{a.nama_alat}|{a.kategori.id_kategori}|{a.kondisi_alat}\n")

    @classmethod
    def muat_alat(cls, data_kategori: dict) -> dict[str, DataAlat]:
        baris_list = cls._baca_baris("alat.txt")
        alat_dict = {}
        for parts in baris_list:
            try:
                if len(parts) >= 4:
                    kode, nama, id_kat, kondisi = parts[0], parts[1], parts[2], parts[3]
                    if id_kat in data_kategori:
                        alat_dict[kode] = DataAlat(kode, nama, data_kategori[id_kat], kondisi)
            except Exception as e:
                print(f"[Peringatan] Baris alat dilewati: {parts} ({e})")
        return alat_dict

    # --- Transaksi & Detail ---
    @classmethod
    def simpan_transaksi(cls, data_transaksi: dict) -> None:
        cls._pastikan_folder_ada()
        path_trx = os.path.join(cls.DATA_DIR, "transaksi.txt")
        path_det = os.path.join(cls.DATA_DIR, "detail_transaksi.txt")
        
        with open(path_trx, "w", encoding="utf-8") as f_trx, open(path_det, "w", encoding="utf-8") as f_det:
            for t in data_transaksi.values():
                tgl_p = t.tanggal_pinjam.strftime("%Y-%m-%d")
                batas_p = t.batas_waktu.strftime("%Y-%m-%d")
                f_trx.write(f"{t.id_transaksi}|{t.peminjam.nim}|{tgl_p}|{batas_p}|{t.status_pinjam}\n")
                
                for d in t.daftar_alat_dipinjam:
                    kondisi_k = d.kondisi_pengembalian_alat if d.kondisi_pengembalian_alat else "-"
                    tgl_k = d.tanggal_pengembalian.strftime("%Y-%m-%d %H:%M:%S") if d.tanggal_pengembalian else "-"
                    f_det.write(f"{t.id_transaksi}|{d.alat.kode_alat}|{d.status_alat}|{kondisi_k}|{tgl_k}\n")

    @classmethod
    def muat_transaksi(cls, data_mahasiswa: dict, data_alat: dict) -> tuple[dict[str, TransaksiPeminjaman], int]:
        baris_trx = cls._baca_baris("transaksi.txt")
        baris_det = cls._baca_baris("detail_transaksi.txt")
        
        transaksi_dict = {}
        counter_max = 0

        for parts in baris_trx:
            try:
                if len(parts) >= 5:
                    id_trx, nim, tgl_p, batas_p, status = parts[0], parts[1], parts[2], parts[3], parts[4]
                    if nim in data_mahasiswa:
                        tgl_dt = datetime.strptime(tgl_p, "%Y-%m-%d")
                        batas_dt = datetime.strptime(batas_p, "%Y-%m-%d")
                        trx = TransaksiPeminjaman(id_trx, data_mahasiswa[nim], tgl_dt, batas_dt, status)
                        transaksi_dict[id_trx] = trx
                        
                        if id_trx.startswith("TRX"):
                            num = int(id_trx.replace("TRX", ""))
                            if num > counter_max:
                                counter_max = num
            except Exception as e:
                print(f"[Peringatan] Baris transaksi dilewati: {parts} ({e})")

        for parts in baris_det:
            try:
                if len(parts) >= 5:
                    id_trx, kode_alat, status_alat, kondisi_k, tgl_k = parts[0], parts[1], parts[2], parts[3], parts[4]
                    if id_trx in transaksi_dict and kode_alat in data_alat:
                        alat_obj = data_alat[kode_alat]
                        kondisi_val = None if kondisi_k == "-" else kondisi_k
                        tgl_val = datetime.strptime(tgl_k, "%Y-%m-%d %H:%M:%S") if tgl_k != "-" else None
                        
                        detail = DetailPeminjaman(alat_obj, kondisi_val, tgl_val, status_alat)
                        transaksi_dict[id_trx].daftar_alat_dipinjam.append(detail)
                        
                        if status_alat == "Dipinjam":
                            alat_obj.ketersediaan_alat = False
            except Exception as e:
                print(f"[Peringatan] Baris detail transaksi dilewati: {parts} ({e})")

        return transaksi_dict, counter_max