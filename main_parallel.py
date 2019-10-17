from random_walk import *
import time
from mpi4py import MPI


def main_parallel(N, a, v, delta_t, t_simulasi, z_pusat, x_pusat, r):
    start = time.time()
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    if rank == 0:
        N_parallel = (N // (size - 1))
        N_sisa = (N % (size - 1))
        arr_r = bangkitkan_random()
        step = t_simulasi / delta_t
        lingkaran = Hole(x_pusat, z_pusat, r)  # ada di dinding  y=a, titik pusat1: x, titik pusat2: y
        hasil = []
        t = []
        p_hist = []
        data = [N, N_parallel, N_sisa, a, v, arr_r, delta_t, t_simulasi, step, lingkaran, hasil, t, p_hist]
    else:
        data = None

    data = comm.bcast(data, root=0)
    N = data[0]
    N_parallel = data[1]
    N_sisa = data[2]
    a = data[3]
    v = data[4]
    arr_r = data[5]
    delta_t = data[6]
    t_simulasi = data[7]
    step = data[8]
    lingkaran = data[9]
    hasil = data[10]
    t = data[11]
    p_hist = data[12]
    i = 0

    N_partikel = None
    if rank == 0:
        N_partikel = N_sisa
    else:
        N_partikel = N_parallel

    arr_particle = inisialisasi_partikel(N_partikel, a, v, arr_r)

    while (i < step):
        for j in range(N_partikel):

            if (arr_particle[j].isInside == 1):
                update_posisi2(arr_particle[j], delta_t, a, lingkaran)
                arr_r = bangkitkan_random()
                arr_particle[j].kecepatan = generate_kecepatan(v, arr_r[3], arr_r[4])

        hasil.append(cekJumlahInside(arr_particle))
        t.append(delta_t * (i))
        p_hist.append(arr_particle.copy())
        i = i + 1

    hasil = comm.gather(hasil, root=0)
    t = comm.gather(t, root=0)
    p_hist = comm.gather(p_hist, root=0)
    end = time.time()
    elapsed = end - start
    if (rank == 0):
        temp = hasil[0][:]
        for i_ in range(1, len(hasil)):
            for j_ in range(0, len(hasil[i_])):
                temp[j_] = temp[j_] + hasil[i_][j_]
        print('=============== Parallel Result ============')
        print('N awal = ' + str(N))
        print('sisa partikel= ' + str(temp[len(temp) - 1]))
        print('time parallel = ' + str(elapsed) + ' s')
        print('=========================================')


# ======================= Parameter Simulasi =======================================================
N = 1000
a = 12
v = 6
delta_t = 0.1
t_simulasi = 1000
z_pusat = 1 / 2 * a
x_pusat = 1/2 * a
r = 3
# ==================================================================================================
main_parallel(N, a, v, delta_t, t_simulasi, z_pusat, x_pusat, r)
