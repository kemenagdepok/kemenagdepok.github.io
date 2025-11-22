import os
import json
import re
from datetime import datetime

# --- KONFIGURASI FOLDER ---
CONTENT_DIR = 'content/berita'
OUTPUT_FILE = 'berita.json'
# URL Logo Default (Fallback jika tidak ada gambar)
DEFAULT_THUMBNAIL = "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9a/Kementerian_Agama_new_logo.png/150px-Kementerian_Agama_new_logo.png"

def parse_markdown_content(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    title = "Tanpa Judul"
    summary = ""
    thumbnail_url = "" # Default kosong
    
    # --- 1. CARI GAMBAR PERTAMA (Thumbnail) ---
    # Kita cari di semua baris mentah sebelum dibersihkan
    for line in lines:
        # Regex untuk mencari sintaks gambar markdown: ![alt](url)
        # Menangkap grup (.*?) yang ada di dalam kurung biasa
        img_match = re.search(r'!\[.*?\]\((.*?)\)', line)
        if img_match:
            # Ambil URL gambar yang ditemukan
            thumbnail_url = img_match.group(1)
            # Cukup gambar pertama saja, berhenti mencari.
            break

    # --- 2. BERSIHKAN KONTEN UNTUK JUDUL & RINGKASAN ---
    clean_lines = []
    for line in lines:
        line = line.strip()
        # Abaikan baris kosong, dan abaikan baris yang isinya cuma gambar
        if not line: continue 
        if line.startswith('!['): continue
        if line.startswith('<img'): continue
        clean_lines.append(line)
        
    if clean_lines:
        # Ambil Baris Pertama sebagai JUDUL
        raw_title = clean_lines[0]
        # Bersihkan tanda markdown bold/header (# atau **) dari judul
        title = re.sub(r'^[#\s]+', '', raw_title)
        title = title.replace('**', '').replace('__', '')
        
        # Ambil Ringkasan dari sisa baris
        if len(clean_lines) > 1:
            full_text = " ".join(clean_lines[1:])
            # Hapus dateline (contoh: "**Depok (Kemenag)** -")
            full_text = re.sub(r'^\*\*.*?\*\*\s*[-–]\s*', '', full_text)
            # Bersihkan sisa markdown agar ringkasan rapi
            full_text = full_text.replace('**', '').replace('#', '').replace('`', '')
            # Potong 160 karakter untuk ringkasan
            summary = full_text[:160] + "..."
            
    return title, summary, thumbnail_url

def generate_json():
    berita_list = []
    
    if not os.path.exists(CONTENT_DIR):
        print(f"Folder {CONTENT_DIR} tidak ditemukan.")
        return

    files = [f for f in os.listdir(CONTENT_DIR) if f.endswith('.md')]
    # Urutkan berdasarkan waktu modifikasi terakhir (Terbaru di atas)
    files.sort(key=lambda x: os.path.getmtime(os.path.join(CONTENT_DIR, x)), reverse=True)

    print(f"Memproses {len(files)} file berita...")

    for filename in files:
        file_path = os.path.join(CONTENT_DIR, filename)
        
        # Ambil tanggal
        stats = os.stat(file_path)
        mod_time = datetime.fromtimestamp(stats.st_mtime)
        months = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
        date_str = f"{mod_time.day} {months[mod_time.month-1]} {mod_time.year}"
        
        # Parse konten
        title, summary, thumbnail = parse_markdown_content(file_path)
        news_id = filename.replace('.md', '')

        berita_item = {
            "id": news_id,
            "judul": title,
            "tanggal": date_str,
            "ringkasan": summary,
            "thumbnail": thumbnail, # Field baru di JSON
            "file": f"{CONTENT_DIR}/{filename}"
        }
        berita_list.append(berita_item)
        print(f"OK: {filename} (Thumb: {'Yes' if thumbnail else 'No'})")

    # Tulis ke JSON
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(berita_list, f, indent=4, ensure_ascii=False)
    print(f"\nSUKSES! {OUTPUT_FILE} berhasil diupdate.")

if __name__ == "__main__":
    generate_json()
