from controllers.sistem_peminjaman import SistemPeminjaman
from ui.menu_ui import MenuUI


def main() -> None:
    sistem = SistemPeminjaman()
    app = MenuUI(sistem)
    app.jalankan()


if __name__ == "__main__":
    main()