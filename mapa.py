import pandas as pd
import folium
from folium.plugins import MarkerCluster

# Cargar los datos desde el archivo Excel
archivo = r'C:\Users\DiegoSanabria\Documents\Desarrollo\FINAL.HACK\FINAL\DATOS_BUCARAMANGA.xlsx'
datos = pd.read_excel(archivo)

# Verificar las columnas del archivo
print("Columnas disponibles en los datos:")
print(datos.columns)

# Asumimos que las columnas de latitud y longitud están presentes y se llaman 'LATITUD' y 'LONGITUD'
# Cambia estos nombres si los encabezados son diferentes en tu archivo
col_lat = 'LATITUD'  # Reemplazar con el nombre correcto si es necesario
col_lon = 'LONGITUD'  # Reemplazar con el nombre correcto si es necesario

# Validar que las columnas de latitud y longitud existan
delitos_geolocalizados = datos[[col_lat, col_lon]].dropna()

# Crear un mapa base centrado en Bucaramanga, Santander
lat_bucaramanga = 7.119349
lon_bucaramanga = -73.122741
m = folium.Map(location=[lat_bucaramanga, lon_bucaramanga], zoom_start=13, tiles='CartoDB Positron', attr='Map tiles by Carto, under CC BY 3.0. Data by OpenStreetMap, under ODbL.')

# Crear un clúster de marcadores
marker_cluster = MarkerCluster().add_to(m)

# Agregar puntos de delitos al clúster (cambiando latitud por longitud y viceversa)
for _, row in delitos_geolocalizados.iterrows():
    folium.Marker(
        location=[row[col_lon], row[col_lat]],  # Intercambiar latitud y longitud
        popup=f"Latitud: {row[col_lon]}, Longitud: {row[col_lat]}",
        icon=folium.Icon(color='red', icon='info-sign')
    ).add_to(marker_cluster)

# Guardar el mapa en un archivo HTML
mapa_salida = r'C:\Users\DiegoSanabria\Documents\Desarrollo\FINAL.HACK\FINAL\mapa_delitos.html'
m.save(mapa_salida)

print(f"El mapa de delitos ha sido guardado en: {mapa_salida}")
