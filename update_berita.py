import os
import json
import re
from datetime import datetime

# Konfigurasi Folder
CONTENT_DIR = 'content/berita'
OUTPUT_FILE = 'berita.json'

def parse_markdown(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Ambil Judul dari baris pertama yang mengandung ** atau #
    title_match = re.search(r'\*\*(.*?)\*\*', content)
    if not title_match:
        title_match = re.search(r'# (.*)', content)
    title = title_match.group(1) if title_match else "Tanpa Judul"

    # Ambil Ringkasan (Hapus karakter aneh, ambil 150 huruf pertama)
    clean_text = re.sub(r'[#*]', '', content)
    lines = [l.strip() for l in clean_text.split('\n') if l.strip()]
    summary = lines[1] if len(lines) > 1 else (lines[0] if lines else "")
    if len(summary) > 150: summary = summary[:150] + "..."
            
    return title, summary

def generate_json():
    berita_list = []
    
    if not os.path.exists(CONTENT_DIR):
        print("Folder content/berita tidak ditemukan.")
        return

    files = [f for f in os.listdir(CONTENT_DIR) if f.endswith('.md')]
    
    # Urutkan berdasarkan waktu upload/modifikasi terakhir
    files.sort(key=lambda x: os.path.getmtime(os.path.join(CONTENT_DIR, x)), reverse=True)

    for filename in files:
        file_path = os.path.join(CONTENT_DIR, filename)
        
        # Ambil tanggal dari metadata file
        stats = os.stat(file_path)
        mod_time = datetime.fromtimestamp(stats.st_mtime)
        months = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
        date_str = f"{mod_time.day} {months[mod_time.month-1]} {mod_time.year}"
        
        title, summary = parse_markdown(file_path)
        news_id = filename.replace('.md', '')

        berita_item = {
            "id": news_id,
            "judul": title,
            "tanggal": date_str,
            "ringkasan": summary,
            "file": f"{CONTENT_DIR}/{filename}"
        }
        berita_list.append(berita_item)

    # Tulis ulang berita.json
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(berita_list, f, indent=4, ensure_ascii=False)
    print("Berita.json berhasil diupdate otomatis.")

if __name__ == "__main__":
    generate_json()