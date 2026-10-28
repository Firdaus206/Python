import os
import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

# --- KONFIGURASI DATABASE ---
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'siakad'
}

def connect_db():
    return mysql.connector.connect(**DB_CONFIG)

# Helper untuk memberikan efek Hover pada tombol
def make_hover(btn, normal_bg, hover_bg):
    btn.bind("<Enter>", lambda e: btn.config(bg=hover_bg))
    btn.bind("<Leave>", lambda e: btn.config(bg=normal_bg))


# ==========================================
# 1. JENDELA LOGIN (MODERN GUI)
# ==========================================
class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Login - SIAKAD")
        self.root.geometry("420x360")
        self.root.resizable(False, False)
        self.root.configure(bg="#F1F5F9")

        # Container Utama
        main_frame = tk.Frame(self.root, bg="#FFFFFF", bd=1, relief=tk.SOLID)
        main_frame.pack(expand=True, fill=tk.BOTH, padx=25, pady=25)

        # Header Title
        lbl_title = tk.Label(
            main_frame, 
            text="SIAKAD LOGIN", 
            font=("Segoe UI", 18, "bold"),
            bg="#FFFFFF", 
            fg="#1E3A8A"
        )
        lbl_title.pack(pady=(20, 15))

        # Form Input Frame
        form_frame = tk.Frame(main_frame, bg="#FFFFFF")
        form_frame.pack(padx=10)

        # Role
        lbl_role = tk.Label(form_frame, text="Login Sebagai", font=("Segoe UI", 10, "bold"), bg="#FFFFFF", fg="#475569", anchor="w")
        lbl_role.grid(row=0, column=0, sticky="w", pady=(0, 2))
        
        self.combo_role = ttk.Combobox(form_frame, values=["Dosen", "Mahasiswa"], state="readonly", width=28, font=("Segoe UI", 10))
        self.combo_role.set("Dosen")
        self.combo_role.grid(row=1, column=0, pady=(0, 10))

        # Username
        lbl_user = tk.Label(form_frame, text="Username (NIP / NIM)", font=("Segoe UI", 10, "bold"), bg="#FFFFFF", fg="#475569", anchor="w")
        lbl_user.grid(row=2, column=0, sticky="w", pady=(0, 2))
        
        self.entry_user = tk.Entry(form_frame, font=("Segoe UI", 10), width=30, relief=tk.SOLID, bd=1)
        self.entry_user.grid(row=3, column=0, pady=(0, 10))
        self.entry_user.focus()

        # Password
        lbl_pass = tk.Label(form_frame, text="Password (Email)", font=("Segoe UI", 10, "bold"), bg="#FFFFFF", fg="#475569", anchor="w")
        lbl_pass.grid(row=4, column=0, sticky="w", pady=(0, 2))
        
        self.entry_pass = tk.Entry(form_frame, font=("Segoe UI", 10), width=30, show="*", relief=tk.SOLID, bd=1)
        self.entry_pass.grid(row=5, column=0, pady=(0, 10))

        # Tombol Login
        btn_login = tk.Button(
            main_frame, 
            text="Masuk ke Sistem", 
            font=("Segoe UI", 10, "bold"),
            bg="#2563EB", 
            fg="white", 
            activebackground="#1D4ED8",
            activeforeground="white",
            width=26, 
            bd=0, 
            cursor="hand2", 
            pady=6,
            command=self.proses_login
        )
        btn_login.pack(pady=(10, 15))
        make_hover(btn_login, "#2563EB", "#1D4ED8")

        self.root.bind('<Return>', lambda event: self.proses_login())

    def proses_login(self):
        role = self.combo_role.get()
        username = self.entry_user.get().strip()
        password = self.entry_pass.get().strip()

        if not username or not password:
            messagebox.showwarning("Peringatan", "Username dan Password wajib diisi!")
            return

        conn = None
        cursor = None

        try:
            conn = connect_db()
            cursor = conn.cursor(dictionary=True)

            if role == "Dosen":
                query = "SELECT nip AS id, nama_dosen AS nama, email FROM dosen WHERE nip = %s AND email = %s"
            else:
                query = "SELECT nim AS id, nama_lengkap AS nama, email FROM mahasiswa WHERE nim = %s AND email = %s"

            cursor.execute(query, (username, password))
            user = cursor.fetchone()

            if user:
                messagebox.showinfo("Berhasil", f"Login Berhasil sebagai {role}!\nSelamat datang, {user['nama']}.")
                self.buka_dashboard(user, role)
            else:
                messagebox.showerror("Gagal", f"Login {role} Gagal!\nUsername atau Password salah.")

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Koneksi database bermasalah:\n{err}")
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()

    def buka_dashboard(self, user, role):
        self.root.destroy()
        dashboard = AplikasiSIAKAD(user, role)
        dashboard.mainloop()


# ==========================================
# 2. TABULAR DASHBOARD (6 TABEL SIAKAD)
# ==========================================

