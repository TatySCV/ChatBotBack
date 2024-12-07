import os
from groq import Groq
import mysql.connector

# Cliente de la API de Groq
client = Groq(api_key="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")

# Configuración de conexión a la base de datos
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "ia-chatbot",
}

# Estructura de la tabla en el modelo de datos de Django (DatosEjercicio)
TABLE_STRUCTURE = """
TABLA aplicacion_datosejercicio:
- id: INT, identificador único del registro.
- age: INT, edad del individuo.
- gender: VARCHAR, género del individuo.
- weight: FLOAT, peso en kilogramos.
- height: FLOAT, altura en metros.
- max_bpm: INT, frecuencia cardíaca máxima.
- avg_bpm: INT, frecuencia cardíaca promedio.
- resting_bpm: INT, frecuencia cardíaca en reposo.
- session_duration: FLOAT, duración de la sesión en horas.
- calories_burned: FLOAT, calorías quemadas durante el ejercicio.
- workout_type: VARCHAR, tipo de ejercicio realizado.
- fat_percentage: FLOAT, porcentaje de grasa corporal.
- water_intake: FLOAT, consumo de agua en litros.
- workout_frequency: INT, frecuencia de entrenamiento por semana.
- experience_level: VARCHAR, nivel de experiencia.
- bmi: FLOAT, índice de masa corporal.
"""


class Integration:
    def __init__(self):
        # Configura la clave API como una variable de entorno
        api_key = os.getenv(
            "GROQ_API_KEY", "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"
        )
        # Inicializa el cliente con la clave API
        self.client = Groq(api_key=api_key)

    def obtener_respuesta(self, mensaje, context):
        print(f"Mensaje recibido: {mensaje}")
        print(f"Contexto recibido: {context}")

        prompt = f"En base al siguiente contexto {context}, responde la pregunta dada por el usuario {mensaje}. Usa el contexto dado solo para entender y dar una respuesta apropiada. No uses el contexto para generar texto adicional. Responde la pregunta del usuario de la mejor manera posible. Responde de forma directa, si indicar que es una respuesta y no te dirijas como Usuario al usuario."

        try:
            # Llama al modelo Llama 3.1 8b 8192 para obtener la respuesta
            completion = self.client.chat.completions.create(
                model="llama3-8b-8192",  # Cambia al modelo correcto
                messages=[{"role": "user", "content": prompt}],
                max_tokens=200,
                temperature=0.7,
                top_p=1,
            )

            # Procesa el resultado y devuelve el texto generado
            respuesta = completion.choices[0].message.content
            print(f"Respuesta generada: {respuesta}")
            return respuesta.strip()
        except Exception as e:
            # Manejo de errores
            print(f"Error al obtener respuesta: {e}")
            return f"Error al obtener respuesta: {e}"

    def llama3_query(self, prompt):
        chat_completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama3-8b-8192",
        )
        try:
            # Retorna la respuesta generada por Llama 3
            return chat_completion.choices[0].message.content
        except IndexError:
            print("Error: No se recibió una respuesta válida.")
            return None

    def obtener_sql_query(self, question, context):
        prompt = f"""De acuerdo a la siguiente estructura de tablas:
        {TABLE_STRUCTURE}
        El historial de conversación es:
        {context}
        Y de acuerdo a la siguiente pregunta en lenguaje natural:
        "{question}"
        
        Por favor, considera estas instrucciones específicas para generar la consulta SQL:
        1. Utiliza SOLO el comando SELECT. Evita cualquier otro comando (ej. DROP, ALTER, etc.).
        2. Las columnas y tablas deben ser EXACTAMENTE  como se describen. Ejemplo de columnas: aplicacion_datosejercicio.age, aplicacion_datosejercicio.calories_burned, etc.
        3. Para busqueda de texto, usa LIKE en lugar de =. Si la busqueda incluye multiples columnas, usa CONCAT_WS.
        4. Para búsquedas numéritcas o de promedios, utiliza funciones de agregación como AVG, COUNT, SUM cuando corresponda.
        5. Si es necesario contat filas utiliza COUNT(*) o COUNT(distinct...).
        6. Utiliza IFNULL para manejar valores nulos. Ejemplo: IFNULL(usuarios.nivel_experiencia, 'N/A').
        7. Limita los resultados a un máximo de 100 filas con el LIMIT 100.
        9. Para filtrar por género considera:
            -'M' para Masculino
            -'F' para Femenino
        10. Si necesitas filtrar los resultados, utiliza WHERE seguido de las condiciones correspondientes.
        11. Si necesitas combinar tablas, utiliza JOIN seguido de las tablas correspondientes.
        12. Si necesitas combinar condiciones, utiliza AND y OR según corresponda.
        13. Si necesitas buscar valores que estén entre un rango, utiliza BETWEEN seguido de los valores correspondientes.
        14. Usa los nombres de las columnas como estan definidas en el {TABLE_STRUCTURE}
        15. Devuelve solo la consulta SQL, sin ninguna otra información adicional.
        16. El formato correcto seria 
            SELECT columnas 
            FROM tabla
            WHERE condiciones 
            GROUP BY columnas 
            LIMIT 100;
        """
        try:
            response = self.llama3_query(prompt)
            # Elimina posibles espacios en blanco y líneas vacías innecesarias
            return response.strip()
        except Exception as e:
            print(f"Error al generar la consulta SQL: {e}")
            return ""

    def execute_sql(self, sql):
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql)
            results = cursor.fetchall()
            return results
        except mysql.connector.Error as e:
            print(
                f"Error al ejecutar la consulta SQL: {e.msg}, Código de error: {e.errno}"
            )
            return []
        except Exception as e:
            print(f"Error inesperado: {e}")
            return []
        finally:
            if "cursor" in locals():
                cursor.close()
            if "conn" in locals():
                conn.close()

    def obtener_respuesta_entendible(self, sql_results, question, context):
        if not sql_results:
            return "Lo siento, no encontré resultados para tu pregunta."

        prompt = f"""Dada la siguiente pregunta:
        "{question}"
        El historial de conversación es:
        {context}
        Y los datos resultantes de la consulta SQL:
        {sql_results}

        Proporciona una respuesta clara y concisa en lenguaje natural:
        """

        try:
            response = self.llama3_query(prompt)
            return (
                response.strip()
            )  # Asegúrate de que el SQL no tenga comillas invertidas aquí
        except Exception as e:
            print(f"Error al generar la consulta SQL: {e}")
            return ""

    def control(self, contexto, pregunta):
        sql_query = self.obtener_sql_query(pregunta, contexto)
        print(f"Consulta SQL generada: {sql_query}")

        sql_results = self.execute_sql(sql_query)
        # print(f"Resultados SQL: {sql_results}")

        respuesta_final = self.obtener_respuesta_entendible(
            sql_results, pregunta, contexto
        )
        print(f"Respuesta: {respuesta_final}")

        return respuesta_final
