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
    
    def prediksi_diabetes(self, gula_darah, bmi, riwayat_ortu):
        """Menentukan prediksi risiko diabetes berdasarkan kondisi"""
        # Gula darah ≥ 200 mg/dL → Tinggi/Sangat Tinggi
        if gula_darah >= 200:
            if bmi >= 30 or riwayat_ortu == "Ya":
                return "Sangat Tinggi", "#8B0000"
            else:
                return "Tinggi", "#DC143C"
        
        # Gula darah 140-199 mg/dL → Sedang/Tinggi
        elif 140 <= gula_darah < 200:
            if bmi >= 30 and riwayat_ortu == "Ya":
                return "Tinggi", "#DC143C"
            elif bmi >= 30 or riwayat_ortu == "Ya":
                return "Sedang", "#FF8C00"
            else:
                return "Sedang", "#FF8C00"
        
        # Gula darah < 140 mg/dL dan BMI ≥ 30 → Waspada/Sedang
        elif gula_darah < 140 and bmi >= 30:
            if riwayat_ortu == "Ya":
                return "Sedang", "#FF8C00"
            else:
                return "Waspada", "#FFD700"
        
        # Gula darah < 140 mg/dL, BMI < 30, ada riwayat → Waspada
        elif gula_darah < 140 and bmi < 30 and riwayat_ortu == "Ya":
            return "Waspada", "#FFD700"
        
        # Gula darah < 140 mg/dL, BMI < 30, tidak ada riwayat → Rendah
        else:
            return "Rendah", "#228B22"
        
        # Tombol-tombol aksi
        btn_frame = tk.Frame(input_frame, bg="#f0f0f0")
        btn_frame.grid(row=5, column=0, columnspan=2, pady=(15, 0), sticky="ew")
        btn_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        btn_prediksi = tk.Button(
            btn_frame, text="PREDIKSI", command=self.submit_data,
            font=("Arial", 11, "bold"), bg="#4CAF50", fg="white", cursor="hand2", pady=5
        )
        btn_prediksi.grid(row=0, column=0, padx=5, sticky="ew")
        
        btn_clear = tk.Button(
            btn_frame, text="CLEAR", command=self.clear_fields,
            font=("Arial", 11, "bold"), bg="#FF9800", fg="white", cursor="hand2", pady=5
        )
        btn_clear.grid(row=0, column=1, padx=5, sticky="ew")
        
        btn_refresh = tk.Button(
            btn_frame, text="LIHAT DATA", command=self.load_table_data,
            font=("Arial", 11, "bold"), bg="#2196F3", fg="white", cursor="hand2", pady=5
        )
        btn_refresh.grid(row=0, column=2, padx=5, sticky="ew")
        
        # Label hasil prediksi
        self.label_hasil = tk.Label(
            input_frame, text="", font=("Arial", 12, "bold"), bg="#f0f0f0", fg="#000000"
        )
        self.label_hasil.grid(row=6, column=0, columnspan=2, pady=(10, 0), sticky="ew")
        
        # Frame tabel data pasien
        table_frame = tk.LabelFrame(
            self.root,
            text=" Riwayat Data Pasien ",
            font=("Arial", 11, "bold"),
            bg="#f0f0f0",
            fg="#333333",
            padx=10,
            pady=10
        )
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Treeview dengan scrollbar
        tree_scroll_y = tk.Scrollbar(table_frame, orient="vertical")
        tree_scroll_y.pack(side="right", fill="y")
        tree_scroll_x = tk.Scrollbar(table_frame, orient="horizontal")
        tree_scroll_x.pack(side="bottom", fill="x")
        
        self.tree = ttk.Treeview(
            table_frame,
            yscrollcommand=tree_scroll_y.set,
            xscrollcommand=tree_scroll_x.set,
            selectmode="browse"
        )
        self.tree.pack(fill="both", expand=True)
        tree_scroll_y.config(command=self.tree.yview)
        tree_scroll_x.config(command=self.tree.xview)
        
        # Kolom tabel
        self.tree['columns'] = ("ID", "Nama", "Usia", "Gula", "BMI", "Riwayat", "Prediksi")
        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.column("ID", anchor="center", width=50)
        self.tree.column("Nama", anchor="w", width=150)
        self.tree.column("Usia", anchor="center", width=80)
        self.tree.column("Gula", anchor="center", width=80)
        self.tree.column("BMI", anchor="center", width=80)
        self.tree.column("Riwayat", anchor="center", width=100)
        self.tree.column("Prediksi", anchor="center", width=120)
        
        self.tree.heading("#0", text="")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nama", text="Nama Pasien")
        self.tree.heading("Usia", text="Usia")
        self.tree.heading("Gula", text="Gula Darah")
        self.tree.heading("BMI", text="BMI")
        self.tree.heading("Riwayat", text="Riwayat Ortu")
        self.tree.heading("Prediksi", text="Hasil Prediksi")
        
        # Status bar
        self.status_bar = tk.Label(
            self.root, text="Siap - Masukkan data pasien", font=("Arial", 9),
            bg="#e0e0e0", anchor="w", padx=10, pady=3
        )
        self.status_bar.pack(fill="x", side="bottom")
        
        # Load data awal
        self.load_table_data()
        
    def submit_data(self):
        """Menyimpan data dan melakukan prediksi"""
        try:
            nama = self.entry_nama.get().strip()
            usia = self.entry_usia.get().strip()
            gula = self.entry_gula.get().strip()
            bmi = self.entry_bmi.get().strip()
            riwayat = self.combo_riwayat.get()

            # Validasi input
            if not nama:
                messagebox.showerror("Error", "Nama pasien tidak boleh kosong!")
                return
            if not usia or not gula or not bmi:
                messagebox.showerror("Error", "Semua data harus diisi!")
                return
            usia = int(usia)
            gula = int(gula)
            bmi = float(bmi)

            # Prediksi
            hasil, warna = self.prediksi_diabetes(gula, bmi, riwayat)

            # Simpan ke database
            self.cursor.execute('''
                INSERT INTO data_pasien (nama_pasien, usia, gula_darah, bmi, riwayat_ortu, hasil_prediksi)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (nama, usia, gula, bmi, riwayat, hasil))
            self.conn.commit()

            self.label_hasil.config(text=f"✓ Hasil prediksi untuk {nama}: Risiko {hasil}", fg=warna)
            self.status_bar.config(text=f"Data {nama} disimpan | Risiko: {hasil}")
            messagebox.showinfo("Hasil Prediksi", f"Nama: {nama}\nUsia: {usia}\nGula: {gula}\nBMI: {bmi}\nRiwayat Ortu: {riwayat}\n\nRisiko Diabetes: {hasil}")
            
            self.clear_fields()
            self.load_table_data()
        except ValueError:
            messagebox.showerror("Error", "Pastikan usia & gula darah angka, BMI angka desimal!")
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}")
    
    def clear_fields(self):
        """Membersihkan semua input field"""
        self.entry_nama.delete(0, tk.END)
        self.entry_usia.delete(0, tk.END)
        self.entry_gula.delete(0, tk.END)
        self.entry_bmi.delete(0, tk.END)
        self.combo_riwayat.current(1)
        self.label_hasil.config(text="")
        self.status_bar.config(text="Form dibersihkan")
    
    def load_table_data(self):
        """Memuat kembali data ke tabel"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.cursor.execute('SELECT * FROM data_pasien')
        rows = self.cursor.fetchall()
        for row in rows:
            self.tree.insert("", "end", values=row)
        self.status_bar.config(text=f"Total Data Pasien: {len(rows)}")
    
    def __del__(self):
        """Menutup koneksi database"""
        if hasattr(self, 'conn'):
            self.conn.close()

        
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
