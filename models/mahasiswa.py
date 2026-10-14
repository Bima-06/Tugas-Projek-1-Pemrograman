class Mahasiswa:
    def __init__(self, nim, nama, no_hp):
        self.nim = nim
        self.nama = nama
        self.no_hp = no_hp

    def tampilkan_info(self):
            print(f"=== NIM ===|=== Nama ===|=== Kontak ===")
            print(f"{self.nim} | {self.nama} | {self.no_hp}")
