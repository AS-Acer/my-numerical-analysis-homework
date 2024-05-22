import numpy as np

# Parametreler
L = 4.0          # Kirişin uzunluğu (m)
h0 = 0.3         # Sabit uçtaki yükseklik (m)
hL = 0.15        # Serbest uçtaki yükseklik (m)
E = 10e9         # Elastisite Modülü (Pa)
b = 0.21         # Kiriş genişliği (m)
P = 21e3         # Kuvvet (N)
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

# Matrislerin oluşturulması
A = np.zeros((n+1, n+1))
B = np.zeros(n+1)

# İç düğümler
for i in range(1, n):
    A[i, i-1] = I_values[i-1] / dx**2
    A[i, i] = -2 * I_values[i] / dx**2
    A[i, i+1] = I_values[i+1] / dx**2

# Uç koşulları
A[0, 0] = 1  # y(0) = 0
A[n, n] = 1  # y(L) = 0
A[n, n-1] = -1 / dx  # Eğilme momenti

B[n] = -P * dx / (E * I_values[-1])

# Çözüm
y = np.linalg.solve(A, B)

# Orta noktadaki çökme ve dönme
middle_index = n // 2
displacement_middle = y[middle_index]
slope_middle = (y[middle_index + 1] - y[middle_index - 1]) / (2 * dx)

print("Orta noktadaki çökme: {:.6f} m".format(displacement_middle))
print("Orta noktadaki dönme: {:.6f} rad".format(slope_middle))
