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
        # Mengeksekusi query untuk mengambil semua record dari tabel jadwal_kuliah
        cursor.execute("SELECT * FROM jadwal_kuliah")
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

# Fungsi untuk menambahkan record jadwal kuliah baru ke database
def tambah_data():
    # Mengambil nilai teks dari masing-masing field form input
    id_jadwal = entry_id.get()
    kode_mk = entry_kodemk.get()
    hari = combo_hari.get()
    jam_mulai = entry_jammulai.get()
    jam_selesai = entry_jamselesai.get()
    ruangan = entry_ruangan.get()

    # Validasi input wajib (ID Jadwal dan Kode MK tidak boleh kosong)
    if not id_jadwal or not kode_mk:
        messagebox.showwarning("Warning", "ID Jadwal dan Kode MK wajib diisi!")
        return

    try:
        # Membuka koneksi database
        db = connect_db()
        cursor = db.cursor()
        # Query SQL INSERT dengan placeholder (%s) untuk mencegah SQL Injection
        sql = "INSERT INTO jadwal_kuliah (id_jadwal, kode_mk, hari, jam_mulai, jam_selesai, ruangan) VALUES (%s, %s, %s, %s, %s, %s)"
        # Tuple berisi kumpulan nilai variabel input
        val = (id_jadwal, kode_mk, hari, jam_mulai, jam_selesai, ruangan)
        # Mengeksekusi query INSERT beserta nilainya
        cursor.execute(sql, val)
        # Menyimpan perubahan transaksi ke database secara permanen
        db.commit()
        # Menutup koneksi database
        db.close()
        # Menampilkan notifikasi sukses
        messagebox.showinfo("Sukses", "Data jadwal berhasil ditambahkan!")
        # Mengosongkan form input
        clear_fields()
        # Memperbarui tampilan data pada tabel Treeview
        load_data()
    except Exception as e:
        # Menampilkan pesan error jika query INSERT gagal dieksekusi
        messagebox.showerror("Error", f"Gagal menambah data: {e}")

# Fungsi untuk memperbarui (update) data jadwal kuliah yang dipilih
def edit_data():
    # Memeriksa baris mana yang sedang dipilih di Treeview
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Warning", "Pilih data di tabel yang ingin diubah!")
        return

    # Mengambil nilai terbaru dari masing-masing field form input
    id_jadwal = entry_id.get()
    kode_mk = entry_kodemk.get()
    hari = combo_hari.get()
    jam_mulai = entry_jammulai.get()
    jam_selesai = entry_jamselesai.get()
    ruangan = entry_ruangan.get()

    try:
        # Membuka koneksi database
        db = connect_db()
        cursor = db.cursor()
        # Query SQL UPDATE untuk mengubah data berdasarkan klausa WHERE id_jadwal
        sql = """UPDATE jadwal_kuliah SET kode_mk=%s, hari=%s, jam_mulai=%s, 
                 jam_selesai=%s, ruangan=%s WHERE id_jadwal=%s"""
        # Tuple nilai parameter query
        val = (kode_mk, hari, jam_mulai, jam_selesai, ruangan, id_jadwal)
        # Mengeksekusi query UPDATE
        cursor.execute(sql, val)
        # Menyimpan perubahan transaksi secara permanen
        db.commit()
        # Menutup koneksi database
        db.close()
        # Menampilkan notifikasi sukses
        messagebox.showinfo("Sukses", "Data jadwal berhasil diperbarui!")
        # Mengosongkan form input dan merefresh tabel
        clear_fields()
        load_data()
    except Exception as e:
        # Menampilkan pop-up error jika terjadi kendala saat mengedit data
        messagebox.showerror("Error", f"Gagal memperbarui data: {e}")

# Fungsi untuk menghapus record jadwal kuliah dari database
def hapus_data():
    # Memeriksa apakah ada item tabel yang dipilih
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Warning", "Pilih data di tabel yang ingin dihapus!")
        return

    # Mengambil ID Jadwal dari input field sebagai acuan penghapusan
    id_jadwal = entry_id.get()
    # Menampilkan dialog konfirmasi Ya/Tidak sebelum menghapus
    confirm = messagebox.askyesno("Konfirmasi", f"Yakin ingin menghapus jadwal dengan ID {id_jadwal}?")
    if confirm:
        try:
            # Membuka koneksi database
            db = connect_db()
            cursor = db.cursor()
            # Mengeksekusi query DELETE berdasarkan ID Jadwal
            cursor.execute("DELETE FROM jadwal_kuliah WHERE id_jadwal = %s", (id_jadwal,))
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
        entry_id.insert(0, values[0])
        entry_kodemk.insert(0, values[1])
        combo_hari.set(values[2])
        entry_jammulai.insert(0, values[3])
        entry_jamselesai.insert(0, values[4])
        entry_ruangan.insert(0, values[5])

# Fungsi helper untuk menghapus/mengosongkan seluruh kotak input form
def clear_fields():
    entry_id.delete(0, tk.END)
    entry_kodemk.delete(0, tk.END)
    combo_hari.set("")
    entry_jammulai.delete(0, tk.END)
    entry_jamselesai.delete(0, tk.END)
    entry_ruangan.delete(0, tk.END)

