import os
from groq import Groq


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
        
        prompt = f'En base al siguiente contexto {context}, responde la pregunta dada por el usuario {mensaje}. Usa el contexto dado solo para entender y dar una respuesta apropiada. No uses el contexto para generar texto adicional. Responde la pregunta del usuario de la mejor manera posible. Responde de forma directa, si indicar que es una respuesta y no te dirijas como Usuario al usuario.'

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
