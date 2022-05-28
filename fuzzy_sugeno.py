# Nama : Hendrik Purnama Yuniar
# Nim : 191011401792
# Kelas: 06tple025
# Matakuliah: Kecerdasan Buatan
# UAS: Metode Sugeno
# Studi Kasus: 
# diketahui : barang_keluar-> minimum=1500, maximum=3600
#             stok_barang-> minimum=200, medium=380, maximum=700
#             barang_masuk-> minimum=2500, maximum=7500
# ditentukan : Jumlah barang masuk?
# jika barang keluar 4300 dan stok barang 3600?

def down(x, xmin, xmax):
    return (xmax- x) / (xmax - xmin)

def up(x, xmin, xmax):
    return (x - xmin) / (xmax - xmin)

class Keluar():
    minimum = 1500
    maximum = 3600

    def turun(self, x):
        if x >= self.maximum:
            return 0
        elif x <= self.minimum:
            return 1
        else:
            return down(x, self.minimum, self.maximum)

    def naik(self, x):
        if x >= self.maximum:
            return 1
        elif x <= self.minimum:
            return 0
        else:
            return up(x, self.minimum, self.maximum)

class Stok():
    minimum = 200
    medium = 380
    maximum = 700

    def sedikit(self, x):
        if x >= self.medium:
            return 0
        elif x <= self.minimum:
            return 1
        else:
            return down(x, self.minimum, self.medium)
    
    def cukup(self, x):
        if self.minimum < x < self.medium:
            return up(x, self.minimum, self.medium)
        elif self.medium < x < self.maximum:
            return down(x, self.medium, self.maximum)
        elif x == self.medium:
            return 1
        else:
            return 0

    def banyak(self, x):
        if x >= self.maximum:
            return 1
        elif x <= self.medium:
            return 0
        else:
            return up(x, self.medium, self.maximum)

class Masuk():
    minimum = 2500
    maximum = 7500
    
    def kurang(self, α):
        return self.maximum - α * (self.maximum-self.minimum)

    def tambah(self, α):
        return α *(self.maximum - self.minimum) + self.minimum

    # 2 barang_keluar 3 stok_barang
    def inferensi(self, jumlah_keluar, jumlah_stok):
        pmt = Keluar()
        psd = Stok()
        result = []
        # [R1] JIKA barang_keluar TURUN, dan stok_barang BANYAK, 
        #     MAKA barang_masuk BERKURANG.
        α1 = min(pmt.turun(jumlah_keluar), psd.banyak(jumlah_stok))
        z1 = self.kurang(α1)
        result.append((α1, z1))
        # [R2] JIKA barang_keluar TURUN, dan stok_barang SEDIKIT, 
        #     MAKA barang_masuk BERKURANG.
        α2 = min(pmt.turun(jumlah_keluar), psd.sedikit(jumlah_stok))
        z2 = self.kurang(α2)
        result.append((α2, z2))
        # [R3] JIKA barang_keluar NAIK, dan stok_barang BANYAK, 
        #     MAKA barang_masuk BERTAMBAH.
        α3 = min(pmt.naik(jumlah_keluar), psd.banyak(jumlah_stok))
        z3 = self.tambah(α3)
        result.append((α3, z3))
        # [R4] JIKA barnag_keluar NAIK, dan stok_barang SEDIKIT,
        #     MAKA barang_masuk BERTAMBAH.
        α4 = min(pmt.naik(jumlah_keluar), psd.sedikit(jumlah_stok))
        z4 = self.tambah(α4)
        result.append((α4, z4))

        # [R5] JIKA barang_keluar NAIK, dan stok_barang CUKUP,
        #     MAKA barang_masuk BERKURANG.
        α5 = min(pmt.naik(jumlah_keluar), psd.cukup(jumlah_stok))
        z5 = self.kurang(α5)
        result.append((α5, z5))

        # [R6] JIKA barang_keluar NAIK, dan stok_barang CUKUP,
        #     MAKA brang_masuk BERKURANG.
        α6 = min(pmt.turun(jumlah_keluar), psd.cukup(jumlah_stok))
        z6 = self.tambah(α6)
        result.append((α6, z6))

        return result
    
    def defuzifikasi(self, jumlah_keluar, jumlah_stok):
        inferensi_values = self.inferensi(jumlah_keluar, jumlah_stok)
        return sum([(value[0]* value[1]) for value in inferensi_values]) / sum([value[0] for value in inferensi_values])