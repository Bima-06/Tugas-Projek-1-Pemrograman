class KategoriAlat:
    def __init__(self, id_kategori: str, nama_kategori: str):
        self.id_kategori = id_kategori
        self.nama_kategori = nama_kategori

    def __str__(self) -> str:
        return self.nama_kategori