#!/usr/bin/env pybricks-micropython

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, ColorSensor, UltrasonicSensor)
from pybricks.parameters import Port, Stop, Color
from pybricks.tools import wait
from math import pi
from random import randint
from pybricks.messaging import BluetoothMailboxServer, TextMailbox
import time
import json

class RoboMestre():
    def __init__(self):
        """Inicializa o robô EV3 Mestre."""
        print("Iniciando configurações iniciais...")
        self.ev3 = EV3Brick()
        # ==== Bluetooth ====
        self.server = BluetoothMailboxServer()
        self.mbox = TextMailbox('greeting', self.server)
        # ==== Motores ====
        self.motor_esq=Motor(Port.B)
        self.motor_dir=Motor(Port.A)
        self.motor_cen=Motor(Port.D)
        print("Motores configurados.")
        # ==== Sensores ===
        self.sen_dir_ext=ColorSensor(Port.S1)
        self.sen_esq_ext=ColorSensor(Port.S2)
        self.sen_dir_int=ColorSensor(Port.S3)
        self.sen_esq_int=ColorSensor(Port.S4)
        print("Sensores configurados.")
        # === Mapa cores ===
        self.mapa_esq = {
            'vermelho': {
    'min': (35, 6, 15),
    'max': (42, 9, 20)
},
            'amarelo': {
    'min': (28, 31, 24),
    'max': (42, 45, 38)
},
            'verde': {
    'min': (5, 14, 18),
    'max': (8, 22, 29)
},
            'azul': {
    'min': (6, 9, 32),
    'max': (9, 12, 45)
},
            'branco': {
    'min': (35, 40, 100),
    'max': (47, 54, 100)
},
            'preto': {
    'min': (3, 3, 9),
    'max': (16, 20, 21)
},
        }
        self.mapa_dir = {   
            'vermelho': {
    'min': (31, 7, 1),
    'max': (37, 8, 2)
},
            'amarelo': {
    'min': (26, 24, 4),
    'max': (37, 34, 6)
},
            'verde': {
    'min': (6, 11, 2),
    'max': (10, 17, 5)
},
            'azul': {
    'min': (7, 9, 5),
    'max': (10, 10, 7)
},
            'branco': {
    'min': (29, 27, 18),
    'max': (40, 38, 26)
},
            'preto': {
    'min': (5, 5, 0),
    'max': (9, 11, 4)
},
        }
        print("Configurações iniciais concluídas.")

    def seguir_linha(self, velocidade, limiar = 30, tempo_ms = None, cor=None):
        kp = 2  # Constante proporcional, ajuste conforme necessário

        if cor:
            if cor == "vermelho":
                cor = Color.RED
            elif cor == "verde":
                cor = Color.GREEN
            elif cor == "amarelo":
                cor = Color.YELLOW
            while True:
                esq = self.sen_esq_int.reflection()
                dir= self.sen_dir_int.reflection()
                esq_ext, dir_ext = self.sensores_externos()
                
                erro = dir - esq  # Se positivo, linha está mais à esquerda, então vira para a esquerda
                correcao = kp * erro

                vel_esq = velocidade - correcao
                vel_dir = velocidade + correcao

                self.motor_esq.run(vel_esq)
                self.motor_dir.run(vel_dir)

                if esq_ext == cor or dir_ext <= cor:
                    self.parar()
                    break
        elif tempo_ms:
            tempo_inicial = time.ticks_ms()
            while time.ticks_diff(time.ticks_ms(), tempo_inicial) < int(tempo_ms):
                esq = self.sen_esq_int.reflection()
                dir= self.sen_dir_int.reflection()
                
                erro = dir - esq  # Se positivo, linha está mais à esquerda, então vira para a esquerda
                correcao = kp * erro

                vel_esq = velocidade - correcao
                vel_dir = velocidade + correcao

                self.motor_esq.run(vel_esq)
                self.motor_dir.run(vel_dir)
            self.parar()
        else:
            while True:
                esq = self.sen_esq_int.reflection()
                dir= self.sen_dir_int.reflection()
                esq_ext = self.sen_esq_ext.reflection()
                dir_ext= self.sen_dir_ext.reflection()
                
                erro = dir - esq  # Se positivo, linha está mais à esquerda, então vira para a esquerda
                correcao = kp * erro

                vel_esq = velocidade - correcao
                vel_dir = velocidade + correcao

                self.motor_esq.run(vel_esq)
                self.motor_dir.run(vel_dir)

                if esq_ext <= limiar and dir_ext <= limiar:
                    self.parar()
                    break

    def sensores_externos(self):
        re, ge, be = self.sen_esq_ext.rgb()
        rd, gd, bd = self.sen_dir_ext.rgb()

        esq = ''
        dir = ''

        # Mapeamento das cores do dicionário para os nomes do Pybricks
        cor_map = {
            'vermelho': Color.RED,
            'amarelo': Color.YELLOW,
            'verde': Color.GREEN,
            'azul': Color.BLUE,
            'branco': Color.WHITE,
            'preto': Color.BLACK,
        }

        # Sensor esquerdo
        for cor in self.mapa_esq:
            min_vals = self.mapa_esq[cor]['min']
            max_vals = self.mapa_esq[cor]['max']
            if (min_vals[0] <= re <= max_vals[0] and
                min_vals[1] <= ge <= max_vals[1] and
                min_vals[2] <= be <= max_vals[2]):
                esq = cor_map[cor]
                break

        # Sensor direito
        for cor in self.mapa_dir:
            min_vals = self.mapa_dir[cor]['min']
            max_vals = self.mapa_dir[cor]['max']
            if (min_vals[0] <= rd <= max_vals[0] and
                min_vals[1] <= gd <= max_vals[1] and
                min_vals[2] <= bd <= max_vals[2]):
                dir = cor_map[cor]
                break

        print(esq, dir)
        return esq, dir

    def receber_conexoes(self, qtd=1):
        """Aguarda conexões Bluetooth."""
        print("Aguardando {} conexão...".format(qtd))
        self.server.wait_for_connection(count=qtd)
        print("Conexão estabelecida.")
        wait(2000)

    def enviar_mensagem(self, mensagem, tempo_ms=None):
        """Envia uma mensagem via Bluetooth."""
        self.mbox.send(mensagem)
        print("Mensagem enviada:", mensagem)
        if tempo_ms:
            wait(tempo_ms)

    def ler_mensagem(self):
        """Lê uma mensagem recebida via Bluetooth."""
        mensagem = self.mbox.read()
        print("Mensagem recebida:", mensagem)
        return mensagem
    
    def alinhar_frente(self):
        """
        Alinha o robô sobre a linha preto usando os sensores externos.
        O robô gira lentamente até que ambos sensores detectem preto.
        indo para frente quando for branco
        """
        print("Iniciando alinhamento com PRETO...")
        while True:
            cor_esq, cor_dir = self.sensores_externos()
            if cor_esq == Color.BLACK or cor_esq == Color.GREEN or cor_esq == Color.YELLOW and cor_dir == Color.BLACK or cor_esq == Color.GREEN or cor_dir == Color.YELLOW:
                self.parar()
                break
            elif cor_esq == Color.BLACK:
                self.motor_esq.run(0)
                self.motor_dir.run(300)
            elif cor_dir == Color.BLACK:
                self.motor_esq.run(300)
                self.motor_dir.run(0)
            else:
                self.motor_dir.run(300)
                self.motor_esq.run(300)
            wait(10)

    def alinhar_tras(self):
        """
        Alinha o robô sobre a linha preto usando os sensores externos.
        O robô gira lentamente até que ambos sensores detectem preto.
        indo para tras quando for branco
        """
        print("Iniciando alinhamento com preto...")
        while True:
            cor_esq, cor_dir = self.sensores_externos()
            if cor_esq == Color.BLACK or cor_dir == Color.BLACK:
                print("Alinhado sobre PRETO.")
                self.parar()
                break
            elif cor_esq == Color.BLACK:
                # Só o esquerdo detecta amarelo, gira levemente para a direita
                self.motor_esq.run(0)
                self.motor_dir.run(-300)
            elif cor_dir == Color.BLACK:
                # Só o direito detecta amarelo, gira levemente para a esquerda
                self.motor_esq.run(-300)
                self.motor_dir.run(0)
            else:
                self.motor_dir.run(-300)
                self.motor_esq.run(-300)

    def alinhar_reflexao_externa(self, limiar_esq, limiar_dir, tempo=100):
        """
        Alinha brevemente o robô usando os sensores externos com base na reflexão.
        Ajusta ambos os motores simultaneamente por até 'tempo' milissegundos.
        Ideal para pequenos ajustes finos em linhas de contraste.
        """
        print("Iniciando alinhamento rápido por reflexão (sensores externos)...")

        tempo_inicial = time.ticks_ms()

        while time.ticks_diff(time.ticks_ms(), tempo_inicial) < tempo:
            esq_ref = self.sen_esq_ext.reflection()
            dir_ref = self.sen_dir_ext.reflection()

            print("Reflexão E:", esq_ref, "| D:", dir_ref)

            erro_esq = limiar_esq - esq_ref
            erro_dir = limiar_dir - dir_ref

            # Se ambos estiverem próximos do ideal, parar
            if abs(erro_esq) <= 2 and abs(erro_dir) <= 2:
                print("Alinhado por reflexão.")
                break

            # Ajuste simultâneo proporcional (leve)
            vel_esq = erro_esq * 5   # ganho pequeno para suavizar
            vel_dir = erro_dir * 5

            # Limita as velocidades para evitar giros bruscos
            vel_esq = max(min(vel_esq, 300), -300)
            vel_dir = max(min(vel_dir, 300), -300)

            print("Vel E:", vel_esq, "| Vel D:", vel_dir)
            self.motor_esq.run(vel_esq)
            self.motor_dir.run(vel_dir)

            wait(1)

    def alinhar_reflexao_externa_invertido(self, limiar_esq, limiar_dir, tempo=100):
        """
        Alinha brevemente o robô usando os sensores externos com base na reflexão,
        mas com comportamento invertido: anda para FRENTE no branco e para TRÁS no preto.
        Ideal para situações onde o robô precisa reagir de forma oposta ao contraste da linha.
        """
        print("Iniciando alinhamento invertido por reflexão (sensores externos)...")

        tempo_inicial = time.ticks_ms()

        while time.ticks_diff(time.ticks_ms(), tempo_inicial) < tempo:
            esq_ref = self.sen_esq_ext.reflection()
            dir_ref = self.sen_dir_ext.reflection()

            print("Reflexão E:", esq_ref, "| D:", dir_ref)

            # Calcula erro em relação ao limiar
            erro_esq = limiar_esq - esq_ref
            erro_dir = limiar_dir - dir_ref

            # Se ambos estiverem próximos do limiar, parar
            if abs(erro_esq) <= 2 and abs(erro_dir) <= 2:
                print("Alinhado por reflexão (invertido).")
                break

            # Ajuste proporcional invertido:
            # Se o sensor lê valor maior (branco), deve andar pra frente.
            # Se lê valor menor (preto), deve andar pra trás.
            vel_esq = (-erro_esq) * 5   # inversão do sinal aqui
            vel_dir = (-erro_dir) * 5

            # Limita as velocidades
            vel_esq = max(min(vel_esq, 300), -300)
            vel_dir = max(min(vel_dir, 300), -300)

            print("Vel E:", vel_esq, "| Vel D:", vel_dir)
            self.motor_esq.run(vel_esq)
            self.motor_dir.run(vel_dir)

            wait(1)

    


    def medir_reflexao_interna(self):
        while True:
            esq_ref = self.sen_esq_int.reflection()
            dir_ref = self.sen_dir_int.reflection()
            print("Reflexão Esq:", esq_ref, " | Dir:", dir_ref)
            wait(500)

    def medir_reflexao_externa(self):
        while True:
            esq_ref = self.sen_esq_ext.reflection()
            dir_ref = self.sen_dir_ext.reflection()
            print("Reflexão Esq:", esq_ref, " | Dir:", dir_ref)
            wait(500)

    def alinhar_amarelo_reflexao(self, tempo_ms=2000):
        self.alinhar_reflexao_externa(limiar_esq=26, limiar_dir=16, tempo=tempo_ms)
    
    def alinhar_vermelho_reflexao(self):
        self.alinhar_reflexao_externa(limiar_esq=24, limiar_dir=15, tempo=2000)

    def alinhar_branco_reflexao(self, time_ms=2000):
        self.alinhar_reflexao_externa(limiar_esq=17, limiar_dir=17, tempo=time_ms)
    
    def alinhar_branco_reflexao_invertido(self, time_ms=2000):
        self.alinhar_reflexao_externa_invertido(limiar_esq=17, limiar_dir=17, tempo=time_ms)
    
    def alinhar_preto_reflexao(self, time_ms=2000):
        self.alinhar_reflexao_externa(limiar_esq=52, limiar_dir=32, tempo=time_ms)

    def andar(self, velocidade):
        """
        Move o robô para frente ou para trás na velocidade especificada.
        Args:
            velocidade (int): Velocidade para mover o robô. Valores positivos movem para frente, negativos para trás.
        """
        self.motor_esq.run(velocidade)
        self.motor_dir.run(velocidade)

    def parar(self):
        """
        Para todos os motores do robô, mantendo sua posição atual.
        Esta função ativa o modo 'hold' nos motores esquerdo, direito e central,
        impedindo que eles se movam e mantendo-os na posição em que estavam no momento da chamada.
        """
        self.motor_esq.hold()
        self.motor_dir.hold()
        self.motor_cen.hold()

    def andar_cm(self, distancia_cm, velocidade=200):
        """
        Move o robô para frente uma distância específica em centímetros.
        distancia_cm: Distância em centímetros para mover.
        velocidade: Velocidade dos motores.
        """
        diametro_roda = 4.8  # cm
        circunferencia = pi * diametro_roda
        rotacoes = distancia_cm / circunferencia
        
        angulo = rotacoes * 360
        
        self.motor_dir.reset_angle(0)
        self.motor_esq.reset_angle(0)
    
        self.motor_esq.run_angle(velocidade, angulo, wait=False)
        self.motor_dir.run_angle(velocidade, angulo, wait=True)
        
        self.motor_esq.hold()
        self.motor_dir.hold()

    def andar_lado_cm(self, distancia_cm, velocidade=200):
       
        diametro_roda = 4.8  # cm
        circunferencia = pi * diametro_roda
        rotacoes = abs(distancia_cm) / circunferencia
        angulo = rotacoes * 360

        # Reseta ângulo do motor de trás
        self.motor_cen.reset_angle(0)

        # Define direção (direita = positivo, esquerda = negativo)
        direcao = 1 if distancia_cm > 0 else -1

        # Compensação (20% da velocidade)
        velocidade_comp = int(velocidade * 0.10)

        # Se for para a direita
        if direcao > 0:
            self.motor_dir.run(-velocidade_comp)  # roda direita gira levemente para trás
        else:
            self.motor_esq.run(-velocidade_comp)  # roda esquerda gira levemente para trás

        # Move o motor central
        self.motor_cen.run_angle(velocidade * direcao, angulo, wait=True)

        # Para tudo no final
        self.motor_cen.hold()
        self.motor_esq.hold()
        self.motor_dir.hold()

    
    def girar_90_esquerda(self, velocidade):
        self.__girar_graus(-100, velocidade)
    
    def girar_90_direita(self, velocidade):
        self.__girar_graus(100, velocidade)

    def __girar_graus(self, angulo, velocidade):
        """
        Gira o robô em torno do seu eixo vertical.
        angulo: Ângulo em graus para girar (positivo para direita, negativo para esquerda).
        velocidade: Velocidade de rotação dos motores.
        """
        self.motor_dir.reset_angle(0)
        self.motor_esq.reset_angle(0)
        self.motor_cen.reset_angle(0)
    
        # Usa o valor absoluto do ângulo para cálculo
        angulo_abs = abs(angulo) * pi
        
        if angulo > 0:  # Direita (horário)
            self.motor_esq.run_angle(velocidade, angulo_abs, wait=False)
            self.motor_dir.run_angle(velocidade, -angulo_abs, wait=False)
            self.motor_cen.run_angle(velocidade, -angulo_abs, wait=True)
        else:  # Esquerda (anti-horário)
            self.motor_esq.run_angle(velocidade, -angulo_abs, wait=False)
            self.motor_dir.run_angle(velocidade, angulo_abs, wait=False)
            self.motor_cen.run_angle(velocidade, angulo_abs, wait=True)
        
        self.motor_esq.hold()
        self.motor_dir.hold()
        self.motor_cen.hold()

    def mapa_rgb(self, index):
        """
        Realiza a leitura dos valores RGB dos sensores esquerdo e direito por 5 segundos.

        Args:
            index (int): Índice da cor na lista ['vermelho', 'amarelo', 'verde', 'azul', 'branco', 'preto'].

        Returns:
            None

        Funcionalidade:
            - Coleta leituras RGB dos sensores esquerdo e direito durante 5 segundos.
            - Calcula os valores mínimo e máximo de cada canal RGB para cada sensor.
            - Cria um mapeamento dos valores RGB mínimos e máximos para a cor selecionada.
            - Exibe os resultados dos mapeamentos no console.
        """
        esq_list = []
        dir_list = []

        inicio = time.time()
        while time.time() - inicio < 10:
            esq = self.sen_esq_ext.rgb()
            dir = self.sen_dir_ext.rgb()
            print(esq, dir)
            esq_list.append(esq)
            dir_list.append(dir)
            wait(100)

        er_min, er_max = self.min_max_canal(esq_list, 0)
        eg_min, eg_max = self.min_max_canal(esq_list, 1)
        eb_min, eb_max = self.min_max_canal(esq_list, 2)

        dr_min, dr_max = self.min_max_canal(dir_list, 0)
        dg_min, dg_max = self.min_max_canal(dir_list, 1)
        db_min, db_max = self.min_max_canal(dir_list, 2)

        e_min = (er_min, eg_min, eb_min)
        e_max = (er_max, eg_max, eb_max)

        d_min = (dr_min, dg_min, db_min)
        d_max = (dr_max, dg_max, db_max)

        cores = ["vermelho", "amarelo", "verde", "azul", "branco", "preto"]
        cor = cores[index]
        
        print("Esquerda:")
        print("'" + cor + "': {")
        print("    'min': " + str(e_min) + ",")
        print("    'max': " + str(e_max))
        print("},")
        print("Direita:")
        print("'" + cor + "': {")
        print("    'min': " + str(d_min) + ",")
        print("    'max': " + str(d_max))
        print("},")


    def min_max_canal(self, lista, index):
        menor = lista[0][index]
        for i in range(len(lista)):
            if menor > lista[i][index]:
                menor = lista[i][index]
    
        maior = lista[0][index]
        for i in range(len(lista)):
            if lista[i][index] > maior:
                maior = lista[i][index]

        return menor, maior

    def sensores_reflexao(self):
        print(self.sen_esq_ext.reflection(), end=", ")
        print(self.sen_dir_ext.reflection())

if __name__ == "__main__":
    robo = RoboMestre()
    while True:
        robo.sensores_externos()
        # mover 10 cm para o lado e depois voltar 10 cm (executa uma vez)
        robo.andar_lado_cm(10, velocidade=200)
        wait(500)
        robo.andar_lado_cm(-10, velocidade=200)
        wait(500)
        break
