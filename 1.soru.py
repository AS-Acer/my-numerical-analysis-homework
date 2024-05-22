import numpy as np
import matplotlib.pyplot as plt

# Parametreler
m = 0.5  # kg
cd = 21 / 1000  # kg/m
g = 9.81  # m/s^2
v0 = 105  # m/s
y0 = 0  # m
dt = 0.01  # s

# Zaman adımları
t_max = 25  # maks zaman
t = np.arange(0, t_max, dt)

# Başlangıç değerleri
v = np.zeros_like(t)
y = np.zeros_like(t)
a = np.zeros_like(t)

v[0] = v0
y[0] = y0

# Sayısal çözüm
for i in range(1, len(t)):
    a[i-1] = -g - (cd/m) * v[i-1] * abs(v[i-1])
    v[i] = v[i-1] + a[i-1] * dt
    y[i] = y[i-1] + v[i-1] * dt

# İvme son adımını hesaplayın
a[-1] = -g - (cd/m) * v[-1] * abs(v[-1])

# En yüksek nokta
y_max = np.max(y)
t_y_max = t[np.argmax(y)]

# Terminal hız
v_terminal = np.sqrt((m * g) / cd)
t_half_terminal = t[np.where(v <= v_terminal / 2)[0][0]]
y_half_terminal = y[np.where(v <= v_terminal / 2)[0][0]]

# Yere dönüş zamanı
t_ground = t[np.where(y <= 0)[0][1]] if len(np.where(y <= 0)[0]) > 1 else t[-1]

print(f"En yüksek konum: {y_max:.2f} m, Zaman: {t_y_max:.2f} s")
print(f"Terminal hız: {v_terminal:.2f} m/s")
print(f"Terminal hızın yarısına ulaşma zamanı: {t_half_terminal:.2f} s, Yükseklik: {y_half_terminal:.2f} m")
print(f"Yere düşme zamanı: {t_ground:.2f} s")

# Grafik çizimi
plt.figure(figsize=(12, 8))

plt.subplot(3, 1, 1)
plt.plot(t, y, label='y(t)')
plt.axhline(0, color='black', linewidth=0.5)
plt.axvline(t_ground, color='red', linestyle='--', label=f'Yere düşme zamanı: {t_ground:.2f} s')
plt.xlabel('Zaman (s)')
plt.ylabel('Yükseklik (m)')
plt.legend()

plt.subplot(3, 1, 2)
plt.plot(t, v, label='v(t)')
plt.axhline(0, color='black', linewidth=0.5)
plt.axhline(v_terminal, color='green', linestyle='--', label=f'Terminal hız: {v_terminal:.2f} m/s')
plt.xlabel('Zaman (s)')
plt.ylabel('Hız (m/s)')
plt.legend()

plt.subplot(3, 1, 3)
plt.plot(t, a, label='a(t)')
plt.axhline(-g, color='black', linewidth=0.5)
plt.xlabel('Zaman (s)')
plt.ylabel('İvme (m/s²)')
plt.legend()

plt.tight_layout()
plt.show()
