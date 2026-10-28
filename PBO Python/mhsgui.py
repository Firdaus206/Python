# Mengimpor modul os untuk interaksi sistem operasi jika diperlukan
import os
# Mengimpor modul tkinter dasar untuk pembuatan komponen GUI
import tkinter as tk
# Mengimpor modul ttk untuk widget bertema (seperti Combobox & Treeview) dan messagebox untuk dialog pop-up
from tkinter import ttk, messagebox
# Mengimpor mysql.connector untuk mengendalikan koneksi dan operasi database MySQL
import mysql.connector

# --- KONEKSI DATABASE ---
# Fungsi untuk membuat dan mengembalikan objek koneksi ke database MySQL
def connect_db():
    return mysql.connector.connect(
        host="localhost",      # Alamat host server MySQL
        user="root",           # Username untuk login ke MySQL
        password="",           # Password pengguna (kosongkan jika tidak ada password)
        database="siakad"      # Nama database yang dituju
    )

# --- FUNGSI CRUD ---
# Fungsi untuk memuat dan menampilkan seluruh data dari tabel database ke Treeview
def load_data():
    # Menghapus seluruh baris data lama yang ada di Treeview sebelum memuat data baru
    for row in tree.get_children():
        tree.delete(row)
    try:
        # Membuka koneksi ke database
        db = connect_db()
        # Membuat objek kursor untuk mengeksekusi query SQL
        cursor = db.cursor()
        # Mengeksekusi query untuk mengambil semua record dari tabel mahasiswa
        cursor.execute("SELECT * FROM mahasiswa")
        # Mengambil seluruh baris hasil query SQL
        rows = cursor.fetchall()
        # Memasukkan setiap baris data hasil query ke dalam komponen Treeview (tabel GUI)
        for row in rows:
            tree.insert("", "end", values=row)
        # Menutup koneksi database
        db.close()
    except Exception as e:
        # Menampilkan pop-up error jika terjadi kegagalan pengambilan data dari database
        messagebox.showerror("Database Error", f"Gagal mengambil data: {e}")

