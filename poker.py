"""Juego de Póker"""
import csv
import logging
import cartas
import random

CSV_FILE1 = "estadisticas_usuarios.csv"
CSV_FILE2 = "partidas_usuarios.csv"

CARTAS = cartas.CARTAS
# for i in CARTAS:
#     print(i)

def repartir_cartas():
    """Función para repartir cartas a los jugadores."""
    # Otorga 5 cartas random a cada jugador
    mano_jugador1 = random.sample(CARTAS, 5)
    mano_maquina = random.sample(CARTAS, 5)
    print("Mano del Jugador 1:", mano_jugador1)
    print("Mano de la Máquina:", mano_maquina)