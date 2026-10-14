class Mahasiswa:
    def __init__(self, nim, nama, no_hp):
        self.nim = nim
        self.nama = nama
        self.no_hp = no_hp

    def tampilkan_info(self):
            kolom = ["NIM", "Nama", "Kontak"]
            print(tabulate(self.nim, self.nama, self.no_hp, headers=kolom, tablefmt="fancy_grid"))