# --- TAB DATA DOSEN ---
class TabDosen(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        frame_form = tk.LabelFrame(self, text=" Form Data Dosen ", font=("Segoe UI", 10, "bold"), padx=12, pady=10, bg="#FFFFFF")
        frame_form.pack(fill="x", padx=15, pady=10)

        labels = ["NIP", "Nama Dosen", "Jenis Kelamin", "Email", "No Telepon", "Pendidikan Terakhir", "Bidang Keahlian"]
        for i, label_text in enumerate(labels):
            tk.Label(frame_form, text=label_text, font=("Segoe UI", 9), bg="#FFFFFF").grid(row=i//2, column=(i%2)*2, sticky="w", padx=5, pady=4)

        self.entry_nip = tk.Entry(frame_form, font=("Segoe UI", 9))
        self.entry_nip.grid(row=0, column=1, padx=5, pady=4, sticky="ew")

        self.entry_nama = tk.Entry(frame_form, font=("Segoe UI", 9))
        self.entry_nama.grid(row=0, column=3, padx=5, pady=4, sticky="ew")

        self.combo_jk = ttk.Combobox(frame_form, values=["Laki-laki", "Perempuan"], state="readonly", font=("Segoe UI", 9))
        self.combo_jk.grid(row=1, column=1, padx=5, pady=4, sticky="ew")

        self.entry_email = tk.Entry(frame_form, font=("Segoe UI", 9))
        self.entry_email.grid(row=1, column=3, padx=5, pady=4, sticky="ew")

        self.entry_tlp = tk.Entry(frame_form, font=("Segoe UI", 9))
        self.entry_tlp.grid(row=2, column=1, padx=5, pady=4, sticky="ew")

        self.entry_pendidikan = tk.Entry(frame_form, font=("Segoe UI", 9))
        self.entry_pendidikan.grid(row=2, column=3, padx=5, pady=4, sticky="ew")

        self.entry_bidang = tk.Entry(frame_form, font=("Segoe UI", 9))
        self.entry_bidang.grid(row=3, column=1, padx=5, pady=4, sticky="ew")

        frame_form.grid_columnconfigure(1, weight=1)
        frame_form.grid_columnconfigure(3, weight=1)

        # Frame Tombol Action
        frame_btn = tk.Frame(self, bg="#F8FAFC")
        frame_btn.pack(fill="x", padx=15, pady=5)

        btn_add = tk.Button(frame_btn, text="Tambah", bg="#10B981", fg="white", font=("Segoe UI", 9, "bold"), bd=0, padx=15, pady=5, cursor="hand2", command=self.tambah_data)
        btn_add.pack(side="left", padx=5)
        make_hover(btn_add, "#10B981", "#059669")

        btn_edit = tk.Button(frame_btn, text="Edit", bg="#3B82F6", fg="white", font=("Segoe UI", 9, "bold"), bd=0, padx=15, pady=5, cursor="hand2", command=self.edit_data)
        btn_edit.pack(side="left", padx=5)
        make_hover(btn_edit, "#3B82F6", "#2563EB")

        btn_del = tk.Button(frame_btn, text="Hapus", bg="#EF4444", fg="white", font=("Segoe UI", 9, "bold"), bd=0, padx=15, pady=5, cursor="hand2", command=self.hapus_data)
        btn_del.pack(side="left", padx=5)
        make_hover(btn_del, "#EF4444", "#DC2626")

        btn_clr = tk.Button(frame_btn, text="Clear", bg="#64748B", fg="white", font=("Segoe UI", 9, "bold"), bd=0, padx=15, pady=5, cursor="hand2", command=self.clear_fields)
        btn_clr.pack(side="left", padx=5)
        make_hover(btn_clr, "#64748B", "#475569")

        # Tabel Data
        frame_table = tk.Frame(self, bg="#FFFFFF")
        frame_table.pack(fill="both", expand=True, padx=15, pady=10)

        columns = ("nip", "nama_dosen", "jenis_kelamin", "email", "no_telepon", "pendidikan_terakhir", "bidang_keahlian")
        self.tree = ttk.Treeview(frame_table, columns=columns, show="headings")

        headers = ["NIP", "Nama Dosen", "Jenis Kelamin", "Email", "No Telepon", "Pendidikan", "Bidang Keahlian"]
        for col, head in zip(columns, headers):
            self.tree.heading(col, text=head)
            self.tree.column(col, width=120)

        self.tree.bind("<<TreeviewSelect>>", self.select_item)

        scrollbar = ttk.Scrollbar(frame_table, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def load_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        try:
            db = connect_db()
            cursor = db.cursor()
            cursor.execute("SELECT * FROM dosen")
            for row in cursor.fetchall():
                self.tree.insert("", "end", values=row)
            db.close()
        except Exception as e:
            messagebox.showerror("Error", f"Gagal mengambil data dosen: {e}")

    def tambah_data(self):
        nip = self.entry_nip.get()
        nama = self.entry_nama.get()
        if not nip or not nama:
            messagebox.showwarning("Warning", "NIP dan Nama wajib diisi!")
            return
        try:
            db = connect_db()
            cursor = db.cursor()
            sql = "INSERT INTO dosen VALUES (%s, %s, %s, %s, %s, %s, %s)"
            val = (nip, nama, self.combo_jk.get(), self.entry_email.get(), self.entry_tlp.get(), self.entry_pendidikan.get(), self.entry_bidang.get())
            cursor.execute(sql, val)
            db.commit()
            db.close()
            messagebox.showinfo("Sukses", "Data berhasil ditambahkan!")
            self.clear_fields()
            self.load_data()
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menambah data: {e}")

    def edit_data(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Pilih data di tabel yang ingin diubah!")
            return
        try:
            db = connect_db()
            cursor = db.cursor()
            sql = """UPDATE dosen SET nama_dosen=%s, jenis_kelamin=%s, email=%s, 
                     no_telepon=%s, pendidikan_terakhir=%s, bidang_keahlian=%s WHERE nip=%s"""
            val = (self.entry_nama.get(), self.combo_jk.get(), self.entry_email.get(), 
                   self.entry_tlp.get(), self.entry_pendidikan.get(), self.entry_bidang.get(), self.entry_nip.get())
            cursor.execute(sql, val)
            db.commit()
            db.close()
            messagebox.showinfo("Sukses", "Data berhasil diperbarui!")
            self.clear_fields()
            self.load_data()
        except Exception as e:
            messagebox.showerror("Error", f"Gagal memperbarui data: {e}")

    def hapus_data(self):
        if not self.tree.selection():
            messagebox.showwarning("Warning", "Pilih data di tabel!")
            return
        nip = self.entry_nip.get()
        if messagebox.askyesno("Konfirmasi", f"Yakin hapus dosen NIP {nip}?"):
            try:
                db = connect_db()
                cursor = db.cursor()
                cursor.execute("DELETE FROM dosen WHERE nip = %s", (nip,))
                db.commit()
                db.close()
                messagebox.showinfo("Sukses", "Data berhasil dihapus!")
                self.clear_fields()
                self.load_data()
            except Exception as e:
                messagebox.showerror("Error", f"Gagal menghapus data: {e}")

    def select_item(self, event):
        selected = self.tree.selection()
        if selected:
            values = self.tree.item(selected[0], "values")
            self.clear_fields()
            self.entry_nip.insert(0, values[0])
            self.entry_nama.insert(0, values[1])
            self.combo_jk.set(values[2])
            self.entry_email.insert(0, values[3])
            self.entry_tlp.insert(0, values[4])
            self.entry_pendidikan.insert(0, values[5])
            self.entry_bidang.insert(0, values[6])

    def clear_fields(self):
        self.entry_nip.delete(0, tk.END)
        self.entry_nama.delete(0, tk.END)
        self.combo_jk.set("")
        self.entry_email.delete(0, tk.END)
        self.entry_tlp.delete(0, tk.END)
        self.entry_pendidikan.delete(0, tk.END)
        self.entry_bidang.delete(0, tk.END)


# --- TAB DATA MAHASISWA ---
class TabMahasiswa(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        frame_form = tk.LabelFrame(self, text=" Form Data Mahasiswa ", font=("Segoe UI", 10, "bold"), padx=12, pady=10, bg="#FFFFFF")
        frame_form.pack(fill="x", padx=15, pady=10)

        tk.Label(frame_form, text="NIM", font=("Segoe UI", 9), bg="#FFFFFF").grid(row=0, column=0, sticky="w", padx=5, pady=4)
        self.entry_nim = tk.Entry(frame_form, font=("Segoe UI", 9))
        self.entry_nim.grid(row=0, column=1, padx=5, pady=4, sticky="ew")

        tk.Label(frame_form, text="Nama Lengkap", font=("Segoe UI", 9), bg="#FFFFFF").grid(row=0, column=2, sticky="w", padx=5, pady=4)
        self.entry_nama = tk.Entry(frame_form, font=("Segoe UI", 9))
        self.entry_nama.grid(row=0, column=3, padx=5, pady=4, sticky="ew")

        tk.Label(frame_form, text="Jenis Kelamin", font=("Segoe UI", 9), bg="#FFFFFF").grid(row=1, column=0, sticky="w", padx=5, pady=4)
        self.combo_jk = ttk.Combobox(frame_form, values=["Laki-laki", "Perempuan"], state="readonly", font=("Segoe UI", 9))
        self.combo_jk.grid(row=1, column=1, padx=5, pady=4, sticky="ew")

        tk.Label(frame_form, text="Tgl Lahir (YYYY-MM-DD)", font=("Segoe UI", 9), bg="#FFFFFF").grid(row=1, column=2, sticky="w", padx=5, pady=4)
        self.entry_tgl = tk.Entry(frame_form, font=("Segoe UI", 9))
        self.entry_tgl.grid(row=1, column=3, padx=5, pady=4, sticky="ew")

        tk.Label(frame_form, text="Tempat Lahir", font=("Segoe UI", 9), bg="#FFFFFF").grid(row=2, column=0, sticky="w", padx=5, pady=4)
        self.entry_tmpt = tk.Entry(frame_form, font=("Segoe UI", 9))
        self.entry_tmpt.grid(row=2, column=1, padx=5, pady=4, sticky="ew")

        tk.Label(frame_form, text="Alamat", font=("Segoe UI", 9), bg="#FFFFFF").grid(row=2, column=2, sticky="w", padx=5, pady=4)
        self.entry_alamat = tk.Entry(frame_form, font=("Segoe UI", 9))
        self.entry_alamat.grid(row=2, column=3, padx=5, pady=4, sticky="ew")

        tk.Label(frame_form, text="No Telepon", font=("Segoe UI", 9), bg="#FFFFFF").grid(row=3, column=0, sticky="w", padx=5, pady=4)
        self.entry_tlp = tk.Entry(frame_form, font=("Segoe UI", 9))
        self.entry_tlp.grid(row=3, column=1, padx=5, pady=4, sticky="ew")

        tk.Label(frame_form, text="Email", font=("Segoe UI", 9), bg="#FFFFFF").grid(row=3, column=2, sticky="w", padx=5, pady=4)
        self.entry_email = tk.Entry(frame_form, font=("Segoe UI", 9))
        self.entry_email.grid(row=3, column=3, padx=5, pady=4, sticky="ew")

        tk.Label(frame_form, text="Jurusan", font=("Segoe UI", 9), bg="#FFFFFF").grid(row=4, column=0, sticky="w", padx=5, pady=4)
        self.entry_jurusan = tk.Entry(frame_form, font=("Segoe UI", 9))
        self.entry_jurusan.grid(row=4, column=1, padx=5, pady=4, sticky="ew")

        tk.Label(frame_form, text="Angkatan", font=("Segoe UI", 9), bg="#FFFFFF").grid(row=4, column=2, sticky="w", padx=5, pady=4)
        self.entry_angkatan = tk.Entry(frame_form, font=("Segoe UI", 9))
        self.entry_angkatan.grid(row=4, column=3, padx=5, pady=4, sticky="ew")

        tk.Label(frame_form, text="Status", font=("Segoe UI", 9), bg="#FFFFFF").grid(row=5, column=0, sticky="w", padx=5, pady=4)
        self.combo_status = ttk.Combobox(frame_form, values=["Aktif", "Cuti", "Lulus", "Non-Aktif"], state="readonly", font=("Segoe UI", 9))
        self.combo_status.grid(row=5, column=1, padx=5, pady=4, sticky="ew")

        frame_form.grid_columnconfigure(1, weight=1)
        frame_form.grid_columnconfigure(3, weight=1)

        # Frame Tombol Action
        frame_btn = tk.Frame(self, bg="#F8FAFC")
        frame_btn.pack(fill="x", padx=15, pady=5)

        btn_add = tk.Button(frame_btn, text="Tambah", bg="#10B981", fg="white", font=("Segoe UI", 9, "bold"), bd=0, padx=15, pady=5, cursor="hand2", command=self.tambah_data)
        btn_add.pack(side="left", padx=5)
        make_hover(btn_add, "#10B981", "#059669")

        btn_edit = tk.Button(frame_btn, text="Edit", bg="#3B82F6", fg="white", font=("Segoe UI", 9, "bold"), bd=0, padx=15, pady=5, cursor="hand2", command=self.edit_data)
        btn_edit.pack(side="left", padx=5)
        make_hover(btn_edit, "#3B82F6", "#2563EB")

        btn_del = tk.Button(frame_btn, text="Hapus", bg="#EF4444", fg="white", font=("Segoe UI", 9, "bold"), bd=0, padx=15, pady=5, cursor="hand2", command=self.hapus_data)
        btn_del.pack(side="left", padx=5)
        make_hover(btn_del, "#EF4444", "#DC2626")

        btn_clr = tk.Button(frame_btn, text="Clear", bg="#64748B", fg="white", font=("Segoe UI", 9, "bold"), bd=0, padx=15, pady=5, cursor="hand2", command=self.clear_fields)
        btn_clr.pack(side="left", padx=5)
        make_hover(btn_clr, "#64748B", "#475569")

        frame_table = tk.Frame(self, bg="#FFFFFF")
        frame_table.pack(fill="both", expand=True, padx=15, pady=10)

        columns = ("nim", "nama_lengkap", "jenis_kelamin", "tanggal_lahir", "tempat_lahir", "alamat", "no_telepon", "email", "jurusan", "angkatan", "status")
        self.tree = ttk.Treeview(frame_table, columns=columns, show="headings")

        headers = ["NIM", "Nama Lengkap", "JK", "Tgl Lahir", "Tempat Lahir", "Alamat", "No Tlp", "Email", "Jurusan", "Angkatan", "Status"]
        for col, head in zip(columns, headers):
            self.tree.heading(col, text=head)
            self.tree.column(col, width=100)

        self.tree.bind("<<TreeviewSelect>>", self.select_item)

        scrollbar_v = ttk.Scrollbar(frame_table, orient="vertical", command=self.tree.yview)
        scrollbar_h = ttk.Scrollbar(frame_table, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=scrollbar_v.set, xscrollcommand=scrollbar_h.set)

        scrollbar_v.pack(side="right", fill="y")
        scrollbar_h.pack(side="bottom", fill="x")
        self.tree.pack(side="left", fill="both", expand=True)

    def load_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        try:
            db = connect_db()
            cursor = db.cursor()
            cursor.execute("SELECT * FROM mahasiswa")
            for row in cursor.fetchall():
                self.tree.insert("", "end", values=row)
            db.close()
        except Exception as e:
            messagebox.showerror("Error", f"Gagal mengambil data mahasiswa: {e}")

    def tambah_data(self):
        nim = self.entry_nim.get()
        nama = self.entry_nama.get()
        if not nim or not nama:
            messagebox.showwarning("Warning", "NIM dan Nama Wajib diisi!")
            return
        try:
            db = connect_db()
            cursor = db.cursor()
            sql = "INSERT INTO mahasiswa VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (nim, nama, self.combo_jk.get(), self.entry_tgl.get(), self.entry_tmpt.get(),
                   self.entry_alamat.get(), self.entry_tlp.get(), self.entry_email.get(),
                   self.entry_jurusan.get(), self.entry_angkatan.get(), self.combo_status.get())
            cursor.execute(sql, val)
            db.commit()
            db.close()
            messagebox.showinfo("Sukses", "Data Mahasiswa berhasil ditambahkan!")
            self.clear_fields()
            self.load_data()
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menambah data: {e}")

    def edit_data(self):
        if not self.tree.selection():
            messagebox.showwarning("Warning", "Pilih data di tabel yang ingin diubah!")
            return
        try:
            db = connect_db()
            cursor = db.cursor()
            sql = """UPDATE mahasiswa SET nama_lengkap=%s, jenis_kelamin=%s, tanggal_lahir=%s, 
                     tempat_lahir=%s, alamat=%s, no_telepon=%s, email=%s, jurusan=%s, 
                     angkatan=%s, status=%s WHERE nim=%s"""
            val = (self.entry_nama.get(), self.combo_jk.get(), self.entry_tgl.get(),
                   self.entry_tmpt.get(), self.entry_alamat.get(), self.entry_tlp.get(),
                   self.entry_email.get(), self.entry_jurusan.get(), self.entry_angkatan.get(),
                   self.combo_status.get(), self.entry_nim.get())
            cursor.execute(sql, val)
            db.commit()
            db.close()
            messagebox.showinfo("Sukses", "Data mahasiswa berhasil diperbarui!")
            self.clear_fields()
            self.load_data()
        except Exception as e:
            messagebox.showerror("Error", f"Gagal memperbarui data: {e}")

    def hapus_data(self):
        if not self.tree.selection():
            messagebox.showwarning("Warning", "Pilih data di tabel!")
            return
        nim = self.entry_nim.get()
        if messagebox.askyesno("Konfirmasi", f"Yakin hapus mahasiswa NIM {nim}?"):
            try:
                db = connect_db()
                cursor = db.cursor()
                cursor.execute("DELETE FROM mahasiswa WHERE nim = %s", (nim,))
                db.commit()
                db.close()
                messagebox.showinfo("Sukses", "Data berhasil dihapus!")
                self.clear_fields()
                self.load_data()
            except Exception as e:
                messagebox.showerror("Error", f"Gagal menghapus data: {e}")

    def select_item(self, event):
        selected = self.tree.selection()
        if selected:
            values = self.tree.item(selected[0], "values")
            self.clear_fields()
            self.entry_nim.insert(0, values[0])
            self.entry_nama.insert(0, values[1])
            self.combo_jk.set(values[2])
            self.entry_tgl.insert(0, values[3])
            self.entry_tmpt.insert(0, values[4])
            self.entry_alamat.insert(0, values[5])
            self.entry_tlp.insert(0, values[6])
            self.entry_email.insert(0, values[7])
            self.entry_jurusan.insert(0, values[8])
            self.entry_angkatan.insert(0, values[9])
            self.combo_status.set(values[10])

    def clear_fields(self):
        self.entry_nim.delete(0, tk.END)
        self.entry_nama.delete(0, tk.END)
        self.combo_jk.set("")
        self.entry_tgl.delete(0, tk.END)
        self.entry_tmpt.delete(0, tk.END)
        self.entry_alamat.delete(0, tk.END)
        self.entry_tlp.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)
        self.entry_jurusan.delete(0, tk.END)
        self.entry_angkatan.delete(0, tk.END)
        self.combo_status.set("")


# --- TAB MATA KULIAH ---
class TabMataKuliah(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        frame_form = tk.LabelFrame(self, text=" Form Mata Kuliah ", font=("Segoe UI", 10, "bold"), padx=12, pady=10, bg="#FFFFFF")
        frame_form.pack(fill="x", padx=15, pady=10)

        labels = ["Kode MK", "Nama MK", "SKS", "Semester", "NIP Dosen Pengampu"]
        for i, label_text in enumerate(labels):
            tk.Label(frame_form, text=label_text, font=("Segoe UI", 9), bg="#FFFFFF").grid(row=i//2, column=(i%2)*2, sticky="w", padx=5, pady=4)

        self.entry_kode = tk.Entry(frame_form, font=("Segoe UI", 9))
        self.entry_kode.grid(row=0, column=1, padx=5, pady=4, sticky="ew")

        self.entry_nama = tk.Entry(frame_form, font=("Segoe UI", 9))
        self.entry_nama.grid(row=0, column=3, padx=5, pady=4, sticky="ew")

        self.entry_sks = tk.Entry(frame_form, font=("Segoe UI", 9))
        self.entry_sks.grid(row=1, column=1, padx=5, pady=4, sticky="ew")

        self.entry_smt = tk.Entry(frame_form, font=("Segoe UI", 9))
        self.entry_smt.grid(row=1, column=3, padx=5, pady=4, sticky="ew")

        self.entry_nip = tk.Entry(frame_form, font=("Segoe UI", 9))
        self.entry_nip.grid(row=2, column=1, padx=5, pady=4, sticky="ew")

        frame_form.grid_columnconfigure(1, weight=1)
        frame_form.grid_columnconfigure(3, weight=1)

        frame_btn = tk.Frame(self, bg="#F8FAFC")
        frame_btn.pack(fill="x", padx=15, pady=5)

        btn_add = tk.Button(frame_btn, text="Tambah", bg="#10B981", fg="white", font=("Segoe UI", 9, "bold"), bd=0, padx=15, pady=5, cursor="hand2", command=self.tambah_data)
        btn_add.pack(side="left", padx=5)
        make_hover(btn_add, "#10B981", "#059669")

        btn_edit = tk.Button(frame_btn, text="Edit", bg="#3B82F6", fg="white", font=("Segoe UI", 9, "bold"), bd=0, padx=15, pady=5, cursor="hand2", command=self.edit_data)
        btn_edit.pack(side="left", padx=5)
        make_hover(btn_edit, "#3B82F6", "#2563EB")

        btn_del = tk.Button(frame_btn, text="Hapus", bg="#EF4444", fg="white", font=("Segoe UI", 9, "bold"), bd=0, padx=15, pady=5, cursor="hand2", command=self.hapus_data)
        btn_del.pack(side="left", padx=5)
        make_hover(btn_del, "#EF4444", "#DC2626")

        btn_clr = tk.Button(frame_btn, text="Clear", bg="#64748B", fg="white", font=("Segoe UI", 9, "bold"), bd=0, padx=15, pady=5, cursor="hand2", command=self.clear_fields)
        btn_clr.pack(side="left", padx=5)
        make_hover(btn_clr, "#64748B", "#475569")

        frame_table = tk.Frame(self, bg="#FFFFFF")
        frame_table.pack(fill="both", expand=True, padx=15, pady=10)

        columns = ("kode_mk", "nama_mk", "sks", "semester", "nip_dosen")
        self.tree = ttk.Treeview(frame_table, columns=columns, show="headings")

        headers = ["Kode MK", "Nama Mata Kuliah", "SKS", "Semester", "NIP Dosen"]
        for col, head in zip(columns, headers):
            self.tree.heading(col, text=head)
            self.tree.column(col, width=130)

        self.tree.bind("<<TreeviewSelect>>", self.select_item)

        scrollbar = ttk.Scrollbar(frame_table, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def load_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        try:
            db = connect_db()
            cursor = db.cursor()
            cursor.execute("SELECT * FROM mata_kuliah")
            for row in cursor.fetchall():
                self.tree.insert("", "end", values=row)
            db.close()
        except Exception as e:
            messagebox.showerror("Error", f"Gagal mengambil data mata kuliah: {e}")

    def tambah_data(self):
        kode = self.entry_kode.get()
        if not kode:
            messagebox.showwarning("Warning", "Kode MK wajib diisi!")
            return
        try:
            db = connect_db()
            cursor = db.cursor()
            sql = "INSERT INTO mata_kuliah VALUES (%s, %s, %s, %s, %s)"
            val = (kode, self.entry_nama.get(), self.entry_sks.get(), self.entry_smt.get(), self.entry_nip.get())
            cursor.execute(sql, val)
            db.commit()
            db.close()
            messagebox.showinfo("Sukses", "Mata Kuliah berhasil ditambahkan!")
            self.clear_fields()
            self.load_data()
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menambah data: {e}")

    def edit_data(self):
        if not self.tree.selection():
            messagebox.showwarning("Warning", "Pilih data di tabel!")
            return
        try:
            db = connect_db()
            cursor = db.cursor()
            sql = "UPDATE mata_kuliah SET nama_mk=%s, sks=%s, semester=%s, nip_dosen=%s WHERE kode_mk=%s"
            val = (self.entry_nama.get(), self.entry_sks.get(), self.entry_smt.get(), self.entry_nip.get(), self.entry_kode.get())
            cursor.execute(sql, val)
            db.commit()
            db.close()
            messagebox.showinfo("Sukses", "Data Mata Kuliah diperbarui!")
            self.clear_fields()
            self.load_data()
        except Exception as e:
            messagebox.showerror("Error", f"Gagal memperbarui data: {e}")

    def hapus_data(self):
        if not self.tree.selection():
            messagebox.showwarning("Warning", "Pilih data di tabel!")
            return
        kode = self.entry_kode.get()
        if messagebox.askyesno("Konfirmasi", f"Yakin hapus MK {kode}?"):
            try:
                db = connect_db()
                cursor = db.cursor()
                cursor.execute("DELETE FROM mata_kuliah WHERE kode_mk = %s", (kode,))
                db.commit()
                db.close()
                messagebox.showinfo("Sukses", "Data berhasil dihapus!")
                self.clear_fields()
                self.load_data()
            except Exception as e:
                messagebox.showerror("Error", f"Gagal menghapus data: {e}")

    def select_item(self, event):
        selected = self.tree.selection()
        if selected:
            values = self.tree.item(selected[0], "values")
            self.clear_fields()
            self.entry_kode.insert(0, values[0])
            self.entry_nama.insert(0, values[1])
            self.entry_sks.insert(0, values[2])
            self.entry_smt.insert(0, values[3])
            self.entry_nip.insert(0, values[4])

    def clear_fields(self):
        self.entry_kode.delete(0, tk.END)
        self.entry_nama.delete(0, tk.END)
        self.entry_sks.delete(0, tk.END)
        self.entry_smt.delete(0, tk.END)
        self.entry_nip.delete(0, tk.END)


# --- TAB JADWAL KULIAH ---
class TabJadwal(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        frame_form = tk.LabelFrame(self, text=" Form Jadwal Kuliah ", font=("Segoe UI", 10, "bold"), padx=12, pady=10, bg="#FFFFFF")
        frame_form.pack(fill="x", padx=15, pady=10)

        labels = ["ID Jadwal", "Kode MK", "Hari", "Jam Mulai", "Jam Selesai", "Ruangan"]
        for i, label_text in enumerate(labels):
            tk.Label(frame_form, text=label_text, font=("Segoe UI", 9), bg="#FFFFFF").grid(row=i//2, column=(i%2)*2, sticky="w", padx=5, pady=4)

        self.entry_id = tk.Entry(frame_form, font=("Segoe UI", 9))
        self.entry_id.grid(row=0, column=1, padx=5, pady=4, sticky="ew")

        self.entry_kodemk = tk.Entry(frame_form, font=("Segoe UI", 9))
        self.entry_kodemk.grid(row=0, column=3, padx=5, pady=4, sticky="ew")

        self.combo_hari = ttk.Combobox(frame_form, values=["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"], state="readonly", font=("Segoe UI", 9))
        self.combo_hari.grid(row=1, column=1, padx=5, pady=4, sticky="ew")

        self.entry_jammulai = tk.Entry(frame_form, font=("Segoe UI", 9))
        self.entry_jammulai.grid(row=1, column=3, padx=5, pady=4, sticky="ew")

        self.entry_jamselesai = tk.Entry(frame_form, font=("Segoe UI", 9))
        self.entry_jamselesai.grid(row=2, column=1, padx=5, pady=4, sticky="ew")

        self.entry_ruangan = tk.Entry(frame_form, font=("Segoe UI", 9))
        self.entry_ruangan.grid(row=2, column=3, padx=5, pady=4, sticky="ew")

        frame_form.grid_columnconfigure(1, weight=1)
        frame_form.grid_columnconfigure(3, weight=1)

        frame_btn = tk.Frame(self, bg="#F8FAFC")
        frame_btn.pack(fill="x", padx=15, pady=5)

        btn_add = tk.Button(frame_btn, text="Tambah", bg="#10B981", fg="white", font=("Segoe UI", 9, "bold"), bd=0, padx=15, pady=5, cursor="hand2", command=self.tambah_data)
        btn_add.pack(side="left", padx=5)
        make_hover(btn_add, "#10B981", "#059669")

        btn_edit = tk.Button(frame_btn, text="Edit", bg="#3B82F6", fg="white", font=("Segoe UI", 9, "bold"), bd=0, padx=15, pady=5, cursor="hand2", command=self.edit_data)
        btn_edit.pack(side="left", padx=5)
        make_hover(btn_edit, "#3B82F6", "#2563EB")

        btn_del = tk.Button(frame_btn, text="Hapus", bg="#EF4444", fg="white", font=("Segoe UI", 9, "bold"), bd=0, padx=15, pady=5, cursor="hand2", command=self.hapus_data)
        btn_del.pack(side="left", padx=5)
        make_hover(btn_del, "#EF4444", "#DC2626")

        btn_clr = tk.Button(frame_btn, text="Clear", bg="#64748B", fg="white", font=("Segoe UI", 9, "bold"), bd=0, padx=15, pady=5, cursor="hand2", command=self.clear_fields)
        btn_clr.pack(side="left", padx=5)
        make_hover(btn_clr, "#64748B", "#475569")

        frame_table = tk.Frame(self, bg="#FFFFFF")
        frame_table.pack(fill="both", expand=True, padx=15, pady=10)

        columns = ("id_jadwal", "kode_mk", "hari", "jam_mulai", "jam_selesai", "ruangan")
        self.tree = ttk.Treeview(frame_table, columns=columns, show="headings")

        headers = ["ID Jadwal", "Kode MK", "Hari", "Jam Mulai", "Jam Selesai", "Ruangan"]
        for col, head in zip(columns, headers):
            self.tree.heading(col, text=head)
            self.tree.column(col, width=120)

        self.tree.bind("<<TreeviewSelect>>", self.select_item)

        scrollbar = ttk.Scrollbar(frame_table, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def load_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        try:
            db = connect_db()
            cursor = db.cursor()
            cursor.execute("SELECT * FROM jadwal_kuliah")
            for row in cursor.fetchall():
                self.tree.insert("", "end", values=row)
            db.close()
        except Exception as e:
            messagebox.showerror("Error", f"Gagal mengambil data jadwal: {e}")

    def tambah_data(self):
        id_j = self.entry_id.get()
        if not id_j:
            messagebox.showwarning("Warning", "ID Jadwal wajib diisi!")
            return
        try:
            db = connect_db()
            cursor = db.cursor()
            sql = "INSERT INTO jadwal_kuliah VALUES (%s, %s, %s, %s, %s, %s)"
            val = (id_j, self.entry_kodemk.get(), self.combo_hari.get(), self.entry_jammulai.get(), self.entry_jamselesai.get(), self.entry_ruangan.get())
            cursor.execute(sql, val)
            db.commit()
            db.close()
            messagebox.showinfo("Sukses", "Data Jadwal berhasil ditambahkan!")
            self.clear_fields()
            self.load_data()
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menambah data: {e}")

    def edit_data(self):
        if not self.tree.selection():
            messagebox.showwarning("Warning", "Pilih data di tabel!")
            return
        try:
            db = connect_db()
            cursor = db.cursor()
            sql = """UPDATE jadwal_kuliah SET kode_mk=%s, hari=%s, jam_mulai=%s, 
                     jam_selesai=%s, ruangan=%s WHERE id_jadwal=%s"""
            val = (self.entry_kodemk.get(), self.combo_hari.get(), self.entry_jammulai.get(), self.entry_jamselesai.get(), self.entry_ruangan.get(), self.entry_id.get())
            cursor.execute(sql, val)
            db.commit()
            db.close()
            messagebox.showinfo("Sukses", "Data berhasil diperbarui!")
            self.clear_fields()
            self.load_data()
        except Exception as e:
            messagebox.showerror("Error", f"Gagal memperbarui data: {e}")

    def hapus_data(self):
        if not self.tree.selection():
            messagebox.showwarning("Warning", "Pilih data di tabel!")
            return
        id_j = self.entry_id.get()
        if messagebox.askyesno("Konfirmasi", f"Yakin hapus ID Jadwal {id_j}?"):
            try:
                db = connect_db()
                cursor = db.cursor()
                cursor.execute("DELETE FROM jadwal_kuliah WHERE id_jadwal = %s", (id_j,))
                db.commit()
                db.close()
                messagebox.showinfo("Sukses", "Data berhasil dihapus!")
                self.clear_fields()
                self.load_data()
            except Exception as e:
                messagebox.showerror("Error", f"Gagal menghapus data: {e}")

    def select_item(self, event):
        selected = self.tree.selection()
        if selected:
            values = self.tree.item(selected[0], "values")
            self.clear_fields()
            self.entry_id.insert(0, values[0])
            self.entry_kodemk.insert(0, values[1])
            self.combo_hari.set(values[2])
            self.entry_jammulai.insert(0, values[3])
            self.entry_jamselesai.insert(0, values[4])
            self.entry_ruangan.insert(0, values[5])

    def clear_fields(self):
        self.entry_id.delete(0, tk.END)
        self.entry_kodemk.delete(0, tk.END)
        self.combo_hari.set("")
        self.entry_jammulai.delete(0, tk.END)
        self.entry_jamselesai.delete(0, tk.END)
        self.entry_ruangan.delete(0, tk.END)


# --- TAB KRS ---
class TabKRS(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        frame_form = tk.LabelFrame(self, text=" Form Kartu Rencana Studi (KRS) ", font=("Segoe UI", 10, "bold"), padx=12, pady=10, bg="#FFFFFF")
        frame_form.pack(fill="x", padx=15, pady=10)

        labels = ["ID KRS", "NIM", "Kode MK", "Semester Ambil", "Tahun Ajaran", "Nilai Huruf", "Nilai Angka"]
        for i, label_text in enumerate(labels):
            tk.Label(frame_form, text=label_text, font=("Segoe UI", 9), bg="#FFFFFF").grid(row=i//2, column=(i%2)*2, sticky="w", padx=5, pady=4)

        self.entry_id = tk.Entry(frame_form, font=("Segoe UI", 9))
        self.entry_id.grid(row=0, column=1, padx=5, pady=4, sticky="ew")

        self.entry_nim = tk.Entry(frame_form, font=("Segoe UI", 9))
        self.entry_nim.grid(row=0, column=3, padx=5, pady=4, sticky="ew")

        self.entry_kodemk = tk.Entry(frame_form, font=("Segoe UI", 9))
        self.entry_kodemk.grid(row=1, column=1, padx=5, pady=4, sticky="ew")

        self.entry_smt = tk.Entry(frame_form, font=("Segoe UI", 9))
        self.entry_smt.grid(row=1, column=3, padx=5, pady=4, sticky="ew")

        self.entry_thn = tk.Entry(frame_form, font=("Segoe UI", 9))
        self.entry_thn.grid(row=2, column=1, padx=5, pady=4, sticky="ew")

        self.combo_huruf = ttk.Combobox(frame_form, values=["A", "A-", "B+", "B", "B-", "C+", "C", "D", "E"], state="readonly", font=("Segoe UI", 9))
        self.combo_huruf.grid(row=2, column=3, padx=5, pady=4, sticky="ew")

        self.entry_angka = tk.Entry(frame_form, font=("Segoe UI", 9))
        self.entry_angka.grid(row=3, column=1, padx=5, pady=4, sticky="ew")

        frame_form.grid_columnconfigure(1, weight=1)
        frame_form.grid_columnconfigure(3, weight=1)

        frame_btn = tk.Frame(self, bg="#F8FAFC")
        frame_btn.pack(fill="x", padx=15, pady=5)

        btn_add = tk.Button(frame_btn, text="Tambah", bg="#10B981", fg="white", font=("Segoe UI", 9, "bold"), bd=0, padx=15, pady=5, cursor="hand2", command=self.tambah_data)
        btn_add.pack(side="left", padx=5)
        make_hover(btn_add, "#10B981", "#059669")

        btn_edit = tk.Button(frame_btn, text="Edit", bg="#3B82F6", fg="white", font=("Segoe UI", 9, "bold"), bd=0, padx=15, pady=5, cursor="hand2", command=self.edit_data)
        btn_edit.pack(side="left", padx=5)
        make_hover(btn_edit, "#3B82F6", "#2563EB")

        btn_del = tk.Button(frame_btn, text="Hapus", bg="#EF4444", fg="white", font=("Segoe UI", 9, "bold"), bd=0, padx=15, pady=5, cursor="hand2", command=self.hapus_data)
        btn_del.pack(side="left", padx=5)
        make_hover(btn_del, "#EF4444", "#DC2626")

        btn_clr = tk.Button(frame_btn, text="Clear", bg="#64748B", fg="white", font=("Segoe UI", 9, "bold"), bd=0, padx=15, pady=5, cursor="hand2", command=self.clear_fields)
        btn_clr.pack(side="left", padx=5)
        make_hover(btn_clr, "#64748B", "#475569")

        frame_table = tk.Frame(self, bg="#FFFFFF")
        frame_table.pack(fill="both", expand=True, padx=15, pady=10)

        columns = ("id_krs", "nim", "kode_mk", "semester_ambil", "tahun_ajaran", "nilai_huruf", "nilai_angka")
        self.tree = ttk.Treeview(frame_table, columns=columns, show="headings")

        headers = ["ID KRS", "NIM", "Kode MK", "Semester", "Tahun Ajaran", "Nilai Huruf", "Nilai Angka"]
        for col, head in zip(columns, headers):
            self.tree.heading(col, text=head)
            self.tree.column(col, width=110)

        self.tree.bind("<<TreeviewSelect>>", self.select_item)

        scrollbar = ttk.Scrollbar(frame_table, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def load_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        try:
            db = connect_db()
            cursor = db.cursor()
            cursor.execute("SELECT * FROM krs")
            for row in cursor.fetchall():
                self.tree.insert("", "end", values=row)
            db.close()
        except Exception as e:
            messagebox.showerror("Error", f"Gagal mengambil data KRS: {e}")

    def tambah_data(self):
        id_krs = self.entry_id.get()
        if not id_krs:
            messagebox.showwarning("Warning", "ID KRS wajib diisi!")
            return
        try:
            db = connect_db()
            cursor = db.cursor()
            sql = "INSERT INTO krs VALUES (%s, %s, %s, %s, %s, %s, %s)"
            val = (id_krs, self.entry_nim.get(), self.entry_kodemk.get(), self.entry_smt.get(), self.entry_thn.get(), self.combo_huruf.get(), self.entry_angka.get())
            cursor.execute(sql, val)
            db.commit()
            db.close()
            messagebox.showinfo("Sukses", "Data KRS berhasil ditambahkan!")
            self.clear_fields()
            self.load_data()
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menambah data: {e}")

    def edit_data(self):
        if not self.tree.selection():
            messagebox.showwarning("Warning", "Pilih data di tabel!")
            return
        try:
            db = connect_db()
            cursor = db.cursor()
            sql = """UPDATE krs SET nim=%s, kode_mk=%s, semester_ambil=%s, 
                     tahun_ajaran=%s, nilai_huruf=%s, nilai_angka=%s WHERE id_krs=%s"""
            val = (self.entry_nim.get(), self.entry_kodemk.get(), self.entry_smt.get(), self.entry_thn.get(), self.combo_huruf.get(), self.entry_angka.get(), self.entry_id.get())
            cursor.execute(sql, val)
            db.commit()
            db.close()
            messagebox.showinfo("Sukses", "Data KRS diperbarui!")
            self.clear_fields()
            self.load_data()
        except Exception as e:
            messagebox.showerror("Error", f"Gagal memperbarui data: {e}")

    def hapus_data(self):
        if not self.tree.selection():
            messagebox.showwarning("Warning", "Pilih data di tabel!")
            return
        id_krs = self.entry_id.get()
        if messagebox.askyesno("Konfirmasi", f"Yakin hapus ID KRS {id_krs}?"):
            try:
                db = connect_db()
                cursor = db.cursor()
                cursor.execute("DELETE FROM krs WHERE id_krs = %s", (id_krs,))
                db.commit()
                db.close()
                messagebox.showinfo("Sukses", "Data berhasil dihapus!")
                self.clear_fields()
                self.load_data()
            except Exception as e:
                messagebox.showerror("Error", f"Gagal menghapus data: {e}")

    def select_item(self, event):
        selected = self.tree.selection()
        if selected:
            values = self.tree.item(selected[0], "values")
            self.clear_fields()
            self.entry_id.insert(0, values[0])
            self.entry_nim.insert(0, values[1])
            self.entry_kodemk.insert(0, values[2])
            self.entry_smt.insert(0, values[3])
            self.entry_thn.insert(0, values[4])
            self.combo_huruf.set(values[5])
            self.entry_angka.insert(0, values[6])

    def clear_fields(self):
        self.entry_id.delete(0, tk.END)
        self.entry_nim.delete(0, tk.END)
        self.entry_kodemk.delete(0, tk.END)
        self.entry_smt.delete(0, tk.END)
        self.entry_thn.delete(0, tk.END)
        self.combo_huruf.set("")
        self.entry_angka.delete(0, tk.END)


# --- TAB PEMBAYARAN UKT ---
class TabPembayaranUKT(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        frame_form = tk.LabelFrame(self, text=" Form Pembayaran UKT ", font=("Segoe UI", 10, "bold"), padx=12, pady=10, bg="#FFFFFF")
        frame_form.pack(fill="x", padx=15, pady=10)

        labels = ["ID Pembayaran", "NIM", "Semester", "Tahun Ajaran", "Jumlah Bayar", "Tgl Bayar (YYYY-MM-DD)", "Metode Pembayaran", "Status"]
        for i, label_text in enumerate(labels):
            tk.Label(frame_form, text=label_text, font=("Segoe UI", 9), bg="#FFFFFF").grid(row=i//2, column=(i%2)*2, sticky="w", padx=5, pady=4)

        self.entry_id = tk.Entry(frame_form, font=("Segoe UI", 9))
        self.entry_id.grid(row=0, column=1, padx=5, pady=4, sticky="ew")

        self.entry_nim = tk.Entry(frame_form, font=("Segoe UI", 9))
        self.entry_nim.grid(row=0, column=3, padx=5, pady=4, sticky="ew")

        self.entry_smt = tk.Entry(frame_form, font=("Segoe UI", 9))
        self.entry_smt.grid(row=1, column=1, padx=5, pady=4, sticky="ew")

        self.entry_thn = tk.Entry(frame_form, font=("Segoe UI", 9))
        self.entry_thn.grid(row=1, column=3, padx=5, pady=4, sticky="ew")

        self.entry_jumlah = tk.Entry(frame_form, font=("Segoe UI", 9))
        self.entry_jumlah.grid(row=2, column=1, padx=5, pady=4, sticky="ew")

        self.entry_tgl = tk.Entry(frame_form, font=("Segoe UI", 9))
        self.entry_tgl.grid(row=2, column=3, padx=5, pady=4, sticky="ew")

        self.combo_metode = ttk.Combobox(frame_form, values=["Transfer Bank", "Virtual Account", "Tunai"], state="readonly", font=("Segoe UI", 9))
        self.combo_metode.grid(row=3, column=1, padx=5, pady=4, sticky="ew")

        self.combo_status = ttk.Combobox(frame_form, values=["Lunas", "Belum Lunas"], state="readonly", font=("Segoe UI", 9))
        self.combo_status.grid(row=3, column=3, padx=5, pady=4, sticky="ew")

        frame_form.grid_columnconfigure(1, weight=1)
        frame_form.grid_columnconfigure(3, weight=1)

        frame_btn = tk.Frame(self, bg="#F8FAFC")
        frame_btn.pack(fill="x", padx=15, pady=5)

        btn_add = tk.Button(frame_btn, text="Tambah", bg="#10B981", fg="white", font=("Segoe UI", 9, "bold"), bd=0, padx=15, pady=5, cursor="hand2", command=self.tambah_data)
        btn_add.pack(side="left", padx=5)
        make_hover(btn_add, "#10B981", "#059669")

        btn_edit = tk.Button(frame_btn, text="Edit", bg="#3B82F6", fg="white", font=("Segoe UI", 9, "bold"), bd=0, padx=15, pady=5, cursor="hand2", command=self.edit_data)
        btn_edit.pack(side="left", padx=5)
        make_hover(btn_edit, "#3B82F6", "#2563EB")

        btn_del = tk.Button(frame_btn, text="Hapus", bg="#EF4444", fg="white", font=("Segoe UI", 9, "bold"), bd=0, padx=15, pady=5, cursor="hand2", command=self.hapus_data)
        btn_del.pack(side="left", padx=5)
        make_hover(btn_del, "#EF4444", "#DC2626")

        btn_clr = tk.Button(frame_btn, text="Clear", bg="#64748B", fg="white", font=("Segoe UI", 9, "bold"), bd=0, padx=15, pady=5, cursor="hand2", command=self.clear_fields)
        btn_clr.pack(side="left", padx=5)
        make_hover(btn_clr, "#64748B", "#475569")

        frame_table = tk.Frame(self, bg="#FFFFFF")
        frame_table.pack(fill="both", expand=True, padx=15, pady=10)

        columns = ("id_pembayaran", "nim", "semester", "tahun_ajaran", "jumlah_bayar", "tanggal_bayar", "metode_pembayaran", "status")
        self.tree = ttk.Treeview(frame_table, columns=columns, show="headings")

        headers = ["ID Bayar", "NIM", "Semester", "Tahun Ajaran", "Jumlah Bayar", "Tanggal Bayar", "Metode", "Status"]
        for col, head in zip(columns, headers):
            self.tree.heading(col, text=head)
            self.tree.column(col, width=110)

        self.tree.bind("<<TreeviewSelect>>", self.select_item)

        scrollbar = ttk.Scrollbar(frame_table, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def load_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        try:
            db = connect_db()
            cursor = db.cursor()
            cursor.execute("SELECT * FROM pembayaran_ukt")
            for row in cursor.fetchall():
                self.tree.insert("", "end", values=row)
            db.close()
        except Exception as e:
            messagebox.showerror("Error", f"Gagal mengambil data pembayaran UKT: {e}")

    def tambah_data(self):
        id_p = self.entry_id.get()
        if not id_p:
            messagebox.showwarning("Warning", "ID Pembayaran wajib diisi!")
            return
        try:
            db = connect_db()
            cursor = db.cursor()
            sql = "INSERT INTO pembayaran_ukt VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            val = (id_p, self.entry_nim.get(), self.entry_smt.get(), self.entry_thn.get(),
                   self.entry_jumlah.get(), self.entry_tgl.get() or None,
                   self.combo_metode.get() or None, self.combo_status.get())
            cursor.execute(sql, val)
            db.commit()
            db.close()
            messagebox.showinfo("Sukses", "Data Pembayaran UKT berhasil ditambahkan!")
            self.clear_fields()
            self.load_data()
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menambah data: {e}")

    def edit_data(self):
        if not self.tree.selection():
            messagebox.showwarning("Warning", "Pilih data di tabel!")
            return
        try:
            db = connect_db()
            cursor = db.cursor()
            sql = """UPDATE pembayaran_ukt SET nim=%s, semester=%s, tahun_ajaran=%s, 
                     jumlah_bayar=%s, tanggal_bayar=%s, metode_pembayaran=%s, status=%s WHERE id_pembayaran=%s"""
            val = (self.entry_nim.get(), self.entry_smt.get(), self.entry_thn.get(),
                   self.entry_jumlah.get(), self.entry_tgl.get() or None,
                   self.combo_metode.get() or None, self.combo_status.get(), self.entry_id.get())
            cursor.execute(sql, val)
            db.commit()
            db.close()
            messagebox.showinfo("Sukses", "Data Pembayaran UKT diperbarui!")
            self.clear_fields()
            self.load_data()
        except Exception as e:
            messagebox.showerror("Error", f"Gagal memperbarui data: {e}")

    def hapus_data(self):
        if not self.tree.selection():
            messagebox.showwarning("Warning", "Pilih data di tabel!")
            return
        id_p = self.entry_id.get()
        if messagebox.askyesno("Konfirmasi", f"Yakin hapus ID Pembayaran {id_p}?"):
            try:
                db = connect_db()
                cursor = db.cursor()
                cursor.execute("DELETE FROM pembayaran_ukt WHERE id_pembayaran = %s", (id_p,))
                db.commit()
                db.close()
                messagebox.showinfo("Sukses", "Data berhasil dihapus!")
                self.clear_fields()
                self.load_data()
            except Exception as e:
                messagebox.showerror("Error", f"Gagal menghapus data: {e}")

    def select_item(self, event):
        selected = self.tree.selection()
        if selected:
            values = self.tree.item(selected[0], "values")
            self.clear_fields()
            self.entry_id.insert(0, values[0])
            self.entry_nim.insert(0, values[1])
            self.entry_smt.insert(0, values[2])
            self.entry_thn.insert(0, values[3])
            self.entry_jumlah.insert(0, values[4])
            if values[5] and values[5] != "None":
                self.entry_tgl.insert(0, values[5])
            if values[6] and values[6] != "None":
                self.combo_metode.set(values[6])
            self.combo_status.set(values[7])

    def clear_fields(self):
        self.entry_id.delete(0, tk.END)
        self.entry_nim.delete(0, tk.END)
        self.entry_smt.delete(0, tk.END)
        self.entry_thn.delete(0, tk.END)
        self.entry_jumlah.delete(0, tk.END)
        self.entry_tgl.delete(0, tk.END)
        self.combo_metode.set("")
        self.combo_status.set("")


# ==========================================
# 3. APLIKASI DASHBOARD UTAMA
# ==========================================
class AplikasiSIAKAD(tk.Tk):
    def __init__(self, user, role):
        super().__init__()
        self.title("Sistem Informasi Akademik (SIAKAD)")
        self.geometry("1150x720")
        self.configure(bg="#F8FAFC")

        # Set Global Style untuk ttk Widgets
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TNotebook", background="#F8FAFC", borderwidth=0)
        style.configure("TNotebook.Tab", font=("Segoe UI", 10, "bold"), padding=[14, 8], background="#E2E8F0")
        style.map("TNotebook.Tab", background=[("selected", "#2563EB")], foreground=[("selected", "#FFFFFF")])
        
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), background="#F1F5F9", foreground="#1E293B")
        style.configure("Treeview", font=("Segoe UI", 9), rowheight=25)

        # Header Frame Utama
        header_frame = tk.Frame(self, bg="#1A237E", pady=8, padx=15)
        header_frame.pack(fill="x")

        # Label Informasi User
        lbl_welcome = tk.Label(
            header_frame, 
            text=f"DASHBOARD SIAKAD - [{role.upper()}: {user['nama']}]", 
            font=("Segoe UI", 13, "bold"), 
            bg="#1A237E", 
            fg="white"
        )
        lbl_welcome.pack(side="left", pady=5)

        # Tombol LOGOUT di Pojok Kanan Header
        btn_logout = tk.Button(
            header_frame,
            text=" Logout",
            font=("Segoe UI", 9, "bold"),
            bg="#DC2626",
            fg="white",
            activebackground="#B91C1C",
            activeforeground="white",
            bd=0,
            padx=12,
            pady=4,
            cursor="hand2",
            command=self.proses_logout
        )
        btn_logout.pack(side="right")
        make_hover(btn_logout, "#DC2626", "#B91C1C")

        # Container Tab (Notebook)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Inisialisasi Tab Modul
        self.tab_dosen = TabDosen(self.notebook)
        self.tab_mahasiswa = TabMahasiswa(self.notebook)
        self.tab_matakuliah = TabMataKuliah(self.notebook)
        self.tab_jadwal = TabJadwal(self.notebook)
        self.tab_krs = TabKRS(self.notebook)
        self.tab_ukt = TabPembayaranUKT(self.notebook)

        self.notebook.add(self.tab_dosen, text=" Data Dosen ")
        self.notebook.add(self.tab_mahasiswa, text=" Data Mahasiswa ")
        self.notebook.add(self.tab_matakuliah, text=" Mata Kuliah ")
        self.notebook.add(self.tab_jadwal, text=" Jadwal Kuliah ")
        self.notebook.add(self.tab_krs, text=" KRS ")
        self.notebook.add(self.tab_ukt, text=" Pembayaran UKT ")

    # Fungsi Logout & Kembali ke Form Login
    def proses_logout(self):
        confirm = messagebox.askyesno("Konfirmasi Logout", "Apakah Anda yakin ingin keluar dari sistem?")
        if confirm:
            self.destroy()  # Tutup Dashboard
            # Buka Kembali Jendela Login
            login_root = tk.Tk()
            LoginWindow(login_root)
            login_root.mainloop()


# Main Entry Point Program
if __name__ == "__main__":
    root = tk.Tk()
    app = LoginWindow(root)
    root.mainloop()