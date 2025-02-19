from fastapi import FastAPI

import pandas as pd


app = FastAPI()

#Cargar Dataset
def cargar_data():
    return pd.read_csv("datos/dataset.csv")

def obtener_meses():
   
    meses = {
        "Enero": "January", "Febrero": "February", "Marzo": "March", "Abril": "April",
        "Mayo": "May", "Junio": "June", "Julio": "July", "Agosto": "August",
        "Septiembre": "September", "Octubre": "October", "Noviembre": "November", "Diciembre": "December"
    }
    return meses


@app.get("/cantidad_filmaciones_mes") 
def cantidad_filmaciones_mes(mes):
    try:
        
        # Obtener diccionario de traducción
        meses = obtener_meses()
        
        #obtener dataset
        df = cargar_data()

        # (convertir primera letra en mayúscula, resto en minúscula)
        mes = mes.capitalize()
        
        # Obtener el nombre del mes en inglés
        mes_ingles = meses[mes]

        # Contar cuántas películas fueron estrenadas en ese mes
        cantidad = df[df['month'] == mes_ingles].shape[0]

        return f"{cantidad} cantidad de películas fueron estrenadas en el mes de {mes}."

    except Exception as e:
        return f"Error inesperado: Valor incorrecto"
    
def obtener_dias():
   
    dias = {"Lunes": "Monday",
            "Martes": "Tuesday",
            "Miércoles": "Wednesday",
            "Jueves": "Thursday",
            "Viernes": "Friday",
            "Sábado": "Saturday",
            "Domingo": "Sunday"
            }
    return dias

@app.get("/cantidad_filmaciones_dia") 

def cantidad_filmaciones_dia(dia):
    try:
        # Obtener diccionario de traducción
        dias = obtener_dias()
        
        #obtener dataset
        df = cargar_data()

        # (convertir primera letra en mayúscula, resto en minúscula)
        dia = dia.capitalize()
        
        # Obtener el nombre del mes en inglés
        dia_ingles = dias[dia]

        # Contar cuántas películas fueron estrenadas en ese mes
        cantidad = df[df['day'] == dia_ingles].shape[0]

        return f"{cantidad} cantidad de películas fueron estrenadas en los días {dia}."

    except Exception as e:
        return f"Error inesperado: Valor incorrecto"