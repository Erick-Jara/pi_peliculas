from fastapi import FastAPI

import pandas as pd
import unidecode  # Para manejar tildes

app = FastAPI()

@app.get("/") 
def cantidad_filmaciones_mes(Mes):
    
    try:
        # Cargar dataset
        df = pd.read_csv("datos/dataset.csv")

        # Normalizar mes (quitar tildes y convertir a minúsculas)
        mes_normalizado = unidecode.unidecode(Mes.strip().lower())

        # Validar si el mes ingresado es correcto
        if mes_normalizado not in meses_traducidos:
            return "Error: Mes inválido. Usa un mes en español, por ejemplo: 'Enero', 'Febrero'."

        # Obtener el nombre del mes en inglés
        mes_ingles = meses_traducidos[mes_normalizado]

        # Contar cuántas películas fueron estrenadas en ese mes
        cantidad = df[df['month'] == mes_ingles].shape[0]

        return f"{cantidad} cantidad de películas fueron estrenadas en el mes de {Mes.capitalize()}."

    except FileNotFoundError:
        return "Error: No se encontró el archivo 'dataset.csv'. Verifica la ruta y el nombre del archivo."

    except pd.errors.EmptyDataError:
        return "Error: El archivo 'dataset.csv' está vacío."

    except KeyError:
        return "Error: La columna 'month' no existe en el dataset."

    except Exception as e:
        return f"Error inesperado: {str(e)}"
