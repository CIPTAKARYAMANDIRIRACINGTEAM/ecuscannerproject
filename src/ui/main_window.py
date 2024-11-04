from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QComboBox, QFrame, QMessageBox
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect
import threading
from src.obd_connector import OBDConnector
from config.config import load_config

class ECUScannerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.config = load_config()
        self.initUI()
        self.connector = None

    def initUI(self):
        self.setWindowTitle('SMART X - ECU Scanner')
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: #f0f4f8;")

        title = QLabel("SMART X - ECU Scanner", self)
        title.setFont(QFont('Arial', 24, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #2c3e50; margin-bottom: 20px;")

        self.connection_type = QComboBox(self)
        self.connection_type.addItems(['Serial', 'Bluetooth', 'WiFi'])
        self.connection_type.currentTextChanged.connect(self.updateConnection)
        self.connection_type.setStyleSheet("""
            QComboBox {
                padding: 5px;
                border-radius: 5px;
                border: 1px solid #2c3e50;
            }
        """)

        self.sensor_frame = QFrame(self)
        self.sensor_frame.setStyleSheet("""
            QFrame {
                border: 1px solid #bdc3c7;
                border-radius: 10px;
                padding: 10px;
                background-color: #ffffff;
            }
        """)

        sensor_layout = QVBoxLayout()
        self.sensor_labels = {
            'RPM': QLabel('RPM: -'),
            'Suhu Mesin': QLabel('Suhu Mesin: -'),
            'Kecepatan': QLabel('Kecepatan: -'),
        }
        for label in self.sensor_labels.values():
            label.setFont(QFont('Arial', 14))
            label.setStyleSheet("color: #34495e;")
            sensor_layout.addWidget(label)

        self.sensor_frame.setLayout(sensor_layout)

        self.scan_button = QPushButton('Scan Data', self)
        self.scan_button.setFont(QFont('Arial', 16))
        self.scan_button.setIcon(QIcon('assets/scan_icon.png'))
        self.scan_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        self.scan_button.clicked.connect(self.scanData)

        main_layout = QVBoxLayout()
        main_layout.addWidget(title)
        main_layout.addWidget(self.connection_type)
        main_layout.addWidget(self.sensor_frame)
        main_layout.addWidget(self.scan_button)
        main_layout.setAlignment(Qt.AlignTop)
        main_layout.setSpacing(15)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        self.anim = QPropertyAnimation(self.sensor_frame, b"geometry")
        self.anim.setDuration(1000)
        self.anim.setStartValue(QRect(150, 150, 500, 0))
        self.anim.setEndValue(QRect(150, 150, 500, 200))
        self.anim.setEasingCurve(Qt.EaseInOutQuad)

    def updateConnection(self, text):
        if not self.config:
            QMessageBox.critical(self, "Error", "Konfigurasi tidak tersedia.")
            return

        try:
            conn_config = self.config['obd_connection']
            if text == 'Serial':
                self.connector = OBDConnector(
                    connection_type='serial',
                    port=conn_config.get('port', 'COM3'),
                    baudrate=conn_config.get('baud_rate', 9600)
                )
            elif text == 'Bluetooth':
                self.connector = OBDConnector(
                    connection_type='bluetooth',
                    port=conn_config.get('port', 'XX:XX:XX:XX:XX:XX')
                )
            elif text == 'WiFi':
                self.connector = OBDConnector(
                    connection_type='wifi',
                    ip_address=conn_config.get('ip_address', '192.168.0.10'),
                    port_number=conn_config.get('port_number', 35000)
                )

            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("Koneksi Berhasil")
            msg.setText("Alat telah berhasil terhubung dengan aplikasi.")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()

        except Exception as e:
            error_msg = QMessageBox()
            error_msg.setIcon(QMessageBox.Critical)
            error_msg.setWindowTitle("Koneksi Gagal")
            error_msg.setText(f"Terjadi kesalahan saat menghubungkan: {str(e)}")
            error_msg.setStandardButtons(QMessageBox.Ok)
            error_msg.exec_()

    def scanData(self):
        if self.connector:
            self.scan_button.setText('Scanning...')
            self.anim.start()
            threading.Thread(target=self.updateSensorData).start()
        else:
            for label in self.sensor_labels.values():
                label.setText('Pilih tipe koneksi terlebih dahulu.')

    def updateSensorData(self):
        try:
            data = self.connector.get_sensor_data()
            for sensor, value in data.items():
                self.sensor_labels[sensor].setText(f'{sensor}: {value}')
        except Exception as e:
            for label in self.sensor_labels.values():
                label.setText('Gagal mendapatkan data.')
            print(f"Error: {str(e)}")
        finally:
            self.scan_button.setText('Scan Data')

    def closeEvent(self, event):
        if self.connector:
            self.connector.close()
        event.accept()
