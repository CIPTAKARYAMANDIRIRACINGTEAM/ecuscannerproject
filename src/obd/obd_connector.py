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

    def detect_protocol(self):
        print("Mendeteksi protokol ECU...")
        for protocol in self.protocols:
            if self.test_protocol(protocol):
                self.current_protocol = protocol
                print(f"Protokol terdeteksi: {protocol}")
                return
        raise ConnectionError("Tidak ada protokol yang cocok.")

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
        }
        data = {}
        for sensor, command in sensors.items():
            response = self.send_command(command)
            if response.startswith('41'):
                value = response[4:].strip()
                data[sensor] = value
            else:
                data[sensor] = 'Data tidak tersedia'
        return data
