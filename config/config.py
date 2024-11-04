# config.py

# Konfigurasi untuk OBDConnector
OBD_CONFIG = {
    'connection_type': 'serial',  # Jenis koneksi: 'serial', 'bluetooth', atau 'wifi'
    'port': 'COM3',                # Port untuk koneksi serial (misal: 'COM3' untuk Windows, '/dev/ttyUSB0' untuk Linux)
    'baudrate': 9600,              # Baudrate untuk koneksi serial
    'ip_address': None,            # Alamat IP untuk koneksi WiFi (jika menggunakan WiFi)
    'port_number': None,           # Nomor port untuk koneksi WiFi (jika menggunakan WiFi)
}

# Jika menggunakan Bluetooth, Anda dapat mengubah port ke alamat Bluetooth
# OBD_CONFIG['connection_type'] = 'bluetooth'
# OBD_CONFIG['port'] = '00:11:22:33:44:55'  # Alamat Bluetooth perangkat OBD-II

# Jika menggunakan WiFi, Anda dapat mengatur alamat IP dan nomor port
# OBD_CONFIG['connection_type'] = 'wifi'
# OBD_CONFIG['ip_address'] = '192.168.1.100'
# OBD_CONFIG['port_number'] = 35000