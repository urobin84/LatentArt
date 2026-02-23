# LatentArt - Image Generation Submission

Selamat datang di proyek **LatentArt**! Proyek ini merupakan implementasi model Text-to-Image dan Inpainting menggunakan `diffusers` (Stable Diffusion) dan interface interaktif menggunakan `Streamlit`. Modul ini disiapkan untuk mencapai target level **ADVANCED**.

## 🌟 Fitur Utama

- **Text-To-Image (T2I) Generation**: Implementasi dasar dan lanjutan generasi gambar dengan paramater kustom menggunakan model `runwayml/stable-diffusion-v1-5`.
- **Eksperimentasi Parameter**: Melakukan uji coba pada `guidance_scale` dan `num_inference_steps` untuk melihat pengaruhnya pada hasil.
- **Two-Stage Generation (Refiner)**: Pipa bertingkat menggunakan Text-to-Image lalu disempurnakan (refined) dengan modul Image-to-Image (Denoising strength 0.8) untuk kualitas gambar resolusi tinggi.
- **Inpainting & Outpainting**: Manipulasi area tertentu dari sebuah gambar dan Zoom-Out dengan perkuatan `runwayml/stable-diffusion-inpainting`. Termasuk masker manual serta otomatis.
- **Device-Agnostic Execution**: Dirancang untuk dapat berjalan optimal baik di CPU lokal, Apple Silicon (MPS), maupun Google Colab (CUDA) menggunakan `torch.float16`.

## 📂 Struktur Repositori

```text
LatentArt/
│
├── .github/          # (Optional) GitHub Actions workflow
├── assets/           # Material yang dibutuhkan seperti template gambar (Inpainting)
├── notebooks/
│   └── LatentArt_Submission.ipynb  # Notebook Eksperimen (Colab-ready)
├── outputs/          # Hasil luaran generator image disimpan di sini (diabaikan oleh git)
├── src/
│   ├── __init__.py
│   ├── engine.py     # Setup pipeline, scheduler logic (Euler A, DPM++, DDIM)
│   └── utils.py      # Device & memory handler (CUDA, MPS, CPU)
├── Makefile          # Utility script untuk setup environment dan run
├── README.md         # Dokumentasi Repositori
└── requirements.txt  # Project dependencies list
```

## 🚀 Cara Menjalankan

### Opsi A: Google Colab (Maksimal Performa)

Kami **sangat merekomendasikan** menggunakan Google Colab (dengan T4 GPU / memori 15GB).

1. Upload seluruh folder `LatentArt` ini ke Google Drive Anda (misal ke `MyDrive/LatentArt`).
2. Buka `notebooks/LatentArt_Submission.ipynb` menggunakan Google Colab.
3. Ubah *runtime type* menjadi **GPU (T4 / T4 High-RAM)**.
4. Jalankan Cell Inisialisasi Colab (yang berada di paling atas) untuk otomatis memasang modul requirements (`pip install`) dan me-mount Google Drive.
5. Eksekusi dari cell awal ke akhir.

### Opsi B: Komputer Lokal (Python / Streamlit Interface)

Jika Anda memiliki sistem yang memadai seperti GPU berbasis CUDA atau Apple Silicon (M1/M2), bisa menjalankannya di VSCode/Terminal.

1. **Setup Lingkungan** (membuat `.venv` dan install `requirements.txt`):
   ```bash
   make setup
   ```
2. **Aktifkan Environment**:
   *   Mac/Linux: `source .venv/bin/activate`
   *   Windows: `.\\.venv\\Scripts\\activate`
3. **Mulai UI Generator Gambar (Streamlit)** *(Tahapan Implementasi Berjalan)*:
   ```bash
   make run
   ```

## 🧠 Model dan Syarat Teknis

Proyek ini dipersiapkan dengan parameter spesifik:
- **T2I Model**: `runwayml/stable-diffusion-v1-5` (Wajib Seed: 222)
- **Inpaint Model**: `runwayml/stable-diffusion-inpainting` (Wajib Seed: 9)
- **Negative Prompt default**: *"photorealistic, realistic, photograph, 3d render, messy, blurry, low quality, bad art, ugly, sketch, grainy, unfinished, chromatic aberration"*

---
**Dikembangkan oleh [Nama Anda/Kelompok] untuk Image Generation Submission.**
