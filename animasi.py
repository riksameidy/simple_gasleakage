import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
from main_serial import *
import numpy as np
# ======================= Parameter Simulasi =======================================================
N = 100
a = 12
v = 6
delta_t = 0.1
t_simulasi = 1000
z_pusat = 1 / 2 * a
x_pusat = 1/ 2 * a
r = 3
# ==================================================================================================

# =================== Serial =======================================================================
[p_hist, hasil, t, elapsed] = main_serial(N, a, v, delta_t, t_simulasi, z_pusat, x_pusat, r)
# ==================================================================================================
print('=============== Serial Result ============')
print('N awal = ' + str(N))
print('sisa partikel = ' + str(hasil[len(hasil) - 1]))
print('time serial = ' + str(elapsed) + ' s')
print('=========================================')

fig = plt.figure(figsize=(12,6))
ax1 = fig.add_subplot(131, projection='3d')
ax2 = fig.add_subplot(132)
ax3 = fig.add_subplot(133)

def f(x,y,a):
    return ((x + y) * 0 ) + a



x = np.linspace(0,a)
y = np.linspace(0,a)
z = np.linspace(0,a)
X1, Y1 = np.meshgrid(x, y)
X2,Z2 = np.meshgrid(x,z)
Y3,Z3 = np.meshgrid(y,z)
ax3.plot(np.arange(0,len(hasil),1 )-1,hasil)

# ====================================================================================================
i=-1
for p in p_hist:
    i=i+1
    xs = []
    ys = []
    zs = []
    for partikel in p:
        xs.append(partikel.posisi.x)
        ys.append(partikel.posisi.y)
        zs.append(partikel.posisi.z)
    # Generate Kotak

    ax1.plot_wireframe(X1, Y1, f(X1, Y1, 0), rstride=50, cstride=50)
    ax1.plot_wireframe(X1, Y1, f(X1, Y1, a), rstride=50, cstride=50)

    ax1.plot_wireframe(X2, f(X1, Y1, a), Z2, rstride=50, cstride=50)
    ax1.plot_wireframe(X2, f(X1, Y1, 0), Z2, rstride=50, cstride=50)

    ax1.plot_wireframe(f(X1, Y1, 0), Y3, Z3, rstride=50, cstride=50)
    ax1.plot_wireframe(f(X1, Y1, a), Y3, Z3, rstride=50, cstride=50)
    # ===================================================================================================
    rling = np.sqrt(1.0)
    theta = np.linspace(0, 2 * np.pi, 100)
    h = 12
    xling = np.outer(rling, np.cos(theta) + x_pusat)
    zling = np.outer(rling, np.sin(theta) + z_pusat)
    lx, lz = np.meshgrid(xling, zling)
    ax1.plot_wireframe(xling, f(xling, xling, a), zling, color='r')
    ax1.set_xlim(-6,a)
    ax1.set_ylim(-6,a)
    ax1.set_zlim(-6,a)
    # ======================================================================================================
    ax1.scatter(xs,ys,zs,color='k')
    ax2.plot(range(i),hasil[0:i])
    plt.draw()
    plt.pause(0.02)
    ax1.cla()
    ax2.cla()

plt.show()

