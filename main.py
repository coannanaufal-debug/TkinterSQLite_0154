import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

class AplikasiPrediksiDiabetes:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplikasi Prediksi Risiko Diabetes")
        self.root.geometry("900x700")
        self.root.minsize(750, 550)
        self.root.configure(bg="#f0f0f0")
        
        # Grid weight agar responsif saat resize/maximize
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
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
        # Gula darah ≥ 200 mg/dL → Tinggi / Sangat Tinggi
        if gula_darah >= 200:
            if bmi >= 30 or riwayat_ortu == "Ya":
                return "Sangat Tinggi", "#8B0000"
            else:
                return "Tinggi", "#DC143C"
        
        # Gula darah 140-199 mg/dL → Sedang / Tinggi
        elif 140 <= gula_darah < 200:
            if bmi >= 30 and riwayat_ortu == "Ya":
                return "Tinggi", "#DC143C"
            elif bmi >= 30 or riwayat_ortu == "Ya":
                return "Sedang", "#FF8C00"
            else:
                return "Sedang", "#FF8C00"
        
        # Gula darah < 140 mg/dL dan BMI ≥ 30 → Waspada / Sedang
        elif gula_darah < 140 and bmi >= 30:
            if riwayat_ortu == "Ya":
                return "Sedang", "#FF8C00"
            else:
                return "Waspada", "#D4AC0D"
        
        # Gula darah < 140 mg/dL, BMI < 30, ada riwayat → Waspada
        elif gula_darah < 140 and bmi < 30 and riwayat_ortu == "Ya":
            return "Waspada", "#D4AC0D"
        
        # Gula darah < 140 mg/dL, BMI < 30, tidak ada riwayat → Rendah
        else:
            return "Rendah", "#228B22"
        
    def create_widgets(self):
        """Membuat komponen GUI yang fleksibel dan responsif"""
        main_frame = tk.Frame(self.root, bg="#f0f0f0", padx=20, pady=20)
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(2, weight=1)
        
        # Judul
        title_label = tk.Label(
            main_frame, 
            text="SISTEM PREDIKSI RISIKO DIABETES", 
            font=("Arial", 18, "bold"),
            bg="#f0f0f0",
            fg="#333333"
        )
        title_label.grid(row=0, column=0, pady=(0, 15), sticky="ew")
        
        # Frame Form Input
        input_frame = tk.LabelFrame(
            main_frame, 
            text=" Input Data Pasien ", 
            font=("Arial", 11, "bold"),
            bg="#f0f0f0", 
            fg="#333333",
            padx=15, 
            pady=15
        )
        input_frame.grid(row=1, column=0, sticky="ew", pady=(0, 15))
        input_frame.grid_columnconfigure(1, weight=1)
        
        # Input fields
        fields = [
            ("Nama Pasien:", "entry_nama", 0),
            ("Usia (tahun):", "entry_usia", 1),
            ("Kadar Gula Darah (mg/dL):", "entry_gula", 2),
            ("BMI (Body Mass Index):", "entry_bmi", 3)
        ]
        
        for label_text, attr_name, r in fields:
            lbl = tk.Label(input_frame, text=label_text, font=("Arial", 11), bg="#f0f0f0")
            lbl.grid(row=r, column=0, sticky="w", pady=6, padx=5)
            
            entry = tk.Entry(input_frame, font=("Arial", 11), relief="solid", bd=1)
            entry.grid(row=r, column=1, sticky="ew", pady=6, padx=5)
            setattr(self, attr_name, entry)
        
        # Combobox Riwayat Ortu
        lbl_riwayat = tk.Label(input_frame, text="Riwayat Diabetes Orang Tua:", font=("Arial", 11), bg="#f0f0f0")
        lbl_riwayat.grid(row=4, column=0, sticky="w", pady=6, padx=5)
        
        self.combo_riwayat = ttk.Combobox(
            input_frame, values=["Ya", "Tidak"], state="readonly", font=("Arial", 11)
        )
        self.combo_riwayat.grid(row=4, column=1, sticky="ew", pady=6, padx=5)
        self.combo_riwayat.current(1)
        
        self.entry_bmi.bind('<Return>', lambda e: self.submit_data())
        
        # Tombol
        btn_frame = tk.Frame(input_frame, bg="#f0f0f0")
        btn_frame.grid(row=5, column=0, columnspan=2, pady=(15, 0), sticky="ew")
        btn_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        btn_prediksi = tk.Button(
            btn_frame, text="PREDIKSI RISIKO", command=self.submit_data,
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
        
        # Tombol untuk tabel
        table_btn_frame = tk.Frame(table_frame, bg="#f0f0f0")
        table_btn_frame.grid(row=2, column=0, columnspan=2, pady=(10, 0), sticky="ew")
        table_btn_frame.grid_columnconfigure((0, 1), weight=1)
        
        btn_delete = tk.Button(
            table_btn_frame, text="HAPUS DATA TERPILIH", command=self.delete_selected,
            font=("Arial", 10, "bold"), bg="#E74C3C", fg="white", cursor="hand2", pady=3
        )
        btn_delete.grid(row=0, column=0, padx=5, sticky="ew")
        
        btn_export = tk.Button(
            table_btn_frame, text="LIHAT DETAIL", command=self.view_detail,
            font=("Arial", 10, "bold"), bg="#3498DB", fg="white", cursor="hand2", pady=3
        )
        btn_export.grid(row=0, column=1, padx=5, sticky="ew")
        
        # Label Hasil
        self.label_hasil = tk.Label(
            input_frame, text="", font=("Arial", 12, "bold"), bg="#f0f0f0", fg="#000000"
        )
        self.label_hasil.grid(row=6, column=0, columnspan=2, pady=(10, 0), sticky="ew")
        
        # Frame Tabel Data
        table_frame = tk.LabelFrame(
            main_frame, 
            text=" Riwayat Data Pasien ", 
            font=("Arial", 11, "bold"),
            bg="#f0f0f0", 
            fg="#333333",
            padx=10, 
            pady=10
        )
        table_frame.grid(row=2, column=0, sticky="nsew")
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        
        tree_scroll_y = tk.Scrollbar(table_frame, orient="vertical")
        tree_scroll_y.grid(row=0, column=1, sticky="ns")
        
        tree_scroll_x = tk.Scrollbar(table_frame, orient="horizontal")
        tree_scroll_x.grid(row=1, column=0, sticky="ew")
        
        self.tree = ttk.Treeview(
            table_frame,
            yscrollcommand=tree_scroll_y.set,
            xscrollcommand=tree_scroll_x.set,
            selectmode="browse"
        )
        self.tree.grid(row=0, column=0, sticky="nsew")
        
        tree_scroll_y.config(command=self.tree.yview)
        tree_scroll_x.config(command=self.tree.xview)
        
        self.tree['columns'] = ("ID", "Nama", "Usia", "Gula Darah", "BMI", "Riwayat Ortu", "Hasil Prediksi")
        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.column("ID", anchor="center", width=50)
        self.tree.column("Nama", anchor="w", width=160)
        self.tree.column("Usia", anchor="center", width=80)
        self.tree.column("Gula Darah", anchor="center", width=100)
        self.tree.column("BMI", anchor="center", width=80)
        self.tree.column("Riwayat Ortu", anchor="center", width=110)
        self.tree.column("Hasil Prediksi", anchor="center", width=130)
        
        self.tree.heading("#0", text="", anchor="w")
        self.tree.heading("ID", text="ID", anchor="center")
        self.tree.heading("Nama", text="Nama Pasien", anchor="w")
        self.tree.heading("Usia", text="Usia", anchor="center")
        self.tree.heading("Gula Darah", text="Gula Darah", anchor="center")
        self.tree.heading("BMI", text="BMI", anchor="center")
        self.tree.heading("Riwayat Ortu", text="Riwayat Ortu", anchor="center")
        self.tree.heading("Hasil Prediksi", text="Hasil Prediksi", anchor="center")
        
        self.status_bar = tk.Label(
            self.root, text="Siap - Masukkan data pasien", font=("Arial", 9),
            bg="#e0e0e0", anchor="w", padx=10, pady=3
        )
        self.status_bar.grid(row=1, column=0, sticky="ew")
        
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

            if usia <= 0 or usia > 150:
                messagebox.showerror("Error", "Usia tidak valid! Masukkan usia antara 1-150 tahun.")
                return

            if gula < 0 or gula > 600:
                messagebox.showerror("Error", "Kadar gula darah tidak valid! Masukkan nilai antara 0-600 mg/dL.")
                return

            if bmi < 10 or bmi > 60:
                messagebox.showerror("Error", "BMI tidak valid! Masukkan BMI antara 10-60.")
                return
            
            if not riwayat or riwayat not in ["Ya", "Tidak"]:
                messagebox.showerror("Error", "Pilih riwayat diabetes orang tua (Ya/Tidak)!")
                return

            # Prediksi
            hasil, warna = self.prediksi_diabetes(gula, bmi, riwayat)

            # Simpan ke database
            self.cursor.execute('''
                INSERT INTO data_pasien (nama_pasien, usia, gula_darah, bmi, riwayat_ortu, hasil_prediksi)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (nama, usia, gula, bmi, riwayat, hasil))
            self.conn.commit()

            self.label_hasil.config(
                text=f"✓ Hasil Prediksi untuk {nama}: Risiko {hasil}",
                fg=warna
            )
            self.status_bar.config(text=f"Data {nama} disimpan | Risiko: {hasil}")
            
            messagebox.showinfo(
                "Hasil Prediksi", 
                f"Nama: {nama}\nUsia: {usia} tahun\nGula Darah: {gula} mg/dL\nBMI: {bmi}\nRiwayat Ortu: {riwayat}\n\n"
                f"HASIL PREDIKSI RISIKO DIABETES:\nRISIKO {hasil.upper()}"
            )
            
            self.clear_fields()
            self.load_table_data()

        except ValueError:
            messagebox.showerror("Error", "Pastikan usia & gula darah angka bulat, BMI angka desimal!")
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
    
    def delete_selected(self):
        """Menghapus data terpilih"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Peringatan", "Pilih data yang ingin dihapus!")
            return
        
        item = self.tree.item(selected[0])
        data_id = item['values'][0]
        nama = item['values'][1]
        
        confirm = messagebox.askyesno("Konfirmasi", f"Hapus data pasien {nama}?")
        if confirm:
            self.cursor.execute('DELETE FROM data_pasien WHERE id = ?', (data_id,))
            self.conn.commit()
            self.load_table_data()
            messagebox.showinfo("Sukses", f"Data {nama} berhasil dihapus!")
    
    def view_detail(self):
        """Menampilkan detail data terpilih"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Peringatan", "Pilih data untuk melihat detail!")
            return
        
        item = self.tree.item(selected[0])
        values = item['values']
        
        detail = f"""
DETAIL DATA PASIEN

ID             : {values[0]}
Nama Pasien    : {values[1]}
Usia           : {values[2]} tahun
Gula Darah     : {values[3]} mg/dL
BMI            : {values[4]}
Riwayat Ortu   : {values[5]}
Hasil Prediksi : RISIKO {values[6].upper()}
        """
        messagebox.showinfo("Detail Data Pasien", detail)

    def __del__(self):
        """Menutup koneksi database"""
        if hasattr(self, 'conn'):
            self.conn.close()

def main():
    root = tk.Tk()
    app = AplikasiPrediksiDiabetes(root)
    root.mainloop()

if __name__ == "__main__":
    main()
