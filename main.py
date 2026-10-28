import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

def init_database():
    """Membuat database prediksi_diabetes.db dan tabel data_pasien"""
    conn = sqlite3.connect('prediksi_diabetes.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS data_pasien (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_pasien TEXT NOT NULL,
            usia INTEGER NOT NULL,
            gula_darah INTEGER NOT NULL,
            bmi REAL NOT NULL,
            riwayat_ortu TEXT NOT NULL,
            hasil_prediksi TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def main():
    init_database()
    root = tk.Tk()
    root.title("Aplikasi Prediksi Risiko Diabetes")
    root.geometry("900x700")
    root.configure(bg="#f0f0f0")
    root.mainloop()

if __name__ == "__main__":
    main()
