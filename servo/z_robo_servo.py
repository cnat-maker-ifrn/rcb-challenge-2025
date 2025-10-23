#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.iodevices import Ev3devSensor
from pybricks.ev3devices import (Motor, ColorSensor, InfraredSensor)
from pybricks.parameters import Port, Stop, Color
from pybricks.tools import wait
from pybricks.messaging import BluetoothMailboxClient, TextMailbox
import time


class RoboServo():
    def __init__(self):
        """Inicializa o robô EV3 Servo."""
        print("Iniciando configurações iniciais...")
        self.ev3 = EV3Brick()
        # ==== Bluetooth ====
        self.server_name = 'ev3dev-mestre'
        self.client = BluetoothMailboxClient()
        self.mbox = TextMailbox('greeting', self.client)
        # ==== Motores ====
        self.motor_garra=Motor(Port.A)
        self.motor_cen=Motor(Port.D)
        # self.motor_esq=Motor(Port.C)
        # self.motor_dir=Motor(Port.B)

        print("Motores configurados.")
        # ==== Sensores ===
        self.infra_cen=InfraredSensor(Port.S3)
        self.infra_dir=InfraredSensor(Port.S4)
        self.sen_hitech_cima=Ev3devSensor(Port.S2)
        self.sen_hitech=Ev3devSensor(Port.S1)
        # ==== Mapa hitech ====
        self.mapa_hitech_resgate = {
'vermelho': {
    'min': (0.34, 0.33, 0.24),
    'max': (0.55, 0.45, 0.34)
},
'amarelo': {
    'min': (0.36, 0.44, 0.16),
    'max': (0.48, 0.5, 0.26)
},
'verde': {
    'min': (0.23, 0.44, 0.33),
    'max': (0.28, 0.49, 0.36)
},
'azul': {
    'min': (0.12, 0.21, 0.2),
    'max': (0.26, 0.44, 0.45)
},
'branco': {
    'min': (0.29, 0.42, 0.33),
    'max': (0.33, 0.4600000000000001, 0.34)
},
'preto': {
    'min': (0.21, 0.39, 0.33),
    'max': (0.25, 0.42, 0.36)
},
        }
        self.mapa_hitech_lixao = {
'vermelho': {
    'min': (0.37, 0.22, 0.14),
    'max': (1.02, 0.6600000000000001, 0.49)
},
'amarelo': {
    'min': (0.41, 0.43, 0.08),
    'max': (0.5699999999999999, 0.54, 0.19)
},
'verde': {
    'min': (0.16, 0.44, 0.26),
    'max': (0.32, 0.62, 0.34)
},
'azul': {
    'min': (0.1, 0.34, 0.38),
    'max': (0.25, 0.43, 0.54)
},
'preto': {
    'min': (0.24, 0.4, 0.29),
    'max': (0.29, 0.47, 0.33)
},
        }

        print("Sensores configurados.")
        print("Configurações iniciais concluídas.")

    def conectar_ao_mestre(self):
        """Conecta ao robô mestre"""
        self.client.connect(self.server_name)

    def enviar_mensagem(self, mensagem):
        """Envia uma mensagem via Bluetooth."""
        self.mbox.send(mensagem)
        print("Mensagem enviada:", mensagem)
        wait(1000) # Espera 1 segundo para garantir o envio

    def esperar_ler_mensagem(self):
        """Espera e lê uma mensagem recebida via Bluetooth."""
        self.mbox.wait()
        mensagem = self.mbox.read()
        print("Mensagem recebida:", mensagem)
        return mensagem
            
    def ler_mensagem(self):
        """Lê uma mensagem recebida via Bluetooth."""
        mensagem = self.mbox.read()
        print("Mensagem recebida:", mensagem)
        return mensagem
    
    def infravermelho_cima(self):
        cima = self.infra_cima.distance()
        print('infra-cima',cima)
        return cima

    def infravermelhos(self):
        cen = self.infra_cen.distance()
        dir = self.infra_dir.distance()
        return cen, dir

    def hitech(self, area, debug=False):
        rgba = None
        if area == "resgate":
            rgba = self.sen_hitech.read("RAW")
        elif area == "lixao":
            rgba = self.sen_hitech_cima.read("RAW")

        # Leitura
        r, g, b, a = rgba

        if a == 0:
            a = 1  # Evita divisão por zero

        print(rgba)

        # Normalização
        rn = r / a
        gn = g / a
        bn = b / a

        # Mapeamento das cores do dicionário para os nomes do Pybricks
        cor_map = {
            'vermelho': Color.RED,
            'amarelo': Color.YELLOW,
            'verde': Color.GREEN,
            'azul': Color.BLUE,
            'branco': Color.WHITE,
            'preto': Color.BLACK,
        }

        # Escolhe qual mapa utilizar
        if (area=="lixao"):
            mapa_hitech = self.mapa_hitech_lixao
        elif (area == "resgate"):
            mapa_hitech = self.mapa_hitech_resgate

        for nome_cor, limites in mapa_hitech.items():
            min_r, min_g, min_b = limites['min']
            max_r, max_g, max_b = limites['max']

            if min_r <= rn <= max_r and min_g <= gn <= max_g and min_b <= bn <= max_b:
                cor_detectada = cor_map[nome_cor]
                if debug:
                    return (cor_detectada, (rn, gn, bn))
                return cor_detectada

        return None  
    
    def levantar_braco(self):
        self.motor_cen.run_until_stalled(-900, then=Stop.HOLD ,duty_limit=1200)

    def descer_braco(self):
        self.motor_cen.run_until_stalled(300, duty_limit=300)

    def fechar_garra(self):
        self.motor_garra.run_until_stalled(-900, duty_limit=50)

    def abrir_garra(self):
        self.motor_garra.run_until_stalled(900, duty_limit=50)

    def descer_mao_dir(self):
        self.motor_dir.run_until_stalled(-600, duty_limit=50)
    
    def levantar_mao_dir(self):
        self.motor_dir.run_until_stalled(600, duty_limit=50)
    
    def descer_mao_esq(self):
        self.motor_esq.run_until_stalled(600, duty_limit=50)
    
    def levantar_mao_esq(self):
        self.motor_esq.run_until_stalled(-600, duty_limit=50)
   

if __name__ == "__main__":
    robo = RoboServo()
    while True:
        print(robo.infravermelhos())

