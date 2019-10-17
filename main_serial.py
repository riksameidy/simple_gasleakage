from random_walk import *
import time


def main_serial(N, a, v, delta_t, t_simulasi, z_pusat, x_pusat, r):
    start = time.time()
    arr_r = bangkitkan_random()
    arr_particle = inisialisasi_partikel(N, a, v, arr_r)
    step = t_simulasi / delta_t
    lingkaran = Hole(x_pusat, z_pusat, r)  # ada di dinding  y=a, titik pusat1: x, titik pusat2: y

    hasil = []
    t = []
    i = 0
    p_hist = []
    while (i <= step):
        arrPart = []
        for j in range(N):


            if (arr_particle[j].isInside == 1):
                update_posisi2(arr_particle[j], delta_t, a, lingkaran)
                arr_r = bangkitkan_random()
                arr_particle[j].kecepatan = generate_kecepatan(v, arr_r[3], arr_r[4])

            part = Particle(arr_particle[j].posisi,arr_particle[j].kecepatan)
            arrPart.append(part)

        hasil.append(cekJumlahInside(arr_particle))
        t.append(delta_t * (i))
        p_hist.append(arrPart)



        i = i + 1

    end = time.time()
    elapsed = end - start
    return [p_hist, hasil, t, elapsed]


# ======================= Parameter Simulasi =======================================================
N = 1000
a = 12
v = 6
delta_t = 0.1
t_simulasi = 1000
z_pusat = 1 / 2 * a
x_pusat = 1/2 * a
r = 3
# # ==================================================================================================
#
# # =================== Serial =======================================================================
[p_hist, hasil, t, elapsed] = main_serial(N, a, v, delta_t, t_simulasi, z_pusat, x_pusat, r)
# ==================================================================================================
print('=============== Serial Result ============')
print('N awal = ' + str(N))
print('sisa partikel = ' + str(hasil[len(hasil) - 1]))
print('time serial = ' + str(elapsed) + ' s')
print('=========================================')