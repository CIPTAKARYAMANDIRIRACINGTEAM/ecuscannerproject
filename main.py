import sys
from PyQt5.QtWidgets import QApplication
from ui.main_window import ECUScannerApp  # Impor dari folder `ui`

if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        main_window = ECUScannerApp()
        main_window.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(f"Error saat menjalankan aplikasi: {e}")
