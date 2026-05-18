import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# 1. Importar los datos médicos originales
df = pd.read_csv('medical_examination.csv')

# 2. Agregar la columna 'overweight' (IMC > 25)
# Nota: La altura viene en cm, por eso se divide por 100 antes de elevar al cuadrado.
bmi = df['weight'] / ((df['height'] / 100) ** 2)
df['overweight'] = (bmi > 25).astype(int)

# 3. Normalizar los datos (0 = bueno, 1 = malo)
df['cholesterol'] = (df['cholesterol'] > 1).astype(int)
df['gluc'] = (df['gluc'] > 1).astype(int)

# 4. Dibuja el gráfico categórico
def draw_cat_plot():
    # 5. Crear el DataFrame para el gráfico usando pd.melt
    df_cat = pd.melt(
        df, 
        id_vars=['cardio'], 
        value_vars=['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight']
    )

    # 6. Agrupar y reformatear los datos para mostrar los recuentos
    df_cat = df_cat.groupby(['cardio', 'variable', 'value']).size().reset_index(name='total')
    
    # 7. Crear el gráfico categórico con sns.catplot()
    cat_plot = sns.catplot(
        x='variable', 
        y='total', 
        hue='value', 
        col='cardio', 
        data=df_cat, 
        kind='bar'
    )

    # 8. Obtener la figura de la salida
    fig = cat_plot.fig

    # 9. No modificar las siguientes dos líneas
    fig.savefig('catplot.png')
    return fig


# 10. Dibuja el mapa de calor
def draw_heat_map():
    # 11. Limpiar los datos en df_heat según los percentiles solicitados
    df_heat = df[
        (df['ap_lo'] <= df['ap_hi']) &
        (df['height'] >= df['height'].quantile(0.025)) &
        (df['height'] <= df['height'].quantile(0.975)) &
        (df['weight'] >= df['weight'].quantile(0.025)) &
        (df['weight'] <= df['weight'].quantile(0.975))
    ]

    # 12. Calcular la matriz de correlación
    corr = df_heat.corr()

    # 13. Generar una máscara para el triángulo superior
    mask = np.triu(np.ones_like(corr, dtype=bool))

    # 14. Configurar la figura de matplotlib
    fig, ax = plt.subplots(figsize=(12, 12))

    # 15. Graficar la matriz utilizando sns.heatmap()
    sns.heatmap(
        corr, 
        mask=mask, 
        annot=True, 
        fmt=".1f", 
        cmap='coolwarm', 
        vmax=0.3, 
        vmin=-0.1, 
        center=0, 
        square=True, 
        linewidths=.5, 
        cbar_kws={"shrink": .5}
    )

    # 16. No modificar las siguientes dos líneas
    fig.savefig('heatmap.png')
    return fig
