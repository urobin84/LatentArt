# LatentArt - Image Generation Submission

Selamat datang di proyek **LatentArt**! Proyek ini merupakan implementasi model Text-to-Image dan Inpainting menggunakan `diffusers` (Stable Diffusion) dan interface interaktif menggunakan `Streamlit`. Modul ini disiapkan untuk mencapai target level **ADVANCED**.

## 🌟 Fitur Utama

- **Text-To-Image (T2I) Generation**: Implementasi dasar dan lanjutan generasi gambar dengan paramater kustom menggunakan model `runwayml/stable-diffusion-v1-5`.
- **Eksperimentasi Parameter**: Melakukan uji coba pada `guidance_scale` dan `num_inference_steps` untuk melihat pengaruhnya pada hasil.
- **Two-Stage Generation (Refiner)**: Pipa bertingkat menggunakan Text-to-Image lalu disempurnakan (refined) dengan modul Image-to-Image (Denoising strength 0.8) untuk kualitas gambar resolusi tinggi.
- **Inpainting & Outpainting**: Manipulasi area tertentu dari sebuah gambar dan Zoom-Out dengan perkuatan `runwayml/stable-diffusion-inpainting`. Termasuk masker manual serta otomatis.
- **Interface Streamlit**: Antarmuka interaktif yang mudah digunakan untuk eksplorasi Text-to-Image, Inpainting, dan Outpainting secara real-time.
- **Device-Agnostic Execution**: Dirancang untuk dapat berjalan optimal baik di CPU lokal, Apple Silicon (MPS), maupun Google Colab (CUDA) menggunakan komputasi yang efisien.

## 🎥 Demonstrasi Aplikasi

Lihat cuplikan interaktif dari aplikasi Streamlit yang telah berjalan pada video di bawah ini:

<video width="100%" controls>
  <source src="video_demo_aplikasi_BFGAI.mp4" type="video/mp4">
  Browser Anda tidak mendukung tag video. Silakan buka file <code>video_demo_aplikasi_BFGAI.mp4</code> secara manual.
</video>

## 📂 Struktur Proyek

```text
LatentArt/
│
├── LatentArt_Pipeline_submission_BFGAI_Muhammad_Muqorrobin.ipynb     # Notebook Pipeline Eksperimen utama
├── LatentArt_Streamlit_submission_BFGAI_Muhammad_Muqorrobin.ipynb    # Notebook Streamlit App beserta pembuatan logic.py & app.py
├── video_demo_aplikasi_BFGAI.mp4                                     # Video demonstrasi aplikasi
├── requirements.txt                                                  # Daftar dependensi yang dibutuhkan
├── Makefile                                                          # Perintah otomatisasi (run, build, zip)
└── README.md                                                         # Dokumentasi Repositori
```

## 🚀 Cara Menjalankan

Proyek ini telah dilengkapi dengan `Makefile` untuk mempermudah eksekusi:

### 1. Membuka Jupyter Notebook
Untuk menjalankan dan mengedit notebook secara interaktif, gunakan perintah berikut:
```bash
make jupyter
```

### 2. Menjalankan Pipeline Notebook (Otomatis)
Untuk menjalankan keseluruhan notebook Pipeline dari awal hingga akhir tanpa membuka antarmuka Jupyter:
```bash
make pipeline
```

### 3. Menjalankan Aplikasi Streamlit
Perintah ini akan secara otomatis menjalankan proses persiapan (headless run) pada notebook Streamlit yang akan meng-generate *source code* Streamlit ke direktori lokal (seperti `logic.py` dan `app.py`), lalu langsung meluncurkan web server Streamlit:
```bash
make streamlit
```

### 4. Membuat File Submission (Zip)
Untuk membungkus file yang dibutuhkan (`notebooks`, `requirements.txt`, `video`) ke dalam satu arsip zip sesuai format target pengumpulan:
```bash
make zip
```

### 5. Membersihkan File Output
Untuk menghapus file arsip `.zip` dan file cache otomatis lainnya:
```bash
make clean
```

## 🧠 Model dan Syarat Teknis

Proyek ini dipersiapkan dengan parameter spesifik:
- **T2I Model**: `runwayml/stable-diffusion-v1-5` (Wajib Seed: 222)
- **Inpaint Model**: `runwayml/stable-diffusion-inpainting` (Wajib Seed: 9)
- **Negative Prompt default**: *"photorealistic, realistic, photograph, 3d render, messy, blurry, low quality, bad art, ugly, sketch, grainy, unfinished, chromatic aberration"*

---
**Dikembangkan oleh Muhammad Muqorrobin untuk Image Generation Submission.**