# Fungsi untuk menambahkan record mahasiswa baru ke database
def tambah_data():
    # Mengambil nilai teks dari masing-masing field form input
    nim = entry_nim.get()
    nama = entry_nama.get()
    jk = combo_jk.get()
    tgl_lahir = entry_tgl.get()
    tmpt_lahir = entry_tmpt.get()
    alamat = entry_alamat.get()
    tlp = entry_tlp.get()
    email = entry_email.get()
    jurusan = entry_jurusan.get()
    angkatan = entry_angkatan.get()
    status = combo_status.get()

    # Validasi input wajib (NIM dan Nama Lengkap tidak boleh kosong)
    if not nim or not nama:
        messagebox.showwarning("Warning", "NIM dan Nama Lengkap wajib diisi!")
        return

    try:
        # Membuka koneksi database
        db = connect_db()
        cursor = db.cursor()
        # Query SQL INSERT dengan placeholder (%s) untuk mencegah SQL Injection
        sql = """INSERT INTO mahasiswa (nim, nama_lengkap, jenis_kelamin, tanggal_lahir, 
                 tempat_lahir, alamat, no_telepon, email, jurusan, angkatan, status) 
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        # Tuple berisi kumpulan nilai variabel input
        val = (nim, nama, jk, tgl_lahir, tmpt_lahir, alamat, tlp, email, jurusan, angkatan, status)
        # Mengeksekusi query INSERT beserta nilainya
        cursor.execute(sql, val)
        # Menyimpan perubahan transaksi ke database secara permanen
        db.commit()
        # Menutup koneksi database
        db.close()
        # Menampilkan notifikasi sukses
        messagebox.showinfo("Sukses", "Data mahasiswa berhasil ditambahkan!")
        # Mengosongkan form input
        clear_fields()
        # Memperbarui tampilan data pada tabel Treeview
        load_data()
    except Exception as e:
        # Menampilkan pesan error jika query INSERT gagal dieksekusi
        messagebox.showerror("Error", f"Gagal menambah data: {e}")

# Fungsi untuk memperbarui (update) data mahasiswa yang dipilih
def edit_data():
    # Memeriksa baris mana yang sedang dipilih di Treeview
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Warning", "Pilih data di tabel yang ingin diubah!")
        return

    # Mengambil nilai terbaru dari masing-masing field form input
    nim = entry_nim.get()
    nama = entry_nama.get()
    jk = combo_jk.get()
    tgl_lahir = entry_tgl.get()
    tmpt_lahir = entry_tmpt.get()
    alamat = entry_alamat.get()
    tlp = entry_tlp.get()
    email = entry_email.get()
    jurusan = entry_jurusan.get()
    angkatan = entry_angkatan.get()
    status = combo_status.get()

    try:
        # Membuka koneksi database
        db = connect_db()
        cursor = db.cursor()
        # Query SQL UPDATE untuk mengubah data berdasarkan klausa WHERE nim
        sql = """UPDATE mahasiswa SET nama_lengkap=%s, jenis_kelamin=%s, tanggal_lahir=%s, 
                 tempat_lahir=%s, alamat=%s, no_telepon=%s, email=%s, jurusan=%s, 
                 angkatan=%s, status=%s WHERE nim=%s"""
        # Tuple nilai parameter query
        val = (nama, jk, tgl_lahir, tmpt_lahir, alamat, tlp, email, jurusan, angkatan, status, nim)
        # Mengeksekusi query UPDATE
        cursor.execute(sql, val)
        # Menyimpan perubahan transaksi secara permanen
        db.commit()
        # Menutup koneksi database
        db.close()
        # Menampilkan notifikasi sukses
        messagebox.showinfo("Sukses", "Data mahasiswa berhasil diperbarui!")
        # Mengosongkan form input dan merefresh tabel
        clear_fields()
        load_data()
    except Exception as e:
        # Menampilkan pop-up error jika terjadi kendala saat mengedit data
        messagebox.showerror("Error", f"Gagal memperbarui data: {e}")

# Fungsi untuk menghapus record mahasiswa dari database
def hapus_data():
    # Memeriksa apakah ada item tabel yang dipilih
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Warning", "Pilih data di tabel yang ingin dihapus!")
        return

    # Mengambil NIM dari input field sebagai acuan penghapusan
    nim = entry_nim.get()
    # Menampilkan dialog konfirmasi Ya/Tidak sebelum menghapus
    confirm = messagebox.askyesno("Konfirmasi", f"Yakin ingin menghapus mahasiswa NIM {nim}?")
    if confirm:
        try:
            # Membuka koneksi database
            db = connect_db()
            cursor = db.cursor()
            # Mengeksekusi query DELETE berdasarkan NIM
            cursor.execute("DELETE FROM mahasiswa WHERE nim = %s", (nim,))
            # Simpan perubahan secara permanen
            db.commit()
            # Menutup koneksi
            db.close()
            # Notifikasi sukses
            messagebox.showinfo("Sukses", "Data berhasil dihapus!")
            # Bersihkan form dan refresh tabel Treeview
            clear_fields()
            load_data()
        except Exception as e:
            # Notifikasi kegagalan hapus data
            messagebox.showerror("Error", f"Gagal menghapus data: {e}")

# Fungsi callback event saat salah satu baris pada tabel Treeview diklik/dipilih
def select_item(event):
    # Mendapatkan ID item baris yang dipilih
    selected = tree.selection()
    if selected:
        # Mengambil daftar nilai kolom dari baris yang dipilih
        values = tree.item(selected[0], "values")
        # Mengosongkan isian form sebelum diisi data baru
        clear_fields()
        # Memasukkan data kolom tabel ke masing-masing elemen input form
        entry_nim.insert(0, values[0])
        entry_nama.insert(0, values[1])
        combo_jk.set(values[2])
        entry_tgl.insert(0, values[3])
        entry_tmpt.insert(0, values[4])
        entry_alamat.insert(0, values[5])
        entry_tlp.insert(0, values[6])
        entry_email.insert(0, values[7])
        entry_jurusan.insert(0, values[8])
        entry_angkatan.insert(0, values[9])
        combo_status.set(values[10])

# Fungsi helper untuk menghapus/mengosongkan seluruh kotak input form
def clear_fields():
    entry_nim.delete(0, tk.END)
    entry_nama.delete(0, tk.END)
    combo_jk.set("")
    entry_tgl.delete(0, tk.END)
    entry_tmpt.delete(0, tk.END)
    entry_alamat.delete(0, tk.END)
    entry_tlp.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    entry_jurusan.delete(0, tk.END)
    entry_angkatan.delete(0, tk.END)
    combo_status.set("")

# --- GUI MAIN WINDOW ---
# Membuat objek jendela utama Tkinter
root = tk.Tk()
# Mengatur judul jendela aplikasi
root.title("Aplikasi Data Mahasiswa - SIAKAD")
# Mengatur dimensi ukuran jendela awal (lebar 1100px, tinggi 650px)
root.geometry("1100x650")

# Membuat frame bergaris tepi (LabelFrame) untuk mengelompokkan form input data
frame_form = tk.LabelFrame(root, text=" Form Data Mahasiswa ", padx=10, pady=10)
# Menampilkan frame form di bagian atas jendela yang memenuhi lebar secara horizontal
frame_form.pack(fill="x", padx=15, pady=10)

# Baris 0: NIM & Nama Lengkap
tk.Label(frame_form, text="NIM").grid(row=0, column=0, sticky="w", padx=5, pady=3)
entry_nim = tk.Entry(frame_form)
entry_nim.grid(row=0, column=1, padx=5, pady=3, sticky="ew")

tk.Label(frame_form, text="Nama Lengkap").grid(row=0, column=2, sticky="w", padx=5, pady=3)
entry_nama = tk.Entry(frame_form)
entry_nama.grid(row=0, column=3, padx=5, pady=3, sticky="ew")

# Baris 1: Jenis Kelamin & Tanggal Lahir
tk.Label(frame_form, text="Jenis Kelamin").grid(row=1, column=0, sticky="w", padx=5, pady=3)
combo_jk = ttk.Combobox(frame_form, values=["Laki-laki", "Perempuan"], state="readonly")
combo_jk.grid(row=1, column=1, padx=5, pady=3, sticky="ew")

tk.Label(frame_form, text="Tanggal Lahir (YYYY-MM-DD)").grid(row=1, column=2, sticky="w", padx=5, pady=3)
entry_tgl = tk.Entry(frame_form)
entry_tgl.grid(row=1, column=3, padx=5, pady=3, sticky="ew")

# Baris 2: Tempat Lahir & Alamat
tk.Label(frame_form, text="Tempat Lahir").grid(row=2, column=0, sticky="w", padx=5, pady=3)
entry_tmpt = tk.Entry(frame_form)
entry_tmpt.grid(row=2, column=1, padx=5, pady=3, sticky="ew")

tk.Label(frame_form, text="Alamat").grid(row=2, column=2, sticky="w", padx=5, pady=3)
entry_alamat = tk.Entry(frame_form)
entry_alamat.grid(row=2, column=3, padx=5, pady=3, sticky="ew")

# Baris 3: No Telepon & Email
tk.Label(frame_form, text="No Telepon").grid(row=3, column=0, sticky="w", padx=5, pady=3)
entry_tlp = tk.Entry(frame_form)
entry_tlp.grid(row=3, column=1, padx=5, pady=3, sticky="ew")

tk.Label(frame_form, text="Email").grid(row=3, column=2, sticky="w", padx=5, pady=3)
entry_email = tk.Entry(frame_form)
entry_email.grid(row=3, column=3, padx=5, pady=3, sticky="ew")

# Baris 4: Jurusan & Angkatan
tk.Label(frame_form, text="Jurusan").grid(row=4, column=0, sticky="w", padx=5, pady=3)
entry_jurusan = tk.Entry(frame_form)
entry_jurusan.grid(row=4, column=1, padx=5, pady=3, sticky="ew")

tk.Label(frame_form, text="Angkatan").grid(row=4, column=2, sticky="w", padx=5, pady=3)
entry_angkatan = tk.Entry(frame_form)
entry_angkatan.grid(row=4, column=3, padx=5, pady=3, sticky="ew")

# Baris 5: Status
tk.Label(frame_form, text="Status").grid(row=5, column=0, sticky="w", padx=5, pady=3)
combo_status = ttk.Combobox(frame_form, values=["Aktif", "Cuti", "Lulus", "Non-Aktif"], state="readonly")
combo_status.grid(row=5, column=1, padx=5, pady=3, sticky="ew")

# Konfigurasi tata letak grid agar kolom input bersifat responsif
frame_form.grid_columnconfigure(1, weight=1)
frame_form.grid_columnconfigure(3, weight=1)

# Membuat frame penampung tombol-tombol aksi CRUD
frame_btn = tk.Frame(root)
frame_btn.pack(fill="x", padx=15, pady=5)

# Membuat dan menampilkan tombol Tambah, Edit, Hapus, dan Clear
tk.Button(frame_btn, text="Tambah", bg="#4CAF50", fg="white", command=tambah_data, width=12).pack(side="left", padx=5)
tk.Button(frame_btn, text="Edit", bg="#2196F3", fg="white", command=edit_data, width=12).pack(side="left", padx=5)
tk.Button(frame_btn, text="Hapus", bg="#f44336", fg="white", command=hapus_data, width=12).pack(side="left", padx=5)
tk.Button(frame_btn, text="Clear", bg="#9E9E9E", fg="white", command=clear_fields, width=12).pack(side="left", padx=5)

# Membuat frame penampung komponen tabel (Treeview)
frame_table = tk.Frame(root)
frame_table.pack(fill="both", expand=True, padx=15, pady=10)

# Definisi nama identifier untuk setiap kolom tabel mahasiswa
columns = ("nim", "nama_lengkap", "jenis_kelamin", "tanggal_lahir", "tempat_lahir", 
           "alamat", "no_telepon", "email", "jurusan", "angkatan", "status")

# Membuat komponen Treeview untuk menampilkan struktur data tabular
tree = ttk.Treeview(frame_table, columns=columns, show="headings")

# Mengatur judul header yang tampil pada setiap kolom tabel
tree.heading("nim", text="NIM")
tree.heading("nama_lengkap", text="Nama Lengkap")
tree.heading("jenis_kelamin", text="Jenis Kelamin")
tree.heading("tanggal_lahir", text="Tgl Lahir")
tree.heading("tempat_lahir", text="Tempat Lahir")
tree.heading("alamat", text="Alamat")
tree.heading("no_telepon", text="No Telepon")
tree.heading("email", text="Email")
tree.heading("jurusan", text="Jurusan")
tree.heading("angkatan", text="Angkatan")
tree.heading("status", text="Status")

# Mengatur lebar relatif dari masing-masing kolom tabel
tree.column("nim", width=80)
tree.column("nama_lengkap", width=130)
tree.column("jenis_kelamin", width=90)
tree.column("tanggal_lahir", width=90)
tree.column("tempat_lahir", width=100)
tree.column("alamat", width=150)
tree.column("no_telepon", width=100)
tree.column("email", width=140)
tree.column("jurusan", width=120)
tree.column("angkatan", width=70)
tree.column("status", width=70)

# Mengikat event klik/pilih item pada Treeview dengan fungsi handler select_item
tree.bind("<<TreeviewSelect>>", select_item)

# Membuat scrollbar vertikal & horizontal dan menghubungkannya dengan komponen Treeview
scrollbar_v = ttk.Scrollbar(frame_table, orient="vertical", command=tree.yview)
scrollbar_h = ttk.Scrollbar(frame_table, orient="horizontal", command=tree.xview)
tree.configure(yscrollcommand=scrollbar_v.set, xscrollcommand=scrollbar_h.set)

# Menampilkan Treeview dan Scrollbar ke dalam frame tabel
scrollbar_v.pack(side="right", fill="y")
scrollbar_h.pack(side="bottom", fill="x")
tree.pack(side="left", fill="both", expand=True)

# Memanggil fungsi load_data() untuk menampilkan data awal saat aplikasi pertama kali dijalankan
load_data()

# Memulai loop utama peristiwa GUI Tkinter
root.mainloop()