class Posisi:
    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z


class Kecepatan:
    def __init__(self,vx,vy,vz):
        self.vx = vx
        self.vy = vy
        self.vz = vz

class Hole:
    def __init__(self,a,b,r):
        self.a = a
        self.b = b
        self.r = r


class Particle:
    def __init__(self,posisi,kecepatan):
        self.posisi = posisi
        self.kecepatan = kecepatan
        self.isInside = 1

    def update_posisi(self,posisi):
        self.posisi = posisi

    def update_kecepatan(self,kecepatan):
        self.kecepatan = kecepatan

    def print_posisi(self):
        print("Posisi: ("  + str(self.posisi.x) + "," + str(self.posisi.y) + "," + str(self.posisi.z) + ")" )

    def print_kecepatan(self):
        print("Kecepatan: (" + str(self.kecepatan.vx) + "," + str(self.kecepatan.vy) + "," + str(self.kecepatan.vz) + ")")