import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

# Leggi il file CSV
df = pd.read_csv('similarity_d_2.csv')

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

# Crea una griglia dai dati
x_unique = np.sort(df['seeds_minimizer_length'].unique())
y_unique = np.sort(df['seeds_minimizer_windowsize'].unique())
X, Y = np.meshgrid(x_unique, y_unique)

# Crea una matrice Z per i valori di similarità
Z = np.zeros_like(X, dtype=float)
for i, y_val in enumerate(y_unique):
    for j, x_val in enumerate(x_unique):
        mask = (df['seeds_minimizer_length'] == x_val) & (df['seeds_minimizer_windowsize'] == y_val)
        if mask.any():
            Z[i, j] = df.loc[mask, 'similarity_score'].iloc[0]

# Crea il grafico
fig, ax = plt.subplots(figsize=(12, 8))

# Plot usando pcolormesh
mesh = plt.pcolormesh(X, Y, Z, 
                     cmap=custom_cmap,
                     vmin=0,
                     vmax=1.0,
                     shading='nearest')

# Personalizza gli assi
plt.xlabel('Minimizer Length')
plt.ylabel('Window Size')

# Imposta i tick per l'asse x (Minimizer Length) con numeri interi
plt.xticks(np.arange(10, 31, 2))

# Imposta i tick per l'asse y (Window Size) con numeri interi
plt.yticks(np.arange(10, 41, 5))

# Aggiungi una barra dei colori
plt.colorbar(mesh, label='Similarity Score')

# Imposta il titolo
plt.title('Similarity Score vs Minimizer Length and Window Size')

# Aggiungi la griglia
plt.grid(True, linestyle='--', alpha=0.7)

# Crea un'annotazione che sarà aggiornata
annot = ax.annotate("", xy=(0,0), xytext=(10,10), textcoords="offset points",
                    bbox=dict(boxstyle="round", fc="w", ec="0.5", alpha=0.9),
                    ha='center', va='center')
annot.set_visible(False)

def update_annot(event):
    if event.inaxes == ax:
        x, y = event.xdata, event.ydata
        if x is not None and y is not None:
            # Trova l'indice più vicino nella griglia
            x_idx = np.abs(x_unique - x).argmin()
            y_idx = np.abs(y_unique - y).argmin()
            
            # Ottieni il valore dalla matrice Z
            z = Z[y_idx, x_idx]
            
            # Aggiorna il testo dell'annotazione
            annot.xy = (x_unique[x_idx], y_unique[y_idx])
            text = f'Minimizer Length: {x_unique[x_idx]:.0f}\nWindow Size: {y_unique[y_idx]:.0f}\nSimilarity Score: {z:.3f}'
            annot.set_text(text)
            annot.set_visible(True)
            fig.canvas.draw_idle()
    else:
        annot.set_visible(False)
        fig.canvas.draw_idle()

fig.canvas.mpl_connect('motion_notify_event', update_annot)

# Mostra il grafico
plt.show()