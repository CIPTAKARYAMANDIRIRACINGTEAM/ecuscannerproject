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

        # Inisialisasi koneksi sesuai dengan jenis yang dipilih
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
                raise ValueError("IP address dan port number harus disediakan untuk koneksi WiFi.")
        
        self.detect_protocol()

    def detect_protocol(self):
        print("Mendeteksi protokol ECU...")
        for protocol in self.protocols:
            if self.test_protocol(protocol):
                self.current_protocol = protocol
                print(f"Protokol terdeteksi: {protocol}")
                return
        print("Tidak ada protokol yang cocok. Pastikan ECU mendukung OBD-II.")
        raise ConnectionError("Protokol tidak terdeteksi.")

    def test_protocol(self, protocol):
        try:
            # Mengirim perintah untuk menguji protokol
            self.send_command('ATZ')  # Reset OBD-II
            time.sleep(1)
            response = self.send_command('ATDP')  # Tanyakan protokol
            return bool(response)
        except Exception as e:
            print(f"Protokol {protocol} gagal: {e}")
            return False

    def send_command(self, command):
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
            return "Koneksi tidak valid"

        return response if response else 'Data tidak tersedia'

    def close(self):
        if self.connection_type == 'serial' and self.ser.is_open:
            self.ser.close()
        elif self.connection_type == 'bluetooth':
            self.bt_sock.close()
        elif self.connection_type == 'wifi':
            self.sock.close()

    def get_sensor_data(self):
        sensors = {
            'RPM': '010C',
            'Suhu Mesin': '0105',
            'Kecepatan': '010D',
            'TPS': '010F',
            'MAP': '010B',
            'Load': '0104',
            'Coolant Temp': '0105',
            'Fuel Status': '012F',
            'Short Term Trim': '0130',
            'Long Term Trim': '0131',
            'Intake Pressure': '010B',
            'Ignition Timing': '010E',
            'Air Temp': '010F',
            'Air Flow': '0110',
            'O2 Voltage': '0130',
            'Fuel Pressure': '0131',
        }
        data = {}
        for sensor, command in sensors.items():
            response = self.send_command(command)
            # Parsing response (sesuaikan ini berdasarkan format respons yang sebenarnya)
            if response.startswith('41'):
                # Mengambil nilai dari respons OBD-II
                value = response[4:].strip()
                data[sensor] = value
            else:
                data[sensor] = 'Data tidak tersedia'
        return data