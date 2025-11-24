"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""

# pylint: disable=import-outside-toplevel

import pandas as pd
import re
def pregunta_01():
    """
    Construya y retorne un dataframe de Pandas a partir del archivo
    'files/input/clusters_report.txt'. Los requerimientos son los siguientes:

    - El dataframe tiene la misma estructura que el archivo original.
    - Los nombres de las columnas deben ser en minusculas, reemplazando los
      espacios por guiones bajos.
    - Las palabras clave deben estar separadas por coma y con un solo
      espacio entre palabra y palabra.
    """
    # Leer el archivo utilizando pandas read_fwf() con especificación de anchos fijos
    df = pd.read_fwf("files/input/clusters_report.txt", 
                     colspecs="infer", 
                     widths=[9, 16, 16, 80], 
                     header=None, 
                     names=["cluster", "cantidad_de_palabras_clave", "porcentaje_de_palabras_clave", "principales_palabras_clave"]
                    ).drop(index={0, 1, 2}).ffill()  # Eliminar filas no deseadas y rellenar valores nulos

    # Convertir los nombres de las columnas a minúsculas y reemplazar espacios por guiones bajos
    df.columns = df.columns.str.lower().str.replace(' ', '_')

    # Limpiar la columna 'porcentaje_de_palabras_clave' para poder convertirla a float
    df['porcentaje_de_palabras_clave'] = df['porcentaje_de_palabras_clave'].replace({'%': '', ',': '.'}, regex=True).astype(float)

    # Convertir los tipos de datos
    df = df.astype({
        "cluster": int, 
        "cantidad_de_palabras_clave": int, 
        "porcentaje_de_palabras_clave": float,
        "principales_palabras_clave": str
    })
    
    # Agrupar por las tres columnas y concatenar las principales palabras clave en una cadena separada por espacio
    df = df.groupby(["cluster", "cantidad_de_palabras_clave", "porcentaje_de_palabras_clave"])["principales_palabras_clave"].agg(' '.join).reset_index()
    
    # Redondear valores a 1 decimal en "porcentaje_de_palabras_clave"
    df["porcentaje_de_palabras_clave"] = df["porcentaje_de_palabras_clave"].round(1)

    # Limpiar los espacios en blanco adicionales y los puntos al final de las cadenas en "principales_palabras_clave"
    df["principales_palabras_clave"] = df["principales_palabras_clave"].apply(lambda x: re.sub(r'\s+', ' ', x).rstrip("."))

    return df
    
