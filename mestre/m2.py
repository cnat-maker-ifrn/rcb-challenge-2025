#!/usr/bin/env pybricks-micropython
"""Arquivo principal para o robô EV3 Mestre."""
from z_robo_mestre import RoboMestre
from z_estrategia import Estrategia
from pybricks.parameters import Color
from pybricks.tools import wait
import time

if __name__ == "__main__":
    robo = RoboMestre()
    robo.receber_conexoes()
    estrategia = Estrategia(robo, concluida=2)
    while True:
        estrategia.inicio()
        estrategia.meio()
