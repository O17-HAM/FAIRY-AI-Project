
# F.A.I.R.Y. AI Assistant 🧚‍♂️

F.A.I.R.Y. adalah asisten kecerdasan buatan berbasis web dengan antarmuka HUD (Heads-Up Display) bergaya *cyberpunk*. Sistem ini berjalan secara lokal (*localhost*) menggunakan Flask dan Python, memungkinkan AI untuk tidak hanya merespon pertanyaan melalui teks dan suara, tetapi juga mengendalikan sistem operasi Windows pengguna secara langsung.

## Fitur Utama
* **Kendali Sistem Lokal:** Mampu mengunci layar (Lock Screen), membuka Task Manager, File Explorer, Notepad, dan Kalkulator langsung dari antarmuka web.
* **Respon Suara Dinamis:** Menggunakan `edge-tts` untuk menghasilkan balasan suara yang natural tanpa membebani kuota API berbayar.
* **Integrasi Gemini AI:** Didukung oleh model `gemini-1.5-flash` untuk percakapan cerdas di luar perintah lokal.
* **HUD Interaktif:** Panel informasi jam dan cuaca *real-time* (menggunakan wttr.in), serta panel pintasan perintah cerdas.
* **Pencarian Dinamis:** Perintah cepat untuk mencari informasi di Google atau memutar video di YouTube.

## Prasyarat Sistem
* OS: Windows 10 / 11 (untuk dukungan penuh eksekusi perintah sistem)
* Python 3.8 atau lebih baru
* API Key dari Google AI Studio (Gemini API)

## Langkah Instalasi & Konfigurasi

1. **Persiapkan Folder**
   Ekstrak file `.zip` ini atau *clone* repositori ke dalam komputer Anda.
   
2. **Instalasi Pustaka (Library)**
   Buka Terminal atau Command Prompt di dalam folder proyek ini, lalu jalankan perintah berikut:
   ```bash
   pip install -r requirements.txt

```

3. **Konfigurasi API Key**
* Cari file bernama `.env.example` di dalam folder utama.
* Ubah nama (rename) file tersebut menjadi `.env` saja.
* Buka file `.env` menggunakan teks editor (seperti Notepad), lalu tempelkan API Key Gemini Anda:
```env
GEMINI_API_KEY=masukkan_api_key_anda_disini

```





## Cara Menjalankan Aplikasi

1. Buka Terminal di dalam folder proyek.
2. Jalankan server lokal dengan perintah:
```bash
python app.py

```


3. Buka web browser (disarankan Google Chrome) dan akses alamat berikut:
**http://127.0.0.1:5000**

## Daftar Perintah Inti

Ketik perintah berikut di kolom obrolan atau klik dari panel sebelah kanan:

* `status sistem` : Mengecek status mesin AI.
* `jam berapa` : Melihat waktu saat ini.
* `cari [topik]` : Melakukan pencarian Google otomatis.
* `putar [video]` : Membuka pencarian YouTube otomatis.
* `buka [nama_web]` : Membuka situs produktivitas (contoh: buka youtube, buka github, buka discord, buka vscode).
* `kunci layar` : **(PERHATIAN)** Mengunci layar PC/Laptop secara instan (Lock Screen).
