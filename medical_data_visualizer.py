import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()

# 1. Cargar y limpiar datos (Mantener entre los percentiles 2.5% y 97.5%)
df = pd.read_csv(
    "fcc-forum-pageviews.csv",
    index_col="date",
    parse_dates=True
)

df = df[
    (df["value"] >= df["value"].quantile(0.025)) &
    (df["value"] <= df["value"].quantile(0.975))
]


def draw_line_plot():
    df_line = df.copy()

    # Configurar el lienzo
    fig, ax = plt.subplots(figsize=(16, 6))
    ax.plot(df_line.index, df_line["value"], color="red", linewidth=1)

    # Títulos y etiquetas exactas
    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    ax.set_xlabel("Date")
    ax.set_ylabel("Page Views")

    fig.savefig("line_plot.png")
    return fig


def draw_bar_plot():
    df_bar = df.copy()

    # Crear columnas de año y nombre de mes
    df_bar["year"] = df_bar.index.year
    df_bar["month"] = df_bar.index.month_name()

    # Definir el orden estricto de los meses
    months_order = [
        "January", "February", "March", "April",
        "May", "June", "July", "August",
        "September", "October", "November", "December"
    ]
    
    # CORRECCIÓN: Convertir la columna 'month' en categórica con orden antes de agrupar
    df_bar["month"] = pd.Categorical(df_bar["month"], categories=months_order, ordered=True)

    # Agrupar por año y mes, calculando el promedio (observed=False mantiene la estructura)
    df_bar_pivot = df_bar.groupby(["year", "month"], observed=False)["value"].mean().unstack()

    # Dibujar el gráfico a partir del pivot ordenado
    fig = df_bar_pivot.plot(kind="bar", figsize=(10, 8)).get_figure()
    ax = fig.gca()

    # Asignar etiquetas directo al objeto ax
    ax.set_xlabel("Years")
    ax.set_ylabel("Average Page Views")
    ax.legend(title="Months")

    fig.savefig("bar_plot.png")
    return fig


def draw_box_plot():
    df_box = df.copy()
    df_box.reset_index(inplace=True)

    # Extraer componentes de fecha
    df_box["year"] = df_box["date"].dt.year
    df_box["month"] = df_box["date"].dt.strftime("%b")  # 'Jan', 'Feb', etc.

    # Configurar paneles lado a lado
    fig, axes = plt.subplots(1, 2, figsize=(20, 6))

    # Primer gráfico: Tendencia anual
    sns.boxplot(x="year", y="value", data=df_box, ax=axes[0])
    axes[0].set_title("Year-wise Box Plot (Trend)")
    axes[0].set_xlabel("Year")
    axes[0].set_ylabel("Page Views")

    # Forzar el orden cronológico de los meses abreviados para Seaborn
    months_short_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    # Segundo gráfico: Estacionalidad mensual
    sns.boxplot(x="month", y="value", data=df_box, ax=axes[1], order=months_short_order)
    axes[1].set_title("Month-wise Box Plot (Seasonality)")
    axes[1].set_xlabel("Month")
    axes[1].set_ylabel("Page Views")

    fig.savefig("box_plot.png")
    return fig
