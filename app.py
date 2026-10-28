from flask import Flask, render_template, request, jsonify
import webbrowser
import os
import time
import asyncio
import edge_tts
import urllib.parse
from datetime import datetime
from dotenv import load_dotenv
from google import genai
import threading
from flask import Flask, render_template, request, jsonify
import webbrowser


# Memuat file rahasia .env
load_dotenv()
app = Flask(__name__)

# Konfigurasi Gemini
API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY)
AI_NAME = "Fairy"

if not os.path.exists('static'):
    os.makedirs('static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/buat_suara', methods=['POST'])
def buat_suara():
    teks = request.json.get('teks', '')
    if not teks:
        return jsonify({"audio_url": ""})
    
    nama_file = "static/suara_ai.mp3"
    jenis_suara = "id-ID-GadisNeural"
    
    async def proses_tts():
        komunikasi = edge_tts.Communicate(teks, jenis_suara)
        await komunikasi.save(nama_file)
        
    asyncio.run(proses_tts())
    return jsonify({"audio_url": f"/{nama_file}?t={int(time.time())}"})

@app.route('/kirim_pesan', methods=['POST'])
def kirim_pesan():
    data = request.get_json()
    pesan = data.get('pesan', '').lower().strip()
    balasan = ""
    
    # -----------------------------------------------------------
    # 1. PERINTAH LOKAL (Tanpa API Gemini / Anti Limit)
    # -----------------------------------------------------------
    
    # Waktu dan Tanggal
    if "jam berapa" in pesan or "waktu" in pesan:
        sekarang = datetime.now()
        balasan = f"Saat ini pukul {sekarang.strftime('%H:%M')} WIB, boss."
    elif "tanggal" in pesan or "hari ini" in pesan:
        sekarang = datetime.now()
        balasan = f"Hari ini adalah tanggal {sekarang.strftime('%d %B %Y')}."

    # Status & Identitas
    elif "status sistem" in pesan or "status" in pesan:
        balasan = "Semua modul inti online. Suhu CPU stabil, memori optimal, dan jaringan terhubung."
    elif "siapa kamu" in pesan or "kamu siapa" in pesan or "identitas" in pesan:
        balasan = f"Saya adalah {AI_NAME}, sistem asisten kecerdasan buatan yang dirancang untuk membantu Anda."

    # Perintah Sistem Windows (Termasuk Kunci Layar)
    elif "buka kalkulator" in pesan:
        os.system("calc")
        balasan = "Membuka kalkulator."
    elif "buka notepad" in pesan:
        os.system("notepad")
        balasan = "Membuka Notepad."
    elif "buka explorer" in pesan:
        os.system("explorer")
        balasan = "Membuka File Explorer."
    elif "buka vscode" in pesan or "buka code" in pesan:
        os.system("code")
        balasan = "Menjalankan Visual Studio Code."
    elif "buka task manager" in pesan:
        os.system("taskmgr")
        balasan = "Membuka Task Manager untuk memantau performa."
    elif "kunci layar" in pesan or "lock screen" in pesan:
        # Membuat fungsi kecil untuk menunda penguncian selama 4 detik
        def eksekusi_kunci():
            time.sleep(4) # Waktu tunggu (sesuaikan jika suaranya kurang panjang)
            os.system("rundll32.exe user32.dll,LockWorkStation")
            
        # Jalankan fungsi hitung mundur di latar belakang (tanpa menghentikan program)
        threading.Thread(target=eksekusi_kunci).start()
        
        balasan = "Protokol keamanan diaktifkan. Mengunci layar sekarang."

    # Pintasan Web Dasar
    elif "buka youtube" in pesan:
        webbrowser.open("https://www.youtube.com")
        balasan = "Membuka YouTube sekarang."
    elif "buka chrome" in pesan or "buka google" in pesan:
        webbrowser.open("https://www.google.com")
        balasan = "Google Chrome segera dibuka."
    elif "buka discord" in pesan:
        webbrowser.open("https://discord.com/app")
        balasan = "Membuka Discord sekarang."
    elif "buka github" in pesan:
        webbrowser.open("https://github.com")
        balasan = "Membuka halaman GitHub."
    elif "buka whatsapp" in pesan or "buka wa" in pesan:
        webbrowser.open("https://web.whatsapp.com")
        balasan = "Membuka WhatsApp Web."
    elif "buka spotify" in pesan:
        webbrowser.open("https://open.spotify.com")
        balasan = "Membuka Spotify."
    elif "cuaca" in pesan:
        webbrowser.open("https://www.google.com/search?q=cuaca+hari+ini")
        balasan = "Menampilkan data cuaca terbaru di layar Anda."

    # Pintasan Web Baru
    elif "buka translate" in pesan or "terjemahkan" in pesan:
        webbrowser.open("https://translate.google.com")
        balasan = "Membuka Google Translate."
    elif "buka maps" in pesan or "buka peta" in pesan:
        webbrowser.open("https://maps.google.com")
        balasan = "Membuka Google Maps."
    elif "buka email" in pesan or "buka gmail" in pesan:
        webbrowser.open("https://mail.google.com")
        balasan = "Membuka kotak masuk Gmail."

    # Pencarian Dinamis
    elif pesan.startswith("cari ") or pesan.startswith("mencari "):
        query = pesan.replace("cari ", "").replace("mencari ", "").strip()
        query_encoded = urllib.parse.quote(query)
        webbrowser.open(f"https://www.google.com/search?q={query_encoded}")
        balasan = f"Mencari informasi tentang {query} di Google."
    elif pesan.startswith("putar ") or pesan.startswith("play ") or pesan.startswith("memutar "):
        query = pesan.replace("putar ", "").replace("play ", "").replace("memutar ", "").strip()
        query_encoded = urllib.parse.quote(query)
        webbrowser.open(f"https://www.youtube.com/results?search_query={query_encoded}")
        balasan = f"Mencari {query} di YouTube."

    # -----------------------------------------------------------
    # 2. RESPON GEMINI AI (Hanya jika tidak ada di perintah atas)
    # -----------------------------------------------------------
    else:
        try:
            prompt = f"Berperanlah sebagai AI cerdas, dingin, dan efisien bernama {AI_NAME}. Jawablah maksimal 2 kalimat saja: {pesan}"
            response = client.models.generate_content(
                model='gemini-3.8-flash', 
                contents=prompt
            )
            balasan = response.text
        except Exception as e:
            print(f"\n[ERROR API GEMINI]: {e}\n")
            balasan = "Sistem AI sedang sibuk atau batas kuota tercapai. Silakan gunakan perintah manual."
            
    return jsonify({"balasan": balasan})

if __name__ == '__main__':
    app.run(debug=True)