from django.db import models


class DatosEjercicio(models.Model):
    # Campos del ejercicio
    age = models.IntegerField(help_text="Edad del individuo.")
    gender = models.CharField(
        max_length=10,
        choices=[("M", "Masculino"), ("F", "Femenino")],
        help_text="Género del individuo.",
    )
    weight = models.FloatField(help_text="Peso en kilogramos.")
    height = models.FloatField(help_text="Altura en metros.")
    max_bpm = models.IntegerField(help_text="Frecuencia cardíaca máxima.")
    avg_bpm = models.IntegerField(help_text="Frecuencia cardíaca promedio.")
    resting_bpm = models.IntegerField(help_text="Frecuencia cardíaca en reposo.")
    session_duration = models.FloatField(help_text="Duración de la sesión en horas.")
    calories_burned = models.FloatField(
        help_text="Calorías quemadas durante el ejercicio."
    )
    workout_type = models.CharField(
        max_length=50, help_text="Tipo de ejercicio realizado."
    )
    fat_percentage = models.FloatField(help_text="Porcentaje de grasa corporal.")
    water_intake = models.FloatField(help_text="Consumo de agua en litros.")
    workout_frequency = models.IntegerField(
        help_text="Frecuencia de entrenamiento por semana."
    )
    experience_level = models.CharField(
        max_length=50,
        choices=[
            ("Principiante", "Principiante"),
            ("Intermedio", "Intermedio"),
            ("Avanzado", "Avanzado"),
        ],
        help_text="Nivel de experiencia.",
    )
    bmi = models.FloatField(
        help_text="Índice de Masa Corporal proporcionado en el CSV."
    )

    def __str__(self):
        return f"Ejercicio registrado - Tipo: {self.workout_type}, Duración: {self.session_duration} horas"

    class Meta:
        db_table = "aplicacion_datosejercicio"
