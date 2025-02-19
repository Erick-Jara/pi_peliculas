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
            "Miercoles": "Wednesday",
            "Jueves": "Thursday",
            "Viernes": "Friday",
            "Sabado": "Saturday",
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
    
@app.get("/score_titulo") 
def score_titulo(titulo):
    
    try:
        # Cargar el dataset
        df = cargar_data()

        # Normalizar el título para evitar problemas de mayúsculas y espacios
        titulo = titulo.strip().lower()

        # Filtrar la película en el DataFrame
        pelicula = df[df["title"].str.strip().str.lower() == titulo]

        if pelicula.empty:
            return f"Error: La película '{titulo}' no se encontró en el dataset."

        # Extraer valores de la primera coincidencia
        release_year = pelicula["release_year"].values[0]
        popularity = pelicula["popularity"].values[0]

        return f"La película '{titulo.title()}' fue estrenada en el año {release_year} con un score/popularidad de {popularity}."

    except Exception as e:
        return f"Error inesperado: Valor incorrecto"
    

@app.get("/votos_titulo") 
def votos_titulo(titulo):
        
    try:
        # Cargar el dataset
        df = cargar_data()

        # Normalizar el título para evitar problemas de mayúsculas y espacios
        titulo = titulo.strip().lower()

        # Filtrar la película en el DataFrame
        pelicula = df[df["title"].str.strip().str.lower() == titulo]
        

        if pelicula.empty:
            return f"Error: La película '{titulo}' no se encontró en el dataset."

        # Extraer valores de la primera coincidencia
        conteo_votos = pelicula["vote_count"].values[0]
        
        if conteo_votos < 2000:
            return f"Error: La película '{titulo}' no cumple con el minimo de 2000 valoraciones."
        
        promedio_votos = pelicula["vote_average"].values[0]

        return f"La película '{titulo.title()}' fue estrenada en el año {conteo_votos} con un score/popularidad de {promedio_votos}."

    except Exception as e:
        return f"Error inesperado: Valor incorrecto"

@app.get("/get_actor") 
def get_actor(actor):
    
    try:
        
        df = cargar_data()
        # Filtrar las películas donde aparece el actor (buscando en la columna 'actor')
        peliculas = df[df["actors"].str.contains(actor, case=False, na=False)]

        # Contar cuántas películas tiene
        total_peliculas = len(peliculas)

        # Si no aparece en ninguna película
        if total_peliculas == 0:
            return f"Error: El actor '{actor}' no se encontró en el dataset."

        # Sumar los valores de la columna 'return' y calcular el promedio
        suma_retorno = peliculas["return"].sum()
        promedio_retorno = suma_retorno / total_peliculas

        return (f"El actor '{actor}' ha participado de {total_peliculas} cantidad de filmaciones, "
                f"el mismo ha conseguido un retorno de {suma_retorno:.2f} "
                f" con un promedio de {promedio_retorno:.2f} por filmación")

    except Exception as e:
        return f"Error inesperado: valor incorrecto"


@app.get("/get_director")    
def get_director(director):
    
    try:
        # Cargar el dataset
        df = cargar_data()

        # Filtrar las películas dirigidas por el director
        peliculas = df[df["director"].str.contains(director, case=False, na=False)]

        # Si el director no tiene películas
        if peliculas.empty:
            return {"Error": f"El director '{director}' no se encontró en el dataset."}

        # Construir la estructura del diccionario
        resultado = {
            "director": director,
            "Pelicula": []
        }
        
        # Iterar sobre cada película encontrada
        for _, fila in peliculas.iterrows():
            resultado["Pelicula"].append({
                "nombre_pelicula": fila["title"],
                "lanzamiento": fila["release_date"],
                "retorno_individual": fila["return"],
                "costo en $": fila["budget"],
                "ganancia en $": fila["revenue"]
            })

        return resultado

    except Exception as e:
        return {"Error": f"Error inesperado: Valor incorrecto"}
