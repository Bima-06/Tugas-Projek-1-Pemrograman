from models.kategori import KategoriAlat

class DataAlat:
    def __init__(self, kode_alat: str, nama_alat: str, kategori: KategoriAlat, kondisi_alat: str = "Baik"):
        self.kode_alat = kode_alat
        self.nama_alat = nama_alat
        self.kategori = kategori
        self.kondisi_alat = kondisi_alat
        self.ketersediaan_alat = True if kondisi_alat.lower() == "baik" else False

    def perbarui_kondisi(self, kondisi_baru: str):
        self.kondisi_alat = kondisi_baru
        if kondisi_baru.lower() == "baik":
            self.ketersediaan_alat = True
        else:
            self.ketersediaan_alat = False

    def alat_tersedia(self) -> bool:
        return self.ketersediaan_alat

    def tampilkan_info(self) -> str:
        status = "Tersedia" if self.ketersediaan_alat else "Tidak Tersedia"
        return f"[{self.kode_alat}] {self.nama_alat} | Kategori: {self.kategori.nama_kategori} | Kondisi: {self.kondisi_alat} | Status: {status}"