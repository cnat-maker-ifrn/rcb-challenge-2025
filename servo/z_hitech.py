#!/usr/bin/env pybricks-micropython
from z_robo_servo import RoboServo
import time

CORES = ["vermelho", "amarelo", "verde", "azul", "branco", "preto"]

if __name__ == "__main__":
    # =========================
    # SELECIONE A POSIÇÃO DA COR
    # =========================
    index = 0
    # area = "resgate"
    area = "lixao"
    # =========================
    # NÃO MEXER ABAIXo
    # =========================

    robo = RoboServo()
    robo.ev3.speaker.beep()

    inicio = time.time()

    # Inicializa os valores min e max com extremos
    min_r = min_g = min_b = 1.0
    max_r = max_g = max_b = 0.0

    while time.time() - inicio < 10:
        rgba = None
        if area == "resgate":
            rgba = robo.sen_hitech.read("RAW")
        elif area == "lixao":
            rgba = robo.sen_hitech_cima.read("RAW")
        r, g, b, a = rgba

        # Evita divisão por zero
        if a == 0:
            continue

        # Normaliza os valores
        rn = r / a
        gn = g / a
        bn = b / a

        print("RAW:", r, g, b, a, " → Normalizado:", round(rn, 2), round(gn, 2), round(bn, 2))

        # Atualiza os valores mínimos e máximos
        min_r = min(min_r, rn)
        min_g = min(min_g, gn)
        min_b = min(min_b, bn)

        max_r = max(max_r, rn)
        max_g = max(max_g, gn)
        max_b = max(max_b, bn)

    # Exibe o resultado final (normalizado)
    print("\n--- Resultado calibrado ---")
    print("'" + CORES[index] + "': {")
    print("    'min': " + str((round(min_r, 2), round(min_g, 2), round(min_b, 2))) + ",")
    print("    'max': " + str((round(max_r, 2), round(max_g, 2), round(max_b, 2))) )
    print("},")
    robo.ev3.speaker.beep()
