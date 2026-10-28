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

def main():
    root = tk.Tk()
    app = AplikasiPrediksiDiabetes(root)
    root.mainloop()

if __name__ == "__main__":
    main()
