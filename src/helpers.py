# Tambahkan fungsi bantuan yang mungkin berguna untuk berbagai komponen proyek
def format_response(response):
    """Format a raw OBD-II response for display."""
    if response.startswith('41'):
        return response[4:].strip()
    return 'Data tidak tersedia'
