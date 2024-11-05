# ui/__init__.py

import logging

# Mengonfigurasi logging untuk paket ini
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Mengimpor kelas ECUScannerApp dari modul main_window
from .main_window import ECUScannerApp

# Menentukan apa yang akan diekspor saat menggunakan wildcard import
__all__ = ['ECUScannerApp']

# Mencetak informasi saat paket diinisialisasi
logger.info("Paket UI telah diinisialisasi")
