import numpy as np

# Parametreler
L = 4.0          # Kirişin uzunluğu (m)
h0 = 0.3         # Sabit uçtaki yükseklik (m)
hL = 0.15        # Serbest uçtaki yükseklik (m)
E = 10e9         # Elastisite Modülü (Pa)
b = 0.21         # Kiriş genişliği (m)
P = 21e3         # Kuvvet (N)
q = P / L        # Düzgün yayılı yük (N/m)
n = 20           # Bölme sayısı
dx = L / n       # Bölme uzunluğu

# Yükseklik fonksiyonu ve momentler inertia
def h(x):
    return h0 + (hL - h0) / L * x

def I(x):
    return (1/12) * b * h(x)**3

# Kesişim noktalarının konumları
x = np.linspace(0, L, n+1)
I_values = I(x)
q_values = q * np.ones(n+1)

# Matrislerin oluşturulması
A = np.zeros((n+1, n+1))
B = np.zeros(n+1)

# İç düğümler
for i in range(1, n):
    A[i, i-1] = I_values[i-1] / dx**2
    A[i, i] = -2 * I_values[i] / dx**2
    A[i, i+1] = I_values[i+1] / dx**2
    B[i] = q_values[i]

# Sınır koşulları
A[0, 0] = 1  # y(0) = 0
A[n, n] = 1  # y(L) = 0

# Çözüm
y = np.linalg.solve(A, B)

# Orta noktadaki çökme ve dönme
max_deflection = np.min(y)
max_deflection_location = x[np.argmin(y)]
slope_middle = (y[1] - y[0]) / dx

# Moment ve Kesme Kuvveti Hesaplamaları
moment = E * I_values * np.gradient(np.gradient(y, dx), dx)
max_moment = np.max(moment)
max_moment_location = x[np.argmax(moment)]
shear_force = q * (L - x)
max_shear_force = np.max(shear_force)
max_shear_force_location = x[np.argmax(shear_force)]

print(f"En büyük çökme: {max_deflection:.6f} m, Konum: {max_deflection_location:.6f} m")
print(f"En büyük pozitif dönme: {slope_middle:.6f} rad")
print(f"En büyük pozitif moment: {max_moment:.6f} Nm, Konum: {max_moment_location:.6f} m")
print(f"En büyük pozitif kesme kuvveti: {max_shear_force:.6f} N, Konum: {max_shear_force_location:.6f} m")
