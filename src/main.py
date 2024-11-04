from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QComboBox, QLineEdit, QMessageBox
from src.obd_connector import OBDConnector  # Pastikan jalur impor benar
import sys

class ECUScannerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ECU Scanner")
        self.setGeometry(100, 100, 600, 400)

        # Inisialisasi layout dan widget
        self.layout = QVBoxLayout()
        self.label = QLabel("Data Sensor akan ditampilkan di sini.")
        self.button = QPushButton("Ambil Data Sensor")
        self.button.clicked.connect(self.get_sensor_data)

        # Dropdown untuk memilih jenis koneksi
        self.connection_type_combo = QComboBox()
        self.connection_type_combo.addItems(["Serial", "Bluetooth", "WiFi"])
        self.layout.addWidget(self.connection_type_combo)

        # Input untuk port, IP address, dan port number
        self.port_label = QLabel("Port (misal: COM3 untuk Serial, atau alamat Bluetooth):")
        self.layout.addWidget(self.port_label)
        self.port_input = QLineEdit()
        self.layout.addWidget(self.port_input)

        self.ip_label = QLabel("IP Address (hanya untuk WiFi):")
        self.layout.addWidget(self.ip_label)
        self.ip_input = QLineEdit()
        self.layout.addWidget(self.ip_input)

        self.port_number_label = QLabel("Port Number (hanya untuk WiFi):")
        self.layout.addWidget(self.port_number_label)
        self.port_number_input = QLineEdit()
        self.layout.addWidget(self.port_number_input)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.button)

        # Set widget pusat
        central_widget = QWidget()
        central_widget.setLayout(self.layout)
        self.setCentralWidget(central_widget)

        # Inisialisasi OBDConnector
        self.obd_connector = None

    def connect_obd(self):
        connection_type = self.connection_type_combo.currentText().lower()
        port = self.port_input.text().strip()
        ip_address = self.ip_input.text().strip()
        port_number = self.port_number_input.text().strip()

        try:
            if connection_type == 'serial':
                if not port:
                    raise ValueError("Port harus diisi untuk koneksi Serial.")
                self.obd_connector = OBDConnector(connection_type='serial', port=port)
            elif connection_type == 'bluetooth':
                if not port:
                    raise ValueError("Alamat Bluetooth harus diisi untuk koneksi Bluetooth.")
                self.obd_connector = OBDConnector(connection_type='bluetooth', port=port)
            elif connection_type == 'wifi':
                if not ip_address or not port_number:
                    raise ValueError("IP Address dan Port Number harus diisi untuk koneksi WiFi.")
                self.obd_connector = OBDConnector(connection_type='wifi', ip_address=ip_address, port_number=int(port_number))
            else:
                raise ValueError("Jenis koneksi tidak dikenali.")
            
            QMessageBox.information(self, "Koneksi Berhasil", "OBD Connector terhubung.")
        except Exception as e:
            QMessageBox.critical(self, "Koneksi Gagal", str(e))

    def get_sensor_data(self):
        if self.obd_connector is None:
            self.connect_obd()  # Coba untuk menghubungkan jika belum terhubung

        if self.obd_connector:
            try:
                data = self.obd_connector.get_sensor_data()  # Pastikan fungsi ini ada di OBDConnector
                self.label.setText(str(data))
            except Exception as e:
                self.label.setText("Gagal mendapatkan data: " + str(e))
        else:
            self.label.setText("Koneksi OBD tidak tersedia.")

    def closeEvent(self, event):
        if self.obd_connector:
            self.obd_connector.close()  # Pastikan ada metode close di OBDConnector
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = ECUScannerApp()
    main_window.show()
    sys.exit(app.exec_())
