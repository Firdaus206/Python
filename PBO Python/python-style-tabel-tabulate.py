# install terlebih dahulu tabulate lewat terminal/cmd => pip install tabulate
# lengkapnya => pip install pandas sqlalchemy mysql-connector-python tabulate

import pandas as pd 
# Memanggil library Pandas dan memberinya alias pd (singkatan standar agar lebih pendek saat ditulis). Pandas digunakan untuk mengolah data berbentuk tabel (DataFrame) dan membaca query dari SQL.
from sqlalchemy import create_engine
# Mengambil hanya fungsi create_engine dari pustaka SQLAlchemy. Fungsi ini bertugas membuat dan mengelola koneksi (engine) antara Python dan server database MySQL.
from tabulate import tabulate
# Mengambil fungsi tabulate dari pustaka Tabulate. Fungsi ini digunakan untuk merapikan tampilan tabel Pandas DataFrame di terminal dengan garis/border kotak-kotak yang indah.

# 1. Konfigurasi Koneksi ke Database 'siakad'
# Format: mysql+mysqlconnector://<username>:<password>@<host>/<database>
DB_USER = "root"          # Ganti sesuai username MySQL Anda
DB_PASS = ""              # Ganti jika MySQL Anda memakai password
DB_HOST = "localhost"     # Host database
DB_NAME = "siakad"        # Nama database dari file SQL Anda

# Membuat engine koneksi SQLAlchemy
engine = create_engine(f"mysql+mysqlconnector://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}")
## f"..." (f-string): Fitur Python untuk menyisipkan nilai dari variabel (seperti {DB_USER}, {DB_HOST}) langsung ke dalam teks secara otomatis.
## mysql+mysqlconnector://: Format URL koneksi (Connection String) yang menentukan:
### mysql: Jenis database yang dituju.
### mysqlconnector: Library/driver penghubung yang digunakan di Python (mysql-connector-python).
## {DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}: Format standar pengiriman akun autentikasi dan lokasi database:
###{DB_USER}: Username MySQL (contoh: root).
###{DB_PASS}: Password MySQL.
###{DB_HOST}: Alamat server MySQL (contoh: localhost).
###{DB_NAME}: Nama database yang diakses (contoh: siakad).
## create_engine(...): Fungsi dari SQLAlchemy yang menyiapkan jalur komunikasi dan mengelola connection pool (antrean koneksi) ke database.
## engine: Variabel penampung objek koneksi yang nantinya dikirimkan ke pd.read_sql() untuk mengeksekusi query.

try:
    # 2. Query SQL untuk mengambil kolom tertentu dari tabel 'dosen'
    ### Tanda petik tiga (""" atau ''') dalam Python disebut Multiline String.
    ### Tanda petik biasa (" atau ') hanya bisa digunakan untuk string satu baris. Jika kamu menekan Enter untuk membuat baris baru pakai petik biasa, Python akan memunculkan error SyntaxError: EOL while scanning string literal. Dengan petik 3, kamu bisa bebas menekan Enter dan merapikan perintah SQL agar mudah dibaca per baris
    query = """
    SELECT 
        nip AS 'NIP',
        nama_dosen AS 'Nama Dosen',
        email AS 'Email',
        no_telepon AS 'No. Telepon',
        pendidikan_terakhir AS 'Pendidikan',
        bidang_keahlian AS 'Bidang Keahlian'
    FROM dosen
    """

    # 3. Membaca data dari MySQL langsung ke Pandas DataFrame
    df = pd.read_sql(query, con=engine)
    ## df = pd.read_sql(query, con=engine) berfungsi untuk menjalankan perintah SQL ke database MySQL dan langsung menyimpan hasilnya ke dalam bentuk tabel Pandas (DataFrame).
    ### pd.read_sql(...): Fungsi bawaan library Pandas yang bertugas membaca data dari database relasional (seperti MySQL) menggunakan perintah SQL.
    ### query: Variabel yang berisi perintah SQL yang ingin dieksekusi (misalnya: "SELECT nip, nama_dosen FROM dosen").
    ### con=engine: Parameter koneksi yang mengarahkan Pandas ke database mana query tersebut harus dikirim, menggunakan konektor SQLAlchemy (engine) yang sudah dibuat sebelumnya.
    ### df: Variabel penampung hasil query berupa DataFrame (singkatan dari df), yaitu struktur data berbentuk tabel berkolom dan berbaris yang siap diolah atau ditampilkan.

    # 4. Menampilkan data dengan border grid yang rapi
    print("\n" + "="*50) # Mencetak baris baru (\n) diikuti karakter garis sama dengan = sebanyak 50 kali. Ini berfungsi sebagai garis pembatas bagian atas.
    print("           DATA DOSEN SIAKAD           ") # Mencetak teks judul "DATA DOSEN SIAKAD" di tengah-tengah garis pembatas.
    print("="*50) # Mencetak kembali garis sama dengan = sebanyak 50 kali sebagai pembatas bagian bawah judul.
    print(tabulate(df, headers='keys', tablefmt='grid', showindex=False)) 
    # Mencetak isi DataFrame (df) menggunakan pustaka tabulate agar berbentuk tabel bergaris:
    ## df: Data yang ingin ditampilkan (data dosen).
    ## headers='keys': Menggunakan nama kolom dari DataFrame sebagai judul baris paling atas tabel.
    ## tablefmt='grid': Memberikan garis border kotak-kotak (grid) pada tabel. model lain : https://pypi.org/project/tabulate/ atau https://github.com/astanin/python-tabulate
    ## showindex=False: Menyembunyikan nomor indeks bawaan dari Pandas (0, 1, 2, dst) agar tampilan tabel bersih.

except Exception as e: 
    # except: Menandai blok kode yang akan dijalankan hanya jika terjadi error di dalam blok try.
    # Exception: Jenis error umum di Python. Bagian ini memberi tahu Python untuk menangkap segala jenis error yang muncul (misalnya: gagal konek database, salah nama tabel, atau koneksi terputus).
    # as e: Menyimpan pesan/detail error yang terjadi ke dalam sebuah variabel bernama e.
    print(f"\n[ERROR] Terjadi kesalahan saat mengambil data: {e}")
    # Menampilkan pesan error asli dari sistem ke layar dalam bentuk teks, sehingga kamu tahu persis di mana letak kendalanya tanpa membuat program mati mendadak.

finally:
    # 5. Menutup koneksi engine
    engine.dispose()
    # Blok finally: bersama perintah engine.dispose() berfungsi sebagai pembersih otomatis yang akan SELALU dijalankan, tidak peduli apakah program kamu berjalan sukses atau terjadi error.
    ## finally: Merupakan bagian akhir dari struktur try-except-finally. Kode di dalam blok ini dijamin akan tetap dieksekusi dalam kondisi apa pun—baik saat program di dalam try berhasil sampai selesai, maupun saat program gagal/gagal koneksi dan masuk ke except
    ## engine.dispose() Berfungsi untuk menutup dan membersihkan seluruh koneksi (connection pool) yang dibuka oleh SQLAlchemy ke database MySQL.
    ## tujuan dipakai script tersebut untuk mencegah Kebocoran Koneksi (Connection Leak): Jika koneksi tidak ditutup, MySQL akan menganggap program kamu masih terhubung. Jika program dijalankan berulang kali, antrean koneksi di MySQL bisa penuh (Too many connections) dan membuat database tidak bisa diakses lagi.
    ## Keamanan & Efisiensi Memori: Menutup koneksi secara tertib membebaskan RAM dan sumber daya server database agar bisa digunakan oleh aplikasi lain.