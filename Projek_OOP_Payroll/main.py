# 1. Class Karyawan (Superclass)
class Karyawan:
    def __init__(self, nama, id_karyawan, gaji_pokok):
        self.nama = nama  # public
        self.id_karyawan = id_karyawan  # public
        self.__gaji_pokok = 0  # private
        self.set_gaji_pokok(gaji_pokok)  # Menggunakan setter untuk validasi awal

    # Getter untuk gaji_pokok
    def get_gaji_pokok(self):
        return self.__gaji_pokok

    # Setter untuk gaji_pokok dengan validasi
    def set_gaji_pokok(self, gaji_pokok):
        if gaji_pokok <= 0:
            print(
                f"[Peringatan] Gaji pokok untuk {self.nama} harus lebih dari 0!"
            )
            self.__gaji_pokok = 0
        else:
            self.__gaji_pokok = gaji_pokok

    # Implementasi dasar hitung_gaji_total
    def hitung_gaji_total(self):
        return self.__gaji_pokok

    # Menampilkan informasi dasar karyawan
    def tampilkan_info(self):
        print(f"ID Karyawan  : {self.id_karyawan}")
        print(f"Nama Lengkap : {self.nama}")
        print(f"Gaji Pokok   : Rp {self.__gaji_pokok:,.2f}")


# 2. Class KaryawanTetap (Child Class dari Karyawan)
class KaryawanTetap(Karyawan):
    def __init__(self, nama, id_karyawan, gaji_pokok, tunjangan):
        super().__init__(nama, id_karyawan, gaji_pokok)
        self.tunjangan = tunjangan  # public

    # Overriding hitung_gaji_total
    def hitung_gaji_total(self):
        return self.get_gaji_pokok() + self.tunjangan

    # Overriding tampilkan_info
    def tampilkan_info(self):
        print("--- Detail Karyawan Tetap ---")
        super().tampilkan_info()
        print(f"Tunjangan    : Rp {self.tunjangan:,.2f}")
        print(f"Total Gaji   : Rp {self.hitung_gaji_total():,.2f}")
        print("-" * 30)


# 3. Class KaryawanKontrak (Child Class dari Karyawan)
class KaryawanKontrak(Karyawan):
    def __init__(self, nama, id_karyawan, gaji_pokok, jam_lembur, tarif_lembur):
        super().__init__(nama, id_karyawan, gaji_pokok)
        self.jam_lembur = jam_lembur  # public
        self.tarif_lembur = tarif_lembur  # public

    # Overriding hitung_gaji_total
    def hitung_gaji_total(self):
        total_lembur = self.jam_lembur * self.tarif_lembur
        return self.get_gaji_pokok() + total_lembur

    # Overriding tampilkan_info
    def tampilkan_info(self):
        print("--- Detail Karyawan Kontrak ---")
        super().tampilkan_info()
        print(f"Jam Lembur   : {self.jam_lembur} jam")
        print(f"Tarif Lembur : Rp {self.tarif_lembur:,.2f} /jam")
        print(
            f"Total Lembur : Rp {self.jam_lembur * self.tarif_lembur:,.2f}"
        )
        print(f"Total Gaji   : Rp {self.hitung_gaji_total():,.2f}")
        print("-" * 30)


# --- CONTOH IMPLEMENTASI / MAIN PROGRAM ---
if __name__ == "__main__":
    # Membuat objek Karyawan Tetap
    pegawai_tetap = KaryawanTetap(
        nama="Andi Pratama",
        id_karyawan="KT-001",
        gaji_pokok=5000000,
        tunjangan=1500000,
    )

    # Membuat objek Karyawan Kontrak
    pegawai_kontrak = KaryawanKontrak(
        nama="Siti Rahma",
        id_karyawan="KK-002",
        gaji_pokok=3500000,
        jam_lembur=10,
        tarif_lembur=50000,
    )

    # Menampilkan informasi masing-masing karyawan (Polymorphism in action)
    pegawai_tetap.tampilkan_info()
    print()
    pegawai_kontrak.tampilkan_info()

    # Contoh pengujian setter peringatan jika nilai <= 0
    print("\n[Pengujian Setter dengan nilai tidak valid]:")
    pegawai_tetap.set_gaji_pokok(100000)