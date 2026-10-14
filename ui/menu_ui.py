import os
from controllers.sistem_peminjaman import SistemPeminjaman


class MenuUI:
    def __init__(self, sistem: SistemPeminjaman) -> None:
        self.sistem = sistem

    # ---------- Helper Tampilan ----------
    def _bersihkan_layar(self) -> None:
        os.system("cls" if os.name == "nt" else "clear")

    def _header(self, judul: str) -> None:
        print("=" * 55)
        print(f" {judul.center(51)} ")
        print("=" * 55)

    def _pause(self) -> None:
        input("\nTekan [Enter] untuk melanjutkan...")

    # ---------- Main Menu Loop ----------
    def jalankan(self) -> None:
        while True:
            self._bersihkan_layar()
            self._header("SISTEM PEMINJAMAN ALAT LABORATORIUM")
            print("1. Kelola Kategori Alat")
            print("2. Kelola Data Alat")
            print("3. Kelola Data Mahasiswa")
            print("4. Transaksi Peminjaman")
            print("5. Transaksi Pengembalian")
            print("6. Lihat Daftar Transaksi")
            print("0. Keluar")
            print("-" * 55)

            pilihan = input("Pilih menu [0-6]: ").strip()

            if pilihan == "1":
                self._menu_kategori()
            elif pilihan == "2":
                self._menu_alat()
            elif pilihan == "3":
                self._menu_mahasiswa()
            elif pilihan == "4":
                self._menu_pinjam()
            elif pilihan == "5":
                self._menu_kembalikan()
            elif pilihan == "6":
                self._menu_daftar_transaksi()
            elif pilihan == "0":
                print("\nTerima kasih telah menggunakan sistem ini.")
                break
            else:
                print("\n[Peringatan] Pilihan menu tidak valid!")
                self._pause()

    # ---------- Menu Kategori ----------
    def _menu_kategori(self) -> None:
        while True:
            self._bersihkan_layar()
            self._header("KELOLA KATEGORI ALAT")
            print("1. Tambah Kategori")
            print("2. Tampilkan Semua Kategori")
            print("3. Hapus Kategori")
            print("0. Kembali ke Menu Utama")
            print("-" * 55)

            pilihan = input("Pilih menu [0-3]: ").strip()

            if pilihan == "1":
                print("\n--- Tambah Kategori ---")
                id_kat = input("ID Kategori   : ").strip()
                nama = input("Nama Kategori : ").strip()
                try:
                    self.sistem.tambah_kategori(id_kat, nama)
                    print("[Sukses] Kategori berhasil ditambahkan!")
                except (ValueError, KeyError) as e:
                    print(f"[Gagal] {e}")
                self._pause()

            elif pilihan == "2":
                print("\n--- Daftar Kategori ---")
                kategori_list = self.sistem.daftar_kategori()
                if not kategori_list:
                    print("Belum ada data kategori.")
                else:
                    for k in kategori_list:
                        print(f"- ID: {k.id_kategori:<10} | Nama: {k.nama_kategori}")
                self._pause()

            elif pilihan == "3":
                print("\n--- Hapus Kategori ---")
                id_kat = input("ID Kategori yang akan dihapus: ").strip()
                try:
                    self.sistem.hapus_kategori(id_kat)
                    print("[Sukses] Kategori berhasil dihapus!")
                except (ValueError, KeyError) as e:
                    print(f"[Gagal] {e}")
                self._pause()

            elif pilihan == "0":
                break

    # ---------- Menu Alat ----------
    def _menu_alat(self) -> None:
        while True:
            self._bersihkan_layar()
            self._header("KELOLA DATA ALAT")
            print("1. Tambah Alat Baru")
            print("2. Ubah Kondisi Alat")
            print("3. Hapus Alat")
            print("4. Lihat Semua Alat")
            print("5. Lihat Alat Tersedia")
            print("6. Lihat Alat Dipinjam")
            print("0. Kembali ke Menu Utama")
            print("-" * 55)

            pilihan = input("Pilih menu [0-6]: ").strip()

            if pilihan == "1":
                print("\n--- Tambah Alat Baru ---")
                kode = input("Kode Alat   : ").strip()
                nama = input("Nama Alat   : ").strip()
                id_kat = input("ID Kategori : ").strip()
                print(f"Opsi kondisi: {', '.join(self.sistem.KONDISI_VALID)}")
                kondisi = input("Kondisi (Default: Baik): ").strip() or "Baik"

                try:
                    self.sistem.tambah_alat(kode, nama, id_kat, kondisi)
                    print("[Sukses] Alat berhasil ditambahkan!")
                except (ValueError, KeyError) as e:
                    print(f"[Gagal] {e}")
                self._pause()

            elif pilihan == "2":
                print("\n--- Ubah Kondisi Alat ---")
                kode = input("Kode Alat: ").strip()
                print(f"Opsi kondisi valid: {', '.join(self.sistem.KONDISI_VALID)}")
                kondisi_baru = input("Kondisi Baru: ").strip()

                try:
                    self.sistem.ubah_kondisi_alat(kode, kondisi_baru)
                    print("[Sukses] Kondisi alat berhasil diperbarui!")
                except (ValueError, KeyError) as e:
                    print(f"[Gagal] {e}")
                self._pause()

            elif pilihan == "3":
                print("\n--- Hapus Alat ---")
                kode = input("Kode Alat yang akan dihapus: ").strip()
                try:
                    self.sistem.hapus_alat(kode)
                    print("[Sukses] Data alat berhasil dihapus!")
                except (ValueError, KeyError) as e:
                    print(f"[Gagal] {e}")
                self._pause()

            elif pilihan == "4":
                print("\n--- Semua Daftar Alat ---")
                daftar = self.sistem.daftar_alat()
                self._tampilkan_daftar_alat(daftar)
                self._pause()

            elif pilihan == "5":
                print("\n--- Daftar Alat Tersedia ---")
                daftar = self.sistem.daftar_alat_tersedia()
                self._tampilkan_daftar_alat(daftar)
                self._pause()

            elif pilihan == "6":
                print("\n--- Daftar Alat Dipinjam ---")
                daftar = self.sistem.daftar_alat_dipinjam()
                self._tampilkan_daftar_alat(daftar)
                self._pause()

            elif pilihan == "0":
                break

    def _tampilkan_daftar_alat(self, daftar: list) -> None:
        if not daftar:
            print("Tidak ada data alat.")
            return
        for a in daftar:
            if hasattr(a, "tampilkan_info"):
                print(a.tampilkan_info())
            else:
                print(f"[{a.kode_alat}] {a.nama_alat} | Kategori: {a.kategori.nama_kategori} | Kondisi: {a.kondisi_alat}")

    # ---------- Menu Mahasiswa ----------
    def _menu_mahasiswa(self) -> None:
        while True:
            self._bersihkan_layar()
            self._header("KELOLA DATA MAHASISWA")
            print("1. Tambah Mahasiswa")
            print("2. Ubah Data Mahasiswa")
            print("3. Hapus Mahasiswa")
            print("4. Tampilkan Semua Mahasiswa")
            print("0. Kembali ke Menu Utama")
            print("-" * 55)

            pilihan = input("Pilih menu [0-4]: ").strip()

            if pilihan == "1":
                print("\n--- Tambah Mahasiswa ---")
                nim = input("NIM     : ").strip()
                nama = input("Nama    : ").strip()
                no_hp = input("No HP   : ").strip()

                try:
                    self.sistem.tambah_mahasiswa(nim, nama, no_hp)
                    print("[Sukses] Mahasiswa berhasil terdaftar!")
                except ValueError as e:
                    print(f"[Gagal] {e}")
                self._pause()

            elif pilihan == "2":
                print("\n--- Ubah Data Mahasiswa ---")
                nim = input("NIM Mahasiswa: ").strip()
                nama = input("Nama Baru (kosongkan jika tidak diubah): ").strip() or None
                no_hp = input("No HP Baru (kosongkan jika tidak diubah): ").strip() or None

                try:
                    self.sistem.ubah_mahasiswa(nim, nama, no_hp)
                    print("[Sukses] Data mahasiswa berhasil diperbarui!")
                except KeyError as e:
                    print(f"[Gagal] {e}")
                self._pause()

            elif pilihan == "3":
                print("\n--- Hapus Mahasiswa ---")
                nim = input("NIM Mahasiswa yang akan dihapus: ").strip()
                try:
                    self.sistem.hapus_mahasiswa(nim)
                    print("[Sukses] Mahasiswa berhasil dihapus!")
                except (ValueError, KeyError) as e:
                    print(f"[Gagal] {e}")
                self._pause()

            elif pilihan == "4":
                print("\n--- Daftar Mahasiswa ---")
                daftar = self.sistem.daftar_mahasiswa()
                if not daftar:
                    print("Belum ada data mahasiswa.")
                else:
                    for m in daftar:
                        print(f"- NIM: {m.nim:<12} | Nama: {m.nama:<20} | No HP: {m.no_hp}")
                self._pause()

            elif pilihan == "0":
                break

    # ---------- Transaksi Peminjaman ----------
    def _menu_pinjam(self) -> None:
        self._bersihkan_layar()
        self._header("TRANSAKSI PEMINJAMAN ALAT")
        nim = input("Masukkan NIM Peminjam: ").strip()
        input_kode = input("Masukkan Kode Alat (pisahkan dengan koma, contoh: ALT01,ALT02): ").strip()

        if not input_kode:
            print("[Gagal] Kode alat tidak boleh kosong.")
            self._pause()
            return

        kode_alat = [k.strip() for k in input_kode.split(",") if k.strip()]

        try:
            trx = self.sistem.pinjam(nim, kode_alat)
            daftar_kode = [d.alat.kode_alat for d in trx.daftar_alat_dipinjam]
            print("\n[Sukses] Transaksi Peminjaman Berhasil Dibuat!")
            print(f"ID Transaksi   : {trx.id_transaksi}")
            print(f"NIM Peminjam   : {trx.peminjam.nim}")
            print(f"Tanggal Pinjam : {trx.tanggal_pinjam.strftime('%Y-%m-%d')}")
            print(f"Batas Waktu    : {trx.batas_waktu.strftime('%Y-%m-%d')}")
            print(f"Daftar Alat    : {', '.join(daftar_kode)}")
        except (ValueError, KeyError) as e:
            print(f"\n[Gagal] {e}")
        self._pause()

    # ---------- Transaksi Pengembalian ----------
    def _menu_kembalikan(self) -> None:
        self._bersihkan_layar()
        self._header("TRANSAKSI PENGEMBALIAN ALAT")
        id_trx = input("Masukkan ID Transaksi: ").strip()

        try:
            trx = self.sistem.get_transaksi(id_trx)
            alat_tersisa = [d.alat.kode_alat for d in trx.daftar_alat_dipinjam if d.status_alat == "Dipinjam"]

            if not alat_tersisa:
                print("[Peringatan] Semua alat pada transaksi ini sudah dikembalikan.")
                self._pause()
                return

            print(f"\nAlat yang belum dikembalikan: {', '.join(alat_tersisa)}")
            input_alat = input("Masukkan kode alat yang akan dikembalikan (pisahkan dengan koma): ").strip()
            
            if not input_alat:
                print("[Gagal] Tidak ada kode alat yang diinput.")
                self._pause()
                return

            kode_kembali = [k.strip() for k in input_alat.split(",") if k.strip()]
            pengembalian_dict = {}

            print(f"\nPilihan kondisi valid: {', '.join(self.sistem.KONDISI_VALID)}")
            for kode in kode_kembali:
                if kode not in alat_tersisa:
                    print(f"[Gagal] Alat {kode} tidak ada dalam daftar peminjaman aktif transaksi ini.")
                    self._pause()
                    return
                kondisi = input(f"Kondisi alat [{kode}] saat dikembalikan: ").strip()
                pengembalian_dict[kode] = kondisi

            res_trx = self.sistem.kembalikan(id_trx, pengembalian_dict)
            print("\n[Sukses] Pengembalian berhasil diproses!")
            print(f"Status Transaksi Sekarang: {res_trx.status_pinjam}")

        except (ValueError, KeyError) as e:
            print(f"\n[Gagal] {e}")
        self._pause()

    # ---------- Daftar Transaksi ----------
    def _menu_daftar_transaksi(self) -> None:
        self._bersihkan_layar()
        self._header("DAFTAR TRANSAKSI")
        print("1. Tampilkan Semua Transaksi")
        print("2. Tampilkan Hanya Transaksi Aktif")
        print("-" * 55)

        pilihan = input("Pilih [1-2]: ").strip()
        hanya_aktif = pilihan == "2"

        daftar = self.sistem.daftar_transaksi(hanya_aktif=hanya_aktif)
        print("\n--- RESULT ---")
        if not daftar:
            print("Tidak ada riwayat transaksi.")
        else:
            for t in daftar:
                total_alat = len(t.daftar_alat_dipinjam)
                dikembalikan_count = sum(1 for d in t.daftar_alat_dipinjam if d.status_alat == "Dikembalikan")
                info_kembali = f" ({dikembalikan_count}/{total_alat} alat kembali)"
                print(
                    f"[{t.id_transaksi}] NIM: {t.peminjam.nim:<10} | Status: {t.status_pinjam:<20} | "
                    f"Pinjam: {t.tanggal_pinjam.strftime('%Y-%m-%d')} | Batas: {t.batas_waktu.strftime('%Y-%m-%d')}{info_kembali}"
                )
        self._pause()
