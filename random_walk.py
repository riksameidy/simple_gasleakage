import random
from math import *
from Particle import *


def cekJumlahInside(arr_partikel):
    jum = 0
    for i,partikel in enumerate(arr_partikel):
        if(partikel.isInside==1):
            jum = jum + 1
    return jum

def bangkitkan_random():
    arr_r = []
    for i in range(5):
        arr_r.append( random.uniform(0,1) )
    return arr_r

def inisialisasi_posisi(r1,r2,r3,a):
    x = r1 * a
    y = r2 * a
    z = r3 * a
    return Posisi(x,y,z)

def next_posisi(particle,delta_t):
    x = particle.posisi.x +  particle.kecepatan.vx * delta_t
    y = particle.posisi.y + particle.kecepatan.vy * delta_t
    z = particle.posisi.z + particle.kecepatan.vz * delta_t
    return Posisi(x,y,z)

def update_posisi(partikel,delta_t,a,lingkaran):

    isStop = 0
    isOut = 0
    posisi_baru = next_posisi(partikel,delta_t)

    while(isStop==0 and isOut==0):

        [posisi_baru_after, delta_posisi_baru ] = checkBoundary(posisi_baru.x,posisi_baru.y,posisi_baru.z,a)

        if(abs(delta_posisi_baru.x) + abs(delta_posisi_baru.y )+ abs(delta_posisi_baru.z) > 0 ):
            # Wall Hit
            cek_wall_flag = [0,0,0]
            if(delta_posisi_baru.x > 0):
                # hit wall perpendicuar to sumbu x

                posisi_baru_after.x = posisi_baru_after.x - abs(delta_posisi_baru.x)
                cek_wall_flag[0] = 1

            if(delta_posisi_baru.y > 0 ):
                # hit wall perpendicuar to sumbu y
                cek_wall_flag[1] = 1

            if(delta_posisi_baru.z > 0):
                # hit wall perpendicuar to sumbu z
                posisi_baru_after.z = posisi_baru_after.z - abs(delta_posisi_baru.z)
                cek_wall_flag[2] = 1

            if( cek_wall_flag[1] == 1 and posisi_baru_after.y ==a):
                # apakah ada di dinding y=a
                if(isInHole(lingkaran,posisi_baru_after)==1):
                    # apakah ada di hole
                    partikel.isInside = 0
                    partikel.posisi = Posisi(-5,-5,-5)
                    isOut = 1

                posisi_baru_after.y = posisi_baru_after.y - abs(delta_posisi_baru.y)

            posisi_baru = posisi_baru_after

        else:
            isStop = 1

    if(partikel.isInside==1):
        partikel.posisi = posisi_baru

def update_posisi2(partikel,delta_t,a,lingkaran):
    calon_posisi_baru = next_posisi(partikel, delta_t)
    [posisi_baru_temp, wall_flag,wall_hit] = checkBoundary(calon_posisi_baru.x, calon_posisi_baru.y, calon_posisi_baru.z, a)

    if(wall_hit==1):

        if( wall_flag[0]==1 or wall_flag[0]==2):
            # hit wall perpendicuar to sumbu x
            posisi_partikel = partikel.posisi.x
            posisi_temp = posisi_baru_temp.x
            kecepatan_partikel = partikel.kecepatan.vx
            sumbu_update = 'x'
        elif(wall_flag[1]==1 or wall_flag[1]==2):
            # hit wall perpendicuar to sumbu y
            posisi_partikel = partikel.posisi.y
            posisi_temp = posisi_baru_temp.y
            kecepatan_partikel = partikel.kecepatan.vy
            sumbu_update = 'y'
        elif(wall_flag[2]==1 or wall_flag[2]==2):
            # hit wall perpendicuar to sumbu z
            posisi_partikel = partikel.posisi.z
            posisi_temp = posisi_baru_temp.z
            kecepatan_partikel = partikel.kecepatan.vz
            sumbu_update = 'z'

        if (isInHole(lingkaran, posisi_baru_temp) == 1 and wall_flag[1]==2):
            # apakah ada di hole
            partikel.isInside = 0
            partikel.posisi = Posisi(-5, -5, -5)
        else:
            # ada di dinding
            delta_t_to_wall = (posisi_temp - posisi_partikel) / kecepatan_partikel
            sisa_delta_t = delta_t - delta_t_to_wall
            posisi_di_wall = next_posisi(partikel, delta_t_to_wall)
            v_baru = kecepatan_partikel * -1

            if(sumbu_update=='x'):
                vbaru = Kecepatan(v_baru, partikel.kecepatan.vy, partikel.kecepatan.vz)
            elif(sumbu_update=='y'):
                vbaru = Kecepatan(partikel.kecepatan.vx, v_baru, partikel.kecepatan.vz)
            elif(sumbu_update=='z'):
                vbaru = Kecepatan(partikel.kecepatan.vx, partikel.kecepatan.vy, v_baru)

            partikel.posisi = posisi_di_wall
            partikel.kecepatan = vbaru
            posisi_baru = next_posisi(partikel, sisa_delta_t)
            partikel.posisi = posisi_baru

    else:
        partikel.posisi = calon_posisi_baru


def generate_kecepatan(v,r1,r2):
    m = 2 * pi * r1
    kos_t = 1 - 2 * r2
    sin_t = sqrt( 1 - kos_t**2 )

    vx = v * sin_t * cos(m)
    vy = v * sin_t * sin(m)
    vz = v * kos_t
    return Kecepatan(vx,vy,vz)

def inisialisasi_partikel(N,a,v,arr_r):
    arr_particle = []
    for i in range(N):
        posisi = inisialisasi_posisi( arr_r[0], arr_r[1],arr_r[2],a )
        kecepatan = generate_kecepatan(v,arr_r[3],arr_r[4])
        p = Particle(posisi,kecepatan)
        arr_particle.append(p)
    return arr_particle


def checkBoundary(x, y, z, a):
    xbaru = x
    ybaru = y
    zbaru = z
    wall_flag = [0,0,0]
    isHitwall = 0

    if (x < 0):
        xbaru = 0
        wall_flag[0] = 1
        isHitwall = 1

    if (x > a):
        xbaru = a
        wall_flag[0] = 2
        isHitwall = 1

    if (y < 0):
        ybaru = 0
        wall_flag[1] = 1
        isHitwall = 1

    if (y > a):
        ybaru = a
        wall_flag[1] = 2
        isHitwall = 1

    if (z < 0):
        zbaru = 0
        wall_flag[2] = 1
        isHitwall = 1

    if (z > a):
        zbaru = a
        wall_flag[2] = 2
        isHitwall = 1

    return [Posisi(xbaru, ybaru, zbaru), wall_flag, isHitwall ]

def isInHole(lingkaran,posisi):
    r = lingkaran.r
    px = posisi.x
    pz = posisi.z

    dist_l_to_posisi = sqrt( (px-lingkaran.a)**2 + (pz-lingkaran.b)**2  )
    if( dist_l_to_posisi <= r ):
        return 1
    else:
        return 0






