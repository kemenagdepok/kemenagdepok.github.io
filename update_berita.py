import os
import json
import re
from datetime import datetime

# Konfigurasi Folder
CONTENT_DIR = 'content/berita'
OUTPUT_FILE = 'berita.json'

def parse_markdown(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    title = "Tanpa Judul"
    summary = ""
    
    clean_lines = []
    for line in lines:
        line = line.strip()
        # Abaikan baris kosong dan kode gambar
        if not line: continue 
        if line.startswith('!['): continue
        if line.startswith('<img'): continue
        clean_lines.append(line)
        
    if clean_lines:
        # 1. Ambil Baris Pertama sebagai JUDUL (Bersihkan markdown bold/header)
        raw_title = clean_lines[0]
        # Hapus tanda # atau ** pada judul
        title = re.sub(r'^[#\s]+', '', raw_title)
        title = title.replace('**', '').replace('__', '')
        
        # 2. Ambil Ringkasan dari sisa baris
        if len(clean_lines) > 1:
            # Gabungkan sisa baris jadi satu paragraf
            full_text = " ".join(clean_lines[1:])
            
            # Hapus dateline jika ada (Contoh: "Depok (Kemenag) - ")
            # Regex ini menghapus teks tebal di awal kalimat yang diikuti tanda hubung
            full_text = re.sub(r'^\*\*.*?\*\*\s*[-–]\s*', '', full_text)
            
            # Bersihkan sisa markdown
            full_text = full_text.replace('**', '').replace('#', '')
            
            # Potong 160 karakter
            summary = full_text[:160] + "..."
            
    return title, summary

def generate_json():
    berita_list = []
    
    if not os.path.exists(CONTENT_DIR):
        print("Folder content/berita tidak ditemukan.")
        return

    files = [f for f in os.listdir(CONTENT_DIR) if f.endswith('.md')]
    
    # Urutkan file (File terbaru diproses duluan)
    files.sort(key=lambda x: os.path.getmtime(os.path.join(CONTENT_DIR, x)), reverse=True)

    for filename in files:
        file_path = os.path.join(CONTENT_DIR, filename)
        
        # Ambil tanggal modifikasi file sebagai tanggal berita
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

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(berita_list, f, indent=4, ensure_ascii=False)
    print("Berita.json berhasil diupdate.")

if __name__ == "__main__":
    generate_json()