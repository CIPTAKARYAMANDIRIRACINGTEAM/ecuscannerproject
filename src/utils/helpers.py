import json

def format_data(data):
    return {k: v for k, v in data.items() if v is not None}

def save_top_speed(data):
    with open('top_speed_log.json', 'a') as f:
        f.write(json.dumps(data) + '\n')

def read_codes():
    return ["P0300", "P0420"]  # Simulasi pembacaan kode kesalahan

def delete_codes():
    return True  # Simulasi penghapusan kode kesalahan
