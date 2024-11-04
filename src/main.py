from PyQt5.QtWidgets import QApplication
from ui.main_window import ECUScannerApp
import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = ECUScannerApp()
    main_window.show()
    sys.exit(app.exec_())
