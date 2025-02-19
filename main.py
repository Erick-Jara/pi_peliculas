from fastapi import FastAPI

import pandas as pd


app = FastAPI()

# Cargar dataset
df = pd.read_csv("datos/dataset.csv")

def obtener_meses():
   
    meses = {
        "Enero": "January", "Febrero": "February", "Marzo": "March", "Abril": "April",
        "Mayo": "May", "Junio": "June", "Julio": "July", "Agosto": "August",
        "Septiembre": "September", "Octubre": "October", "Noviembre": "November", "Diciembre": "December"
    }
    return meses


@app.get("/cantidad_filmaciones_mes") 
def cantidad_filmaciones_mes(Mes):
    
    try:
        
        # Obtener diccionario de traducción
        meses_traducidos = obtener_meses()

        # (convertir primera letra en mayúscula, resto en minúscula)
        mes_formateado = mes.capitalize()

        # Obtener el nombre del mes en inglés
        mes_ingles = meses_traducidos[mes_formateado]

        # Contar cuántas películas fueron estrenadas en ese mes
        cantidad = df[df['month'] == mes_ingles].shape[0]

        return f"{cantidad} cantidad de películas fueron estrenadas en el mes de {mes_formateado}."

    except Exception as e:
        return f"Error inesperado: {str(e)}"
