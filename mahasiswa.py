from tabulate import tabulate
import alat

class mahasiswa:
    def __init__(self, nim, nama, no_hp):
        self.nim = nim
        self.nama = nama
        self.no_hp = no_hp

    def register():
        register_state = True
        while register_state:
            try:

                with open("data_mahasiswa.txt", "w") as data:
                    reg_nim = input("Masukkan NIM Anda: ")
                    reg_nama = input("Masukkan Nama Anda: ")
                    reg_no_hp = input("Masukkan No HP Anda: ")
                    confirmation = input(f"Apakah benar Nama Anda {reg_nama} dengan NIM {reg_nim} dan No HP {reg_no_hp}?\n(y/n): ")

                    if confirmation.lower() == "y":
                        data[reg_nim] = {reg_nama, reg_no_hp}

                    if reg_nim not in data:
                        data[reg_nim] = [reg_nama, reg_no_hp]

            except FileNotFoundError:
                data = {}

    

    def login():
        login_state = True
        while login_state:
            try:
                with open("data_mahasiswa.txt", "r") as data:
                    user_input1 = input("Masukkan NIM Anda: ")
                    user_input2 = input("Masukkan Nama Anda ")
                    
                    nim_valid = {id: file for id, file in data() if id.upper() == user_input1.upper()}
                    nama_valid = {id: file for id, file in data() if file.upper() == user_input2.upper()}

                    if user_input1 == nim_valid and user_input2 == nama_valid:
                        login_as = user_input2
                        return login_as

            except LookupError as e:
                 print(f"Input tidak ditemukan dalam database: Error {e}")
                         

    def tampilkan_info():
            with open("data_mahasiswa.txt", "r") as data:
                kolom = ["NIM", "Nama", "Kontak"]
                print(tabulate(data, headers=kolom, tablefmt="fancy_grid"))

    def pinjam():
        pinjam_state = True
        pinjam_limit = 3
        while pinjam_state:
            try:
                if pinjam_limit <= 3:
                    
                    input_kategori = input("Masukkan kategori alat: ")
                    input_kode = input("Masukkan kode alat: ")
