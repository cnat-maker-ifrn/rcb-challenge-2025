#!/usr/bin/env pybricks-micropython
"""Arquivo para ver o rgb dos sensores externos do robô EV3 Mestre."""
from z_robo_mestre import RoboMestre
from pybricks.parameters import Port, Stop, Color
from pybricks.tools import wait

if __name__ == "__main__":
    robo = RoboMestre()
    robo.medir_reflexao_externa()
    # robo.medir_reflexao_interna()
