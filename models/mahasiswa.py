class Mahasiswa:
    def __init__(self, nim: str, nama: str, no_hp: str) -> None:
        self.nim = nim
        self.nama = nama
        self.no_hp = no_hp

    def tampilkan_info(self) -> str:
        return f"[{self.nim}] {self.nama} | HP: {self.no_hp}"