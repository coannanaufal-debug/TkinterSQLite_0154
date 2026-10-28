# Aplikasi Prediksi Risiko Diabetes

Aplikasi desktop berbasis Python menggunakan Tkinter dan SQLite untuk memprediksi risiko diabetes berdasarkan data pasien.

## Fitur

- **Input Data Pasien**: Nama, usia, kadar gula darah, BMI, dan riwayat diabetes orang tua
- **Prediksi Risiko Otomatis**: Berdasarkan algoritma medis dengan 5 tingkat risiko
- **Penyimpanan Database**: SQLite dengan tabel `data_pasien`
- **Tampilan Tabel Interaktif**: Melihat semua riwayat data pasien
- **Hapus & Lihat Detail**: Mengelola data pasien yang tersimpan
- **Validasi Input Lengkap**: Memastikan data yang dimasukkan valid
- **GUI Responsif**: Layout fleksibel yang menyesuaikan ukuran window

## Struktur Database

**Database:** `prediksi_diabetes.db`  
**Tabel:** `data_pasien`

| Kolom | Tipe | Keterangan |
|-------|------|------------|
| id | INTEGER | Primary Key (Auto Increment) |
| nama_pasien | TEXT | Nama lengkap pasien |
| usia | INTEGER | Usia dalam tahun |
| gula_darah | INTEGER | Kadar gula darah dalam mg/dL |
| bmi | REAL | Body Mass Index |
| riwayat_ortu | TEXT | Riwayat diabetes orang tua (Ya/Tidak) |
| hasil_prediksi | TEXT | Hasil prediksi risiko |

## Logika Prediksi Risiko

### Tingkat Risiko:
1. **Rendah** 🟢 - Gula darah < 140, BMI < 30, tidak ada riwayat
2. **Waspada** 🟡 - Gula darah < 140, BMI ≥ 30 atau ada riwayat
3. **Sedang** 🟠 - Gula darah 140-199 atau kombinasi faktor risiko
4. **Tinggi** 🔴 - Gula darah ≥ 200 atau BMI tinggi + riwayat
5. **Sangat Tinggi** ⚫ - Gula darah ≥ 200 dengan BMI tinggi atau riwayat

### Kondisi Detail:

- **Gula darah ≥ 200 mg/dL** → Risiko Tinggi/Sangat Tinggi
- **Gula darah 140-199 mg/dL** → Risiko Sedang/Tinggi (tergantung BMI & riwayat)
- **Gula darah < 140 mg/dL dan BMI ≥ 30** → Risiko Waspada/Sedang
- **Gula darah < 140 mg/dL, BMI < 30, ada riwayat** → Risiko Waspada
- **Gula darah < 140 mg/dL, BMI < 30, tidak ada riwayat** → Risiko Rendah

## Cara Menjalankan

1. Pastikan Python 3.x terinstal
2. Clone repository ini
3. Jalankan aplikasi:
   ```bash
   python main.py
   ```

## Cara Penggunaan

1. Masukkan data pasien (nama, usia, gula darah, BMI)
2. Pilih riwayat diabetes orang tua (Ya/Tidak)
3. Klik tombol **PREDIKSI RISIKO**
4. Hasil prediksi akan ditampilkan dengan warna sesuai tingkat risiko
5. Data otomatis tersimpan dan muncul di tabel bawah
6. Gunakan **LIHAT DATA** untuk refresh tabel
7. Pilih data di tabel lalu klik **HAPUS DATA TERPILIH** untuk menghapus
8. Klik **LIHAT DETAIL** untuk melihat informasi lengkap data terpilih

## Validasi Input

- **Nama**: Tidak boleh kosong
- **Usia**: 1-150 tahun
- **Gula Darah**: 0-600 mg/dL
- **BMI**: 10-60
- **Riwayat Ortu**: Harus pilih Ya/Tidak

## Teknologi

- **Python 3**
- **Tkinter** (GUI)
- **SQLite3** (Database)
- **ttk** (Treeview & Combobox)

## Fitur GUI

- Layout responsif dengan grid weight
- Status bar menampilkan informasi real-time
- Tabel scrollable dengan scrollbar horizontal & vertikal
- Warna hasil prediksi dinamis sesuai tingkat risiko
- Tombol Enter untuk submit langsung

## Lisensi

Project ini dibuat untuk keperluan praktikum mata kuliah Pemrograman.
