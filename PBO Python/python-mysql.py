# install terlebih dahulu mysql connector lewat terminal/cmd => pip install mysql-connector-python
import mysql.connector

try:
    # 1. Membuat koneksi ke database
    db = mysql.connector.connect(
        host="localhost",
        user="root",          # ganti dengan username database Anda
        password="",          # ganti dengan password database Anda
        database="siakad"   # ganti dengan nama database Anda
    )

    # 2. Membuat objek cursor
    # Baris kode cursor = db.cursor() berfungsi untuk membuat objek Cursor yaitu "perantara" atau "papan pengetik" yang digunakan Python untuk mengirim perintah SQL dan mengambil data dari database MySQL.
    # Maksud dan Analogi sederhananya
    ## Jika koneksi database (db) diibaratkan sebagai kabel telepon yang sudah terhubung ke server database maka cursor adalah orang/pesuruh yang memegang mikrofon telepon tersebut.
    ## Tugas utama cursor meliputi:
    ### Mengirim & Menjalankan Perintah SQL
    #### Menjalankan perintah SQL seperti SELECT, INSERT, UPDATE, atau DELETE menggunakan fungsi cursor.execute().
    ### Menampung & Mengambil Hasil Query
    #### Menyimpan hasil pencarian data sementara agar bisa diambil oleh Python menggunakan fungsi cursor.fetchall() atau cursor.fetchone().

    cursor = db.cursor()

    # 3. Menulis dan menjalankan perintah SQL
    query = "SELECT * FROM dosen"
    cursor.execute(query)

    # 4. Mengambil seluruh hasil query
    results = cursor.fetchall()

    # 5. Menampilkan data menggunakan perulangan
    print("--- DATA DARI MYSQL ---")
    for row in results:
        print(row)

except mysql.connector.Error as err:
    print(f"Gagal terhubung ke database: {err}")

finally:
    # 6. Menutup cursor dan koneksi
    if 'cursor' in locals():
        # if 'cursor' in locals():
        ## Maksud: Memeriksa apakah variabel cursor sudah pernah dibuat di memori lokal program.
        ## Tujuan: Mencegah error baru jika program gagal sebelum objek cursor sempat dibuat (misalnya error terjadi tepat saat koneksi ke database gagal).
        cursor.close()
        # Maksud: Menutup objek cursor yang telah selesai digunakan.
        ## Tujuan: Membebaskan memori tempat menampung sementara hasil query SQL.
    if 'db' in locals() and db.is_connected():
        # Memeriksa dua hal sekaligus:
        ## Apakah variabel koneksi db ada di memori lokal?
        ## Apakah jalur koneksi ke server MySQL statusnya masih aktif/terhubung (db.is_connected())?
        db.close()
        # Menutup jalur koneksi utama dari Python ke database MySQL.
        ## Tujuan: Mengembalikan slot koneksi ke server MySQL agar batas maksimal koneksi database tidak habis (Too many connections).
