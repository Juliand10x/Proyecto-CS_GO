import nbformat as nbf
import os

nb = nbf.v4.new_notebook()

nb['cells'] = [
    nbf.v4.new_markdown_cell("""# Visualización de Priors: Distribuciones de Probabilidad
Este cuaderno muestra gráficamente las distribuciones que hemos elegido para nuestras **Priors**. La forma de estas curvas (campanas de Gauss) representa nuestra incertidumbre inicial sobre los efectos de cada variable.
"""),

    nbf.v4.new_code_cell("""import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import seaborn as sns

sns.set_theme(style="whitegrid")

def plot_prior_styled(name, mu, sigma, color, description):
    dist = stats.norm(mu, sigma)
    x = np.linspace(mu - 4*sigma, mu + 4*sigma, 500)
    plt.figure(figsize=(10, 5))
    plt.plot(x, dist.pdf(x), lw=4, color=color, label=f'N({mu}, {sigma})')
    plt.fill_between(x, dist.pdf(x), alpha=0.3, color=color)
    plt.axvline(mu, color='black', linestyle='--', alpha=0.5, label='Media Prior')
    plt.title(f'Prior para {name}', fontsize=16)
    plt.xlabel('Valor del Parámetro (Beta)')
    plt.ylabel('Densidad de Probabilidad')
    plt.legend()
    plt.figtext(0.5, -0.05, description, wrap=True, horizontalalignment='center', fontsize=12)
    plt.tight_layout()
    plt.savefig(f"prior_{name.lower().replace(' ', '_')}.png", dpi=300)
    plt.show()
"""),

    nbf.v4.new_markdown_cell("### Distribución Prior 1: Rating (Informativa)"),
    nbf.v4.new_code_cell("""plot_prior_styled(
    'Rating', 
    4.79, 1.28, 
    '#2ecc71', 
    "Es una prior Informativa. La campana es estrecha porque confiamos en el fuerte vínculo Rating-Victoria hallado en el EDA."
)"""),

    nbf.v4.new_markdown_cell("### Distribución Prior 2: Impacto (Débilmente Informativa)"),
    nbf.v4.new_code_cell("""plot_prior_styled(
    'Impacto', 
    1.99, 5.0, 
    '#f1c40f', 
    "Es una prior Débilmente Informativa. La campana es ancha para permitir que los nuevos datos modifiquen el resultado fácilmente."
)"""),

    nbf.v4.new_markdown_cell("### Distribución Prior 3: Intercepto (No Informativa)"),
    nbf.v4.new_code_cell("""plot_prior_styled(
    'Intercepto', 
    0.01, 100.0, 
    '#95a5a6', 
    "Es una prior No Informativa. Casi plana para garantizar neutralidad absoluta sobre qué equipo parte con ventaja."
)""")
]

with open('Priors.ipynb', 'w') as f:
    nbf.write(nb, f)
print("Notebook Priors actualizado y listo.")
