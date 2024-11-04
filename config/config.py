import yaml

def load_config(file_path='config/config.yaml'):
    try:
        with open(file_path, 'r') as config_file:
            config = yaml.safe_load(config_file)
            return config
    except FileNotFoundError:
        print(f"File konfigurasi tidak ditemukan di: {file_path}")
        return None
    except yaml.YAMLError:
        print("Gagal membaca file konfigurasi YAML.")
        return None
