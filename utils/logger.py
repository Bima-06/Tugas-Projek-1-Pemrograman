import os
from datetime import datetime

class Logger:
    def __init__(self, file_path: str = "app.log"):
        self.file_path = file_path
        # Memastikan file log dibuat jika belum ada
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w", encoding="utf-8") as f:
                f.write("=== LOG AKTIVITAS SISTEM PEMINJAMAN ===\n")

    def log(self, pesan: str, tingkat: str = "INFO"):
        """Mencatat pesan log dengan timestamp dan tingkat keparahan (INFO/WARNING/ERROR)."""
        waktu_sekarang = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        format_log = f"[{waktu_sekarang}] [{tingkat.upper()}] {pesan}\n"
        
        # Menuliskan baris log ke dalam file
        with open(self.file_path, "a", encoding="utf-8") as f:
            f.write(format_log)

    def info(self, pesan: str):
        self.log(pesan, tingkat="INFO")

    def warning(self, pesan: str):
        self.log(pesan, tingkat="WARNING")

    def error(self, pesan: str):
        self.log(pesan, tingkat="ERROR")

    def baca_log(self) -> str:
        """Membaca seluruh isi catatan dari file log."""
        if os.path.exists(self.file_path):
            with open(self.file_path, "r", encoding="utf-8") as f:
                return f.read()
        return "File log tidak ditemukan."