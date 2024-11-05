import yaml

def load_config():
    try:
        with open('config/config.yaml', 'r') as file:
            config = yaml.safe_load(file)
        return config
    except FileNotFoundError:
        print("File konfigurasi 'config.yaml' tidak ditemukan.")
        return None
    except yaml.YAMLError as e:
        print(f"Kesalahan saat membaca file konfigurasi: {e}")
        return None
