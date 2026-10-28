import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

class AplikasiPrediksiDiabetes:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplikasi Prediksi Risiko Diabetes")
        self.root.geometry("900x700")
        self.root.configure(bg="#f0f0f0")
        
        self.init_database()
        self.create_widgets()
        
    def init_database(self):
        """Membuat database prediksi_diabetes.db dan tabel data_pasien"""
        self.conn = sqlite3.connect('prediksi_diabetes.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
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
        self.conn.commit()
        
    def create_widgets(self):
        """Membuat komponen GUI"""
        title_label = tk.Label(
            self.root, 
            text="SISTEM PREDIKSI RISIKO DIABETES", 
            font=("Arial", 18, "bold"),
            bg="#f0f0f0",
            fg="#333333"
        )
        title_label.pack(pady=20)
        
        # Frame untuk input
        input_frame = tk.LabelFrame(
            self.root,
            text=" Input Data Pasien ",
            font=("Arial", 11, "bold"),
            bg="#f0f0f0",
            padx=20,
            pady=15
        )
        input_frame.pack(padx=20, pady=10, fill="x")
        
        # Nama Pasien
        tk.Label(input_frame, text="Nama Pasien:", font=("Arial", 11), bg="#f0f0f0").grid(
            row=0, column=0, sticky="w", pady=8, padx=5
        )
        self.entry_nama = tk.Entry(input_frame, font=("Arial", 11), width=40)
        self.entry_nama.grid(row=0, column=1, pady=8, padx=5)
        
        # Usia
        tk.Label(input_frame, text="Usia (tahun):", font=("Arial", 11), bg="#f0f0f0").grid(
            row=1, column=0, sticky="w", pady=8, padx=5
        )
        self.entry_usia = tk.Entry(input_frame, font=("Arial", 11), width=40)
        self.entry_usia.grid(row=1, column=1, pady=8, padx=5)
        
        # Gula Darah
        tk.Label(input_frame, text="Kadar Gula Darah (mg/dL):", font=("Arial", 11), bg="#f0f0f0").grid(
            row=2, column=0, sticky="w", pady=8, padx=5
        )
        self.entry_gula = tk.Entry(input_frame, font=("Arial", 11), width=40)
        self.entry_gula.grid(row=2, column=1, pady=8, padx=5)
        
        # BMI
        tk.Label(input_frame, text="BMI (Body Mass Index):", font=("Arial", 11), bg="#f0f0f0").grid(
            row=3, column=0, sticky="w", pady=8, padx=5
        )
        self.entry_bmi = tk.Entry(input_frame, font=("Arial", 11), width=40)
        self.entry_bmi.grid(row=3, column=1, pady=8, padx=5)
        
        # Riwayat Orang Tua - Combobox
        tk.Label(input_frame, text="Riwayat Diabetes Orang Tua:", font=("Arial", 11), bg="#f0f0f0").grid(
            row=4, column=0, sticky="w", pady=8, padx=5
        )
        self.combo_riwayat = ttk.Combobox(
            input_frame,
            values=["Ya", "Tidak"],
            state="readonly",
            font=("Arial", 11),
            width=38
        )
        self.combo_riwayat.grid(row=4, column=1, pady=8, padx=5)
        self.combo_riwayat.current(1)  # Default "Tidak"

def main():
    root = tk.Tk()
    app = AplikasiPrediksiDiabetes(root)
    root.mainloop()

if __name__ == "__main__":
    main()
