# librerías
import pandas as pd
import matplotlib.pyplot as plt 
import numpy as np

# Se leen los datos del CSV 
datos = pd.read_csv('ventas_tienda.csv')
#----------------------------------------------------------------------------------------
# Primera gráfica: Producto vs cantidad vendida

ventas_por_producto = datos.groupby('producto')['cantidad'].sum()

plt.figure(figsize=(10,6))
ax = ventas_por_producto.plot(kind='bar', color='skyblue', edgecolor='black')

# Esto pone etiquetas numéricas sobre cada barra
for p in ax.patches:
    ax.annotate(f"{int(p.get_height())}", 
               (p.get_x() + p.get_width() / 2., p.get_height()), 
               ha='center', va='center', 
               xytext=(0, 5), 
               textcoords='offset points')

# Grafica
plt.xlabel('Producto', fontsize=12)
plt.ylabel('Cantidad Vendida', fontsize=12)
plt.title('Ventas por Producto', fontsize=16, fontweight='bold')
plt.xticks(rotation=0)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.figtext(0.5, 0.01, 
            "En los 6 meses se tiene que se han vendido aproximadamente 241 camisas, 164 pantalones y 211 zapatos. ", 
            ha="center", fontsize=10, style='italic', color='gray')
plt.tight_layout()
plt.show()
#-----------------------------------------------------------------------------------------------
# Segunda gráfica: Ventas por mes

orden_meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio']

datos['mes'] = pd.Categorical(datos['mes'], categories=orden_meses, ordered=True)

ventas_por_mes_producto = datos.groupby(['mes', 'producto'])['cantidad'].sum().unstack()

fig, ax = plt.subplots(figsize=(12, 6))
ventas_por_mes_producto.plot(kind='line', marker='o', ax=ax, colormap='tab10', linewidth=2)

# Esto pone etiquetas numéricas en cada punto
for producto in ventas_por_mes_producto.columns:
    for i, valor in enumerate(ventas_por_mes_producto[producto]):
        ax.text(x=i, y=valor + 1, s=f'{int(valor)}', ha='center', fontsize=9)

# Grafica
plt.xlabel('Mes', fontsize=12)
plt.ylabel('Cantidad Vendida', fontsize=12)
plt.title('Ventas por Mes y Producto', fontsize=16, fontweight='bold')
plt.xticks(range(len(orden_meses)), orden_meses, rotation=45)  # Aseguramos el orden correcto
plt.grid(axis='both', linestyle='--', alpha=0.7)
plt.legend(title='Producto', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.figtext(0.5, 0.01, 
            "La grafica muestra las ventas de los tres productos por mes. ", 
            ha="center", fontsize=10, style='italic', color='gray')
plt.tight_layout()
plt.show()
#------------------------------------------------------------------------------------------------
# Tabla resumen: Ingresos por producto 
if 'precio_unitario' in datos.columns:
    datos['ingresos'] = datos['cantidad'] * datos['precio_unitario']
    ingresos_por_producto = datos.groupby('producto')['ingresos'].sum().sort_values(ascending=False)

    # Crear DataFrame formateado
    tabla_resumen = pd.DataFrame({
        'Producto': ingresos_por_producto.index,
        'Ingresos Totales': ingresos_por_producto.map(lambda x: f"${x:,.2f}")
    })

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.axis('off')
    ax.set_title('Tabla Resumen: Ingresos por Producto', 
                 fontsize=14, fontweight='bold', pad=20, color='navy')

    table = ax.table(
        cellText=tabla_resumen.values,
        colLabels=tabla_resumen.columns,
        cellLoc='center',
        loc='center',
        colColours=['#f7f7f7', '#f7f7f7']
    )

    table.auto_set_font_size(False)
    table.set_fontsize(11)
    table.scale(1.2, 1.5)

    for (i, j), cell in table.get_celld().items():
        if i == 0:
            cell.set_text_props(fontsize=12, fontweight='bold', color='white')
            cell.set_facecolor('#4F81BD')
            cell.set_edgecolor('white')
        else:
            cell.set_facecolor('#E6E6E6' if i % 2 == 0 else 'white')
            cell.set_edgecolor('white')
            if j == 1:
                cell.set_text_props(style='italic', fontweight='bold')

    plt.figtext(0.5, 0.01, 
                "La siguiente tabla muestra los ingresos por producto de los 6 meses. ", 
                ha="center", fontsize=10, style='italic', color='gray')
    plt.tight_layout()
    plt.show()
else:
    print("Error: La columna 'precio_unitario' no existe en el dataset.")

# ---------------------------------------------------------------
# Cálculo extra 

datos['producto'] = datos['producto'].str.strip().str.capitalize()

# Calcula el total de unidades vendidas por mes
ventas_por_mes = datos.groupby('mes')['cantidad'].sum()

orden_meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio']
ventas_por_mes = ventas_por_mes.reindex(orden_meses)

# Esto detecta el mes con más ventas
mes_mayor_ventas = ventas_por_mes.idxmax()
unidades_mes_mayor = ventas_por_mes.max()

# Calcula lo s promedios por producto
ventas_totales = datos.groupby('producto')['cantidad'].sum()
promedios = (ventas_totales / 6).round(2)

colores = ['mediumseagreen' if mes == mes_mayor_ventas else 'lightgreen' for mes in ventas_por_mes.index]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle('Resumen de Ventas', fontsize=16, fontweight='bold')

# ----------------------------------------------------------------
# Subgráfico 1: Ventas por mes (todos los meses)
ax1.bar(ventas_por_mes.index, ventas_por_mes.values, color=colores, edgecolor='darkgreen')
ax1.set_title('Unidades Totales', fontsize=14)
ax1.set_ylabel('Total de Unidades Vendidas', fontsize=12)

for i, (mes, total) in enumerate(ventas_por_mes.items()):
    ax1.text(i, total + 3, f'{total}', ha='center', va='bottom', fontsize=10)

# -----------------------------------------------------------------
# Subgráfico 2: Promedio por producto
productos = list(promedios.index)
valores = list(promedios.values)

barras = ax2.bar(productos, valores, color=['lightblue', 'lightcoral', 'lightyellow'],
                 edgecolor=['blue', 'red', 'gold'], linewidth=2)

for bar in barras:
    altura = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., altura + 0.5,
             f'{altura:.2f}', ha='center', va='bottom', fontsize=11)

ax2.set_title('Promedio Mensual por Producto', fontsize=14)
ax2.set_ylabel('Unidades Vendidas / Mes', fontsize=12)
ax2.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()
