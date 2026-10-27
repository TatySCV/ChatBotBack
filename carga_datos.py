import csv
from django.core.exceptions import ValidationError
from aplicacion.models import DatosEjercicio  # Reemplaza "aplicacion" con el nombre de tu aplicación

def cargar_datos_csv(ruta_archivo_csv):
    # Definir el mapeo de los valores numéricos a los niveles de experiencia
    experiencia_map = {
        '1': 'Principiante',
        '2': 'Intermedio',
        '3': 'Avanzado'
    }
    
    with open(ruta_archivo_csv, mode='r', encoding='utf-8') as archivo:
        lector_csv = csv.DictReader(archivo)
        
        for fila in lector_csv:
            # Convierte los datos de cada fila
            try:
                # Mapear los valores numéricos de experiencia a los valores de texto
                experiencia = experiencia_map.get(fila['Experience_Level'], 'Principiante')  # Default to 'Principiante' si no está en el mapeo

                # Crear un nuevo registro en la base de datos
                datos_ejercicio = DatosEjercicio(
                    age=int(fila['Age']),  # Convertir a entero
                    gender='M' if fila['Gender'] == 'Male' else 'F',  # Cambiar valores a 'M' o 'F'
                    weight=float(fila['Weight (kg)']),  # Convertir a float
                    height=float(fila['Height (m)']),  # Convertir a float
                    max_bpm=int(fila['Max_BPM']),  # Convertir a entero
                    avg_bpm=int(fila['Avg_BPM']),  # Convertir a entero
                    resting_bpm=int(fila['Resting_BPM']),  # Convertir a entero
                    session_duration=float(fila['Session_Duration (hours)']),  # Convertir a float
                    calories_burned=float(fila['Calories_Burned']),  # Convertir a float
                    workout_type=fila['Workout_Type'],  # Texto
                    fat_percentage=float(fila['Fat_Percentage']),  # Convertir a float
                    water_intake=float(fila['Water_Intake (liters)']),  # Convertir a float
                    workout_frequency=int(fila['Workout_Frequency (days/week)']),  # Convertir a entero
                    experience_level=experiencia,  # Asignar el valor mapeado
                    bmi=float(fila['BMI']),  # Convertir a float
                )
                # Guardar los datos en la base de datos
                datos_ejercicio.save()
                print(f"Datos de ejercicio para {fila['Gender']} cargados correctamente.")
            
            except ValidationError as e:
                print(f"Error en los datos: {e}")
            except Exception as e:
                print(f"Error al procesar la fila: {e}")