# --- GUI MAIN WINDOW ---
# Membuat objek jendela utama Tkinter
root = tk.Tk()
# Mengatur judul jendela aplikasi
root.title("Aplikasi Jadwal Kuliah - SIAKAD")
# Mengatur dimensi ukuran jendela awal (lebar 850px, tinggi 520px)
root.geometry("850x520")

# Membuat frame bergaris tepi (LabelFrame) untuk mengelompokkan form input data
frame_form = tk.LabelFrame(root, text=" Form Jadwal Kuliah ", padx=10, pady=10)
# Menampilkan frame form di bagian atas jendela yang memenuhi lebar secara horizontal
frame_form.pack(fill="x", padx=15, pady=10)

# Daftar teks label untuk setiap field data jadwal kuliah
labels = ["ID Jadwal", "Kode MK", "Hari", "Jam Mulai", "Jam Selesai", "Ruangan"]
# Perulangan untuk membuat label teks secara dinamis menggunakan layout Grid 2 kolom
for i, label_text in enumerate(labels):
    tk.Label(frame_form, text=label_text).grid(row=i//2, column=(i%2)*2, sticky="w", padx=5, pady=3)

# Membuat elemen Entry untuk input ID Jadwal
entry_id = tk.Entry(frame_form)
entry_id.grid(row=0, column=1, padx=5, pady=3, sticky="ew")

# Membuat elemen Entry untuk input Kode MK
entry_kodemk = tk.Entry(frame_form)
entry_kodemk.grid(row=0, column=3, padx=5, pady=3, sticky="ew")

# Membuat elemen Combobox untuk opsi pilihan Hari
combo_hari = ttk.Combobox(frame_form, values=["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"], state="readonly")
combo_hari.grid(row=1, column=1, padx=5, pady=3, sticky="ew")

# Membuat elemen Entry untuk input Jam Mulai
entry_jammulai = tk.Entry(frame_form)
entry_jammulai.grid(row=1, column=3, padx=5, pady=3, sticky="ew")

# Membuat elemen Entry untuk input Jam Selesai
entry_jamselesai = tk.Entry(frame_form)
entry_jamselesai.grid(row=2, column=1, padx=5, pady=3, sticky="ew")

# Membuat elemen Entry untuk input Ruangan
entry_ruangan = tk.Entry(frame_form)
entry_ruangan.grid(row=2, column=3, padx=5, pady=3, sticky="ew")

# Konfigurasi tata letak grid agar kolom input bersifat responsif menyesuaikan lebar frame
frame_form.grid_columnconfigure(1, weight=1)
frame_form.grid_columnconfigure(3, weight=1)

# Membuat frame penampung tombol-tombol aksi CRUD
frame_btn = tk.Frame(root)
frame_btn.pack(fill="x", padx=15, pady=5)

# Membuat dan menampilkan tombol Tambah, Edit, Hapus, dan Clear secara berdampingan
tk.Button(frame_btn, text="Tambah", bg="#4CAF50", fg="white", command=tambah_data, width=12).pack(side="left", padx=5)
tk.Button(frame_btn, text="Edit", bg="#2196F3", fg="white", command=edit_data, width=12).pack(side="left", padx=5)
tk.Button(frame_btn, text="Hapus", bg="#f44336", fg="white", command=hapus_data, width=12).pack(side="left", padx=5)
tk.Button(frame_btn, text="Clear", bg="#9E9E9E", fg="white", command=clear_fields, width=12).pack(side="left", padx=5)

# Membuat frame penampung komponen tabel (Treeview)
frame_table = tk.Frame(root)
frame_table.pack(fill="both", expand=True, padx=15, pady=10)

# Definisi nama identifier untuk setiap kolom tabel jadwal kuliah
columns = ("id_jadwal", "kode_mk", "hari", "jam_mulai", "jam_selesai", "ruangan")
# Membuat komponen Treeview untuk menampilkan struktur data tabular
tree = ttk.Treeview(frame_table, columns=columns, show="headings")

# Mengatur judul header yang tampil pada setiap kolom tabel
tree.heading("id_jadwal", text="ID Jadwal")
tree.heading("kode_mk", text="Kode MK")
tree.heading("hari", text="Hari")
tree.heading("jam_mulai", text="Jam Mulai")
tree.heading("jam_selesai", text="Jam Selesai")
tree.heading("ruangan", text="Ruangan")

# Mengatur lebar relatif dari masing-masing kolom tabel
tree.column("id_jadwal", width=80)
tree.column("kode_mk", width=100)
tree.column("hari", width=100)
tree.column("jam_mulai", width=100)
tree.column("jam_selesai", width=100)
tree.column("ruangan", width=150)

# Mengikat event klik/pilih item pada Treeview dengan fungsi handler select_item
tree.bind("<<TreeviewSelect>>", select_item)

# Membuat scrollbar vertikal dan menghubungkannya dengan komponen Treeview
scrollbar = ttk.Scrollbar(frame_table, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)

# Menampilkan Treeview dan Scrollbar ke dalam frame tabel
tree.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Memanggil fungsi load_data() untuk menampilkan data awal saat aplikasi pertama kali dijalankan
load_data()

# Memulai loop utama peristiwa GUI Tkinter
root.mainloop()