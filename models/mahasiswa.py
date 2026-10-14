from tabulate import tabulate
class Mahasiswa:
    def __init__(self, nim, nama, no_hp):
        self.nim = nim
        self.nama = nama
        self.no_hp = no_hp

    def tampilkan_info(self):
            kolom = ["NIM", "Nama", "Kontak"]
            print(tabulate(self.nim, self.nama, self.kontak, headers=kolom, tablefmt="fancy_grid"))

    def tambah_mahasiswa(self, nim, nama, no_hp):
        if nim in self.data_mahasiswa:
              print(f"Error: NIM {nim} telah terdaftar di database!")
        else:
            self.data_mahasiswa[nim] = Mahasiswa(nim, nama, no_hp)
            return self.data_mahasiswa[nim]

    def get_mahasiswa(self, nim):
        if nim not in self.data_mahasiswa:
              print(f"Error: NIM {nim} tidak terdaftar di database!")
        else:
            return self.dat_mahasiswa[nim]

    def ubah_mahasiswa(self, nim, nama, no_hp):
        mhs = self.get_mahasiswa(nim)
        mhs.nama = nama or mhs.nama
        mhs.no_hp = no_hp or mhs.no_hp
        return mhs

    def hapus_mahasiswa(self, nim):
        self.get_mahasiswa(nim)
        if self.transaksi_aktif(nim):
              print("Mahasiswa masih memiliki alat yang belum dikembalikan.")
        else:
            del self.data_mahasiswa[nim]

    def daftar_mahasiswa(self):
         return list(self.data_mahasiswa.values())