#!/usr/bin/env pybricks-micropython
from z_robo_mestre import RoboMestre
from pybricks.parameters import Port, Stop, Color
from pybricks.tools import wait
import time

class Estrategia():
    def __init__(self, robo: RoboMestre, velocidade=600, concluida=0):
        self.robo = robo

        self.velocidade = velocidade
        self.cores_disponiveis = []
        self.posicoes_containers = {}

        self.linha = 0 # Numero da linha
        self.coluna = 0 
        self.concluido = concluida

        self.pegou = False
        self.pegou_mas_nao_deixou = False
        self.voltando = False
        self.cor_atual = ""

        self.deixou_cubos_cor = {
            "amarelo": 0,
            "vermelho": 0,
            "verde": 0,
            "azul": 0,
            "preto": 0,
        }

    def inicio(self):
        primeiro_contanto_amarelo = True
        while True:
            esq, dir = self.robo.sensores_externos()
            if esq == Color.YELLOW and dir == Color.YELLOW:
                self.robo.parar()
                self.robo.alinhar_amarelo_reflexao()
                if primeiro_contanto_amarelo:
                    primeiro_contanto_amarelo = False
                    self.robo.andar_cm(-10, velocidade=self.velocidade)
                    self.robo.girar_90_direita(velocidade=self.velocidade)
                else:
                    self.robo.parar()
                    break
                
            elif esq == Color.RED or dir == Color.RED:
                self.robo.parar()
                self.robo.alinhar_vermelho_reflexao()
                primeiro_contanto_amarelo = False
                self.robo.andar_cm(-10, velocidade=self.velocidade)
                self.robo.girar_90_esquerda(velocidade=self.velocidade)

            elif esq == Color.WHITE or dir == Color.WHITE:
                self.robo.parar()
                self.robo.alinhar_branco_reflexao()
                primeiro_contanto_amarelo = False
                self.robo.andar_cm(-10, velocidade=self.velocidade)
                self.robo.girar_90_esquerda(velocidade=self.velocidade)

            elif dir == Color.BLUE and esq != Color.BLUE:
                self.robo.__girar_graus(-10, velocidade=self.velocidade)

            elif esq == Color.YELLOW and dir != Color.YELLOW:
                self.robo.__girar_graus(10, velocidade=self.velocidade)

            self.robo.andar(velocidade=self.velocidade)

        self.robo.alinhar_amarelo_reflexao()
        self.robo.andar_cm(2, velocidade=self.velocidade)
        self.robo.girar_90_esquerda(velocidade=self.velocidade)
        self.robo.andar_cm(-15, velocidade=self.velocidade)

        vel_base = 300
        Kp = 2  # ganho proporcional
        Kd = 1.5  # ganho derivativo
        limiar = 25  # média entre verde e amarelo
        erro_anterior = 0
        while True:
            ref = self.robo.sen_dir_int.reflection()  # sensor único

            # Sensores externos para parar no vermelho
            esq_ext, dir_ext = self.robo.sensores_externos()
            if esq_ext == Color.RED or dir_ext == Color.RED:
                self.robo.andar_cm(-10, velocidade=self.velocidade)
                self.robo.girar_90_esquerda(velocidade=self.velocidade)
                print(self.cores_disponiveis)
                break

            self.robo.enviar_mensagem("hitech-lixao")
            msg = self.robo.ler_mensagem()

            if self.pegou == True:
                if self.cor_atual == msg:
                    self.robo.andar_cm(-6, velocidade=self.velocidade)
                    self.robo.girar_90_direita(velocidade=200)
                    self.robo.andar_cm(-2, self.velocidade)
                    self.robo.alinhar_amarelo_reflexao()
                    
                    self.estrategia_deixar()
                    self.pegou = False
                    
                    self.robo.alinhar_amarelo_reflexao()
                    self.robo.andar_cm(2)
                    self.robo.girar_90_esquerda(velocidade=self.velocidade)
            else:
                if msg not in self.cores_disponiveis and msg != "desconhecida":
                    self.cores_disponiveis.append(msg)

            # Cálculo do erro e derivativo
            erro = limiar - ref
            derivativo = erro - erro_anterior
            ajuste = Kp * erro + Kd * derivativo
            erro_anterior = erro

            # Ajuste proporcional + derivativo nas velocidades
            vel_esq = vel_base + ajuste
            vel_dir = vel_base - ajuste

            # Limitar velocidade para segurança
            vel_esq = max(min(vel_esq, 500), -500)
            vel_dir = max(min(vel_dir, 500), -500)

            # Movimento dos motores
            self.robo.motor_esq.run(vel_esq)
            self.robo.motor_dir.run(vel_dir)

        while True:
            self.robo.andar(600)
            esq, dir = self.robo.sensores_externos()
            if esq == Color.WHITE or dir == Color.WHITE:
                self.robo.andar_cm(-10, velocidade=self.velocidade)
                self.robo.girar_90_direita(velocidade=self.velocidade)
                break

        while True:
            self.robo.andar(600)
            esq, dir = self.robo.sensores_externos()
            if esq == Color.RED or dir == Color.RED: 
                self.robo.parar()
                self.robo.alinhar_vermelho_reflexao()
                
                self.robo.andar_cm(((self.concluido * 31) + 8) * -1, velocidade=self.velocidade)
                self.robo.girar_90_esquerda(velocidade=self.velocidade)
                while True:
                    self.robo.andar(300)
                    esq, dir = self.robo.sensores_externos()
                    if esq == Color.WHITE or dir == Color.WHITE:
                        self.robo.alinhar_branco_reflexao(time_ms=4000)
                        self.robo.andar_cm(3)
                        return

    def voltar_para_a_proxima_coluna(self):      
        self.robo.andar_cm(-10, velocidade=self.velocidade)
        self.robo.__girar_graus(200, velocidade=self.velocidade)
        self.voltando = True
        self.concluido = self.concluido + 1

        while True:
            self.robo.seguir_linha(400)
            self.robo.andar_cm(3, velocidade=self.velocidade)
            esq, dir = self.robo.sensores_externos()
            if esq == Color.GREEN or dir == Color.GREEN or \
                esq == Color.BLUE or dir == Color.BLUE:
               
                self.robo.andar_cm(-3, velocidade=self.velocidade)
                self.robo.alinhar_branco_reflexao_invertido(time_ms=3000)
                self.robo.andar_cm(15, velocidade=self.velocidade)
                self.robo.girar_90_direita(velocidade=200)
                self.robo.andar_cm(31, velocidade=self.velocidade)
                self.robo.girar_90_direita(velocidade=200)
                # avançar até ver azul e então andar 3 cm
                while True:
                    print("LOPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP")
                    esq, dir = self.robo.sensores_externos()
                    if esq == Color.BLUE or dir == Color.BLUE or \
                        esq == Color.WHITE or dir == Color.WHITE:
                        self.robo.alinhar_frente()
                        break
                    self.robo.andar(velocidade=self.velocidade)
                    wait(50)

                self.robo.andar_cm(4, velocidade=self.velocidade)
                self.coluna = self.coluna + 1
                break
                
    def meio(self):
        self.linha=0
        self.voltando = False

        while self.pegou == False:
            print(self.pegou)
            self.robo.seguir_linha(300)
            self.robo.andar_cm(3)
            self.linha = self.linha + 1

            if self.linha == 4:
                self.voltar_para_a_proxima_coluna()
                self.linha = 0

                
            esq, dir = self.robo.sensores_externos()
            if esq == Color.GREEN or dir == Color.GREEN or \
                esq == Color.BLUE or dir == Color.BLUE:
                self.voltar_para_a_proxima_coluna()
                self.linha = 0

            else:
                self.robo.alinhar_preto_reflexao()


                self.robo.enviar_mensagem("tem-cubo-na-direita", tempo_ms=1000)
                msg = self.robo.ler_mensagem()
                if msg == "true":
                    self.robo.andar_cm(3)
                    self.robo.girar_90_direita(velocidade=200)
                    self.robo.andar_cm(1)
                    self.robo.alinhar_tras()
                    self.robo.alinhar_preto_reflexao()

                    # ========== Qual é a cor do cubo? ==========
                    pode_pegar_bloco = None
                    self.robo.andar_cm(5)
                    while True:
                        self.robo.enviar_mensagem("hitech-resgate")
                        msg = self.robo.ler_mensagem()                               
                        esq, dir = self.robo.sensores_externos()

                        if msg in self.cores_disponiveis:
                            self.cor_atual = msg
                            pode_pegar_bloco = True
                            break
                        else:
                            if msg == "branco":
                                self.robo.ev3.speaker.beep()
                                cronometro = time.ticks_ms()
                                while time.ticks_diff(time.ticks_ms(), cronometro) < 3000:
                                    self.robo.ev3.light.on(Color.ORANGE)
                                    wait(50)
                                    self.robo.ev3.light.off()
                                pode_pegar_bloco = False
                                break

                        if esq == Color.BLACK or dir == Color.BLACK:
                            self.robo.parar()
                            pode_pegar_bloco = False
                            break

                        self.robo.andar(velocidade=-75)
                    self.robo.alinhar_tras()
                    self.robo.alinhar_preto_reflexao()

                    if pode_pegar_bloco:
                        self.robo.andar_cm(5)
                        self.robo.enviar_mensagem("pegar-cubo")
                        while True:
                            msg = self.robo.ler_mensagem()
                            if msg == "pegar-cubo-concluido":
                                self.pegou = True
                                break
                        self.robo.andar_cm(-5)
                    else:
                        self.pegou = False




                    self.robo.andar_cm(2)
                    self.robo.girar_90_esquerda(velocidade=200)
                    self.robo.andar_cm(2)
                    self.robo.alinhar_preto_reflexao()

                if self.pegou == False: # Pois ele pode ter pego na direita
                    # ========== Existe cubo na frente? ==========
                    self.robo.andar_cm(5, velocidade=self.velocidade)
                    existe_bloco = None
                    confirma = None
                    while True:
                        esq, dir = self.robo.sensores_externos()
                        self.robo.enviar_mensagem("tem-cubo-na-frente")
                        msg = self.robo.ler_mensagem() 
                        if msg == 'true':
                            existe_bloco = True
                            break

                        if esq == Color.BLACK or dir == Color.BLACK:
                            existe_bloco = False
                            confirma = True
                            break
                        
                        self.robo.andar(velocidade=-75)
                    self.robo.alinhar_tras()

                    self.robo.alinhar_preto_reflexao(time_ms=3000)
                    if confirma:
                        self.robo.andar_cm(7, velocidade=self.velocidade)
                    else:
                        if existe_bloco:
                            pode_pegar_bloco = None
                            # ========== Qual é a cor do cubo? ==========
                            self.robo.andar_cm(5, velocidade=self.velocidade)
                            while True:
                                self.robo.enviar_mensagem("hitech-resgate")
                                msg = self.robo.ler_mensagem()                               
                                esq, dir = self.robo.sensores_externos()

                                if msg in self.cores_disponiveis:
                                    self.cor_atual = msg
                                    pode_pegar_bloco = True
                                    break
                                else:
                                    if msg == "branco":
                                        self.robo.ev3.speaker.beep()
                                        cronometro = time.ticks_ms()
                                        while time.ticks_diff(time.ticks_ms(), cronometro) < 3000:
                                            self.robo.ev3.light.on(Color.ORANGE)
                                            wait(50)
                                            self.robo.ev3.light.off()
                                        pode_pegar_bloco = False

                                if esq == Color.BLACK or dir == Color.BLACK:
                                    self.robo.parar()
                                    pode_pegar_bloco = False
                                    break

                                self.robo.andar(velocidade=-70)

                         
                            self.robo.alinhar_tras()
                            self.robo.alinhar_preto_reflexao(time_ms=2000)
                            if pode_pegar_bloco == False:
                                self.concluido = self.concluido + 1
                                self.robo.__girar_graus(200, velocidade=200)
                                self.voltando = True
                                while True:
                                    self.robo.seguir_linha(250)
                                    self.robo.andar_cm(7, velocidade=self.velocidade)
                                    esq, dir = self.robo.sensores_externos()
                                    if esq == Color.GREEN or dir == Color.GREEN or \
                                        esq == Color.BLUE or dir == Color.BLUE:
                                        
                                        self.robo.andar_cm(-3)
                                        self.robo.alinhar_branco_reflexao()
                                        self.robo.andar_cm(15, 300)
                                        self.robo.girar_90_direita(velocidade=self.velocidade)
                                        self.robo.andar_cm(31, 300)
                                        self.robo.girar_90_direita(velocidade=self.velocidade)
                                        # avançar até ver aproxima linha
                                        while True:
                                            esq, dir = self.robo.sensores_externos()
                                            if esq == Color.BLUE or dir == Color.BLUE:
                                                self.robo.parar()
                                                break
                                            self.robo.andar(velocidade=200)
                                            wait(50)

                                        self.robo.andar_cm(3)
                                        self.coluna = self.coluna + 1
                                        break
                            else: # =========== Pegar o cubo ===================                
                                self.robo.andar_cm(5)
                                self.robo.enviar_mensagem("pegar-cubo")
                                while True:
                                    msg = self.robo.ler_mensagem()
                                    if msg == "pegar-cubo-concluido":
                                        self.pegou = True
                                        break
        self.robo.girar_90_esquerda(velocidade=200)
        self.robo.girar_90_esquerda(velocidade=200)
        
        while True:
            self.robo.seguir_linha(self.velocidade)
            self.robo.andar_cm(7, velocidade=self.velocidade)
            esq, dir = self.robo.sensores_externos()
            if esq == Color.GREEN or dir == Color.GREEN or \
                esq == Color.BLUE or dir == Color.BLUE:
                self.robo.parar()
                self.robo.andar_cm(5, velocidade=self.velocidade)
                break

    def estrategia_deixar(self):
        cor = self.cor_atual
        vezes = self.deixou_cubos_cor[cor]
        if vezes == 0:
            # primeira vez que vai deixar essa cor

            self.robo.girar_90_esquerda(200)
            while True: 
                    self.robo.enviar_mensagem("container-dir")
                    msg = self.robo.ler_mensagem()
                    self.robo.andar_cm(1)   
                    if msg == "false":
                        self.robo.parar()
                        break
                       
            self.robo.andar_cm(-5)
            self.robo.girar_90_direita(velocidade=200)

            self.robo.alinhar_amarelo_reflexao(tempo_ms=3000)
            self.robo.andar_cm(6)
            self.robo.enviar_mensagem("deixar-cubo")

            while True:
                resposta = self.robo.ler_mensagem()
                if resposta == "deixar-cubo-concluido":
                    self.pegou = False
                    break
                wait(100)

            self.robo.andar_cm(-5)
            self.deixou_cubos_cor[cor] = 1

        elif vezes == 1:
            # Segunda vez que vai deixar essa cor

            self.robo.girar_90_esquerda(200)
            while True: 
                    self.robo.enviar_mensagem("container-dir")
                    msg = self.robo.ler_mensagem()
                    self.robo.andar_cm(1)   
                    if msg == "false":
                        self.robo.parar()
                        break
                       
            self.robo.andar_cm(-11)
            self.robo.girar_90_direita(velocidade=200)

            self.robo.alinhar_amarelo_reflexao(tempo_ms=3000)
            self.robo.andar_cm(6)
            self.robo.enviar_mensagem("deixar-cubo")

            while True:
                resposta = self.robo.ler_mensagem()
                if resposta == "deixar-cubo-concluido":
                    self.pegou = False
                    break
                wait(100)

            self.robo.andar_cm(-5)
            self.deixou_cubos_cor[cor] = 2
            
        elif vezes == 2:
            self.robo.girar_90_esquerda(200)
            while True: 
                    self.robo.enviar_mensagem("container-dir")
                    msg = self.robo.ler_mensagem()
                    self.robo.andar_cm(1)   
                    if msg == "false":
                        self.robo.parar()
                        break
                       
            self.robo.andar_cm(-16)
            self.robo.girar_90_direita(velocidade=200)

            self.robo.alinhar_amarelo_reflexao(tempo_ms=3000)
            self.robo.andar_cm(6)
            self.robo.enviar_mensagem("deixar-cubo")

            while True:
                resposta = self.robo.ler_mensagem()
                if resposta == "deixar-cubo-concluido":
                    self.pegou = False
                    break
                wait(100)

            self.robo.andar_cm(-5)

            self.robo.andar_cm(-5)
            self.deixou_cubos_cor[cor] = 3
            return True