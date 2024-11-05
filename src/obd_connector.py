import serial
import bluetooth
import socket
import time

class OBDConnector:
    def __init__(self, connection_type='serial', port='COM3', baudrate=9600, ip_address=None, port_number=None):
        self.connection_type = connection_type
        self.ser = None
        self.sock = None
        self.bt_sock = None

        self.protocols = ['ISO 9141-2', 'ISO 14230-4', 'ISO 15765-4', 'J1850 PWM', 'J1850 VPW']
        self.current_protocol = None

        try:
            if connection_type == 'serial':
                self.ser = serial.Serial(port=port, baudrate=baudrate, timeout=1)
            elif connection_type == 'bluetooth':
                self.bt_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
                self.bt_sock.connect((port, 1))
            elif connection_type == 'wifi':
                if ip_address and port_number:
                    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self.sock.connect((ip_address, port_number))
                else:
                    raise ValueError("IP address dan port harus disediakan untuk koneksi WiFi.")
            
            self.detect_protocol()
        except (serial.SerialException, bluetooth.BluetoothError, socket.error, ValueError) as e:
            print(f"Kesalahan saat menginisialisasi koneksi: {e}")
            raise ConnectionError(f"Gagal menghubungkan menggunakan {connection_type}: {e}")

    def detect_protocol(self):
        print("Mendeteksi protokol ECU...")
        for protocol in self.protocols:
            if self.test_protocol(protocol):
                self.current_protocol = protocol
                print(f"Protokol terdeteksi: {protocol}")
                return
        raise ConnectionError("Tidak ada protokol yang cocok ditemukan.")

    def test_protocol(self, protocol):
        try:
            self.send_command('ATZ')  # Reset ECU
            time.sleep(1)
            response = self.send_command('ATDP')  # Tanyakan protokol
            return bool(response)
        except Exception as e:
            print(f"Protokol {protocol} gagal: {e}")
            return False

    def send_command(self, command):
        try:
            if self.connection_type == 'serial':
                self.ser.write((command + '\r').encode())
                response = self.ser.read(128).decode().strip()
            elif self.connection_type == 'bluetooth':
                self.bt_sock.send((command + '\r').encode())
                response = self.bt_sock.recv(128).decode().strip()
            elif self.connection_type == 'wifi':
                self.sock.sendall((command + '\r').encode())
                response = self.sock.recv(128).decode().strip()
            else:
                raise ValueError("Jenis koneksi tidak valid")
            
            return response if response else 'Data tidak tersedia'
        except (serial.SerialException, bluetooth.BluetoothError, socket.error) as e:
            print(f"Kesalahan saat mengirim perintah '{command}': {e}")
            return 'Gagal mengirim perintah'

    def close(self):
        try:
            if self.connection_type == 'serial' and self.ser.is_open:
                self.ser.close()
                print("Koneksi serial ditutup.")
            elif self.connection_type == 'bluetooth' and self.bt_sock:
                self.bt_sock.close()
                print("Koneksi Bluetooth ditutup.")
            elif self.connection_type == 'wifi' and self.sock:
                self.sock.close()
                print("Koneksi WiFi ditutup.")
        except Exception as e:
            print(f"Kesalahan saat menutup koneksi: {e}")

    def get_sensor_data(self):
        sensors = {
            'RPM': '010C',
            'Suhu Mesin': '0105',
            'Kecepatan': '010D',
        }
        data = {}
        for sensor, command in sensors.items():
            response = self.send_command(command)
            if response.startswith('41'):
                value = response[4:].strip()  # Ini hanya contoh; dekoding tambahan mungkin diperlukan
                data[sensor] = value
            else:
                data[sensor] = 'Data tidak tersedia'
        return data
