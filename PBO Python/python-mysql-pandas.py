# Pandas membutuhkan library konektor seperti SQLAlchemy dan mysql-connector-python atau PyMySQL untuk terhubung ke MySQL
# install terlebih dahulu mysql connector lewat terminal/cmd => pip install pandas sqlalchemy mysql-connector-python
import pandas as pd
# Memanggil library Pandas dan memberinya alias pd (singkatan standar agar lebih pendek saat ditulis). Pandas digunakan untuk mengolah data berbentuk tabel (DataFrame) dan membaca query dari SQL.
from sqlalchemy import create_engine
# Mengambil hanya fungsi create_engine dari pustaka SQLAlchemy. Fungsi ini bertugas membuat dan mengelola koneksi (engine) antara Python dan server database MySQL.

# 1. Format string koneksi SQLAlchemy:
# mysql+mysqlconnector://<username>:<password>@<host>/<database>
engine = create_engine("mysql+mysqlconnector://root:@localhost/siakad")

try:
    # 2. Menulis query SQL
    query = "SELECT * FROM dosen"

    # 3. Membaca data MySQL langsung ke Pandas DataFrame
    df = pd.read_sql(query, con=engine)
    ## df = pd.read_sql(query, con=engine) berfungsi untuk menjalankan perintah SQL ke database MySQL dan langsung menyimpan hasilnya ke dalam bentuk tabel Pandas (DataFrame).
    ### pd.read_sql(...): Fungsi bawaan library Pandas yang bertugas membaca data dari database relasional (seperti MySQL) menggunakan perintah SQL.
    ### query: Variabel yang berisi perintah SQL yang ingin dieksekusi (misalnya: "SELECT nip, nama_dosen FROM dosen").
    ### con=engine: Parameter koneksi yang mengarahkan Pandas ke database mana query tersebut harus dikirim, menggunakan konektor SQLAlchemy (engine) yang sudah dibuat sebelumnya.
    ### df: Variabel penampung hasil query berupa DataFrame (singkatan dari df), yaitu struktur data berbentuk tabel berkolom dan berbaris yang siap diolah atau ditampilkan.

    # 4. Menampilkan data
    print("--- 5 BARIS PERTAMA DATA ---")
    print(df.head())
    ## Perintah print(df.head()) berfungsi untuk mencetak/menampilkan 5 baris pertama dari data yang ada di dalam DataFrame (df).
    ### df: Variabel tempat menyimpan data tabel Pandas.
    ### .head(): Metode bawaan Pandas untuk mengambil baris teratas. Secara default/bawaan, fungsi ini mengambil 5 baris.
    ### print(...): Menampilkan hasil cetakannya ke layar console/terminal.
    ####  contoh lain misal => print(df.head(2))  # Menampilkan 2 baris pertama saja
    #### contol lainnya lagi => print(df.head(10)) # Menampilkan 10 baris pertama
    ### Jika ingin melihat baris dari paling bawah/terakhir, gunakan .tail()
    #### print(df.tail(3))  # Menampilkan 3 baris terakhir

# berfungsi sebagai sistem penangkap dan penampil pesan error saat kode program di dalam blok try mengalami kendala.
except Exception as e:
    print(f"Terjadi kesalahan: {e}")
## except: Menandai blok kode darurat yang hanya akan berjalan jika ada error saat program mengeksekusi perintah di dalam try.
## Exception: Jenis base class error di Python. Menggunakan Exception artinya program akan menangkap hampir semua jenis error umum (seperti koneksi database gagal, nama tabel/kolom salah, password salah, dsb).
## as e: Menyimpan objek/pesan error yang terjadi ke dalam variabel bernama e.
## f"Terjadi kesalahan: {e}" (f-string atau Formatted String Literal): Menggabungkan teks "Terjadi kesalahan: " dengan isi variabel e (pesan rincian error dari sistem).

finally:
    # 5. Menutup koneksi engine
    engine.dispose()
    # Blok finally: bersama perintah engine.dispose() berfungsi sebagai pembersih otomatis yang akan SELALU dijalankan, tidak peduli apakah program kamu berjalan sukses atau terjadi error.
    ## finally: Merupakan bagian akhir dari struktur try-except-finally. Kode di dalam blok ini dijamin akan tetap dieksekusi dalam kondisi apa pun—baik saat program di dalam try berhasil sampai selesai, maupun saat program gagal/gagal koneksi dan masuk ke except
    ## engine.dispose() Berfungsi untuk menutup dan membersihkan seluruh koneksi (connection pool) yang dibuka oleh SQLAlchemy ke database MySQL.
    ## tujuan dipakai script tersebut untuk mencegah Kebocoran Koneksi (Connection Leak): Jika koneksi tidak ditutup, MySQL akan menganggap program kamu masih terhubung. Jika program dijalankan berulang kali, antrean koneksi di MySQL bisa penuh (Too many connections) dan membuat database tidak bisa diakses lagi.
    ## Keamanan & Efisiensi Memori: Menutup koneksi secara tertib membebaskan RAM dan sumber daya server database agar bisa digunakan oleh aplikasi lain.