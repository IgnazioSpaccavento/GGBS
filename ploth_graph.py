import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import LinearSegmentedColormap
from scipy.interpolate import griddata

# Leggi il file CSV
df = pd.read_csv('similarity_scores_density_3.csv')

# Crea una griglia più fine per l'interpolazione
length_min, length_max = df['seeds_minimizer_length'].min(), df['seeds_minimizer_length'].max()
window_min, window_max = df['seeds_minimizer_windowsize'].min(), df['seeds_minimizer_windowsize'].max()

# Crea una griglia più densa di punti
grid_x = np.linspace(length_min, length_max, 200)
grid_y = np.linspace(window_min, window_max, 200)
X_fine, Y_fine = np.meshgrid(grid_x, grid_y)

# Prepara i dati per l'interpolazione
points = np.column_stack((df['seeds_minimizer_length'], df['seeds_minimizer_windowsize']))
values = df['similarity_score']

# Interpola i dati sulla griglia più fine
Z_fine = griddata(points, values, (X_fine, Y_fine), method='cubic')

# Crea una mappa di colori personalizzata con più sfumature
colors = [
    (0.8, 0, 0),      # Rosso scuro
    (1, 0, 0),        # Rosso
    (1, 0.5, 0),      # Arancione
    (1, 0.8, 0),      # Arancione chiaro
    (1, 1, 0),        # Giallo
    (0.7, 1, 0),      # Giallo-verde
    (0.4, 1, 0),      # Verde chiaro
    (0, 1, 0)         # Verde
]
n_bins = 256
custom_cmap = LinearSegmentedColormap.from_list("custom", colors, N=n_bins)

# Crea il grafico 3D
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')

# Plot della superficie con i dati interpolati
surf = ax.plot_surface(X_fine, Y_fine, Z_fine,
                      cmap=custom_cmap,
                      linewidth=0.5,
                      antialiased=True,
                      vmin=0,
                      vmax=1.0)

# Personalizza gli assi
ax.set_xlabel('Minimizer Length')
ax.set_ylabel('Window Size')
ax.set_zlabel('Similarity Score')

# Imposta i limiti degli assi
ax.set_xlim(10, 30)
ax.set_ylim(10, 40)
ax.set_zlim(0, 1.0)

# Imposta i tick per l'asse x (Minimizer Length) con numeri interi
ax.set_xticks(np.arange(10, 31, 2))
ax.xaxis.set_major_formatter(plt.FormatStrFormatter('%d'))

# Imposta i tick per l'asse y (Window Size) con numeri interi
ax.set_yticks(np.arange(10, 41, 5))
ax.yaxis.set_major_formatter(plt.FormatStrFormatter('%d'))

# Imposta l'angolo di vista
ax.view_init(elev=30, azim=-45)

# Aggiungi una barra dei colori
plt.colorbar(surf, shrink=0.5, aspect=5)

# Imposta il titolo
plt.title('Similarity Score vs Minimizer Length and Window Size')

# Mostra il grafico
plt.show()