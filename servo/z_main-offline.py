#!/usr/bin/env pybricks-micropython
from z_robo_servo import RoboServo
from pybricks.parameters import Stop, Color
from pybricks.tools import wait


robo = RoboServo()
while True:
    # ====================================================
    # PARA TESTES
    # ====================================================
    # msg = "container-dir"
    # msg = "container-cor"
    # msg = "tem-cubo-na-frente"
    # msg = "tem-cubo-na-direita"
    # msg = "tem-cubo-na-frente-direita"

    # msg = "hitech-resgate"
    msg = "hitech-resgate"

    # msg = "pegar-cubo"
    # msg = "deixar-cubo"

    # msg = "mao_esq_descer"
    # msg = "mao_dir_descer"
    # msg = "mao_esq_levantar"
    # msg = "mao_dir_levantar"

    # msg = "sensor"
    # msg = "deixar"
    # msg = "verificar_se_cubo_deixou"
    # msg = "cubos"
    # ====================================================

    if msg == "container-dir":
        _, dir = robo.infravermelhos()
        print(_, dir)
        resposta = 'false'
        if dir < 25: # Container preto
            resposta = "true"
        robo.enviar_mensagem(resposta)

    elif msg == "container-cor":
        cor_detectada = robo.hitech(area="lixao")
        print(cor_detectada)
        
        if cor_detectada == Color.RED:
            resposta = "vermelho"
        elif cor_detectada == Color.BLUE:
            resposta = "azul"
        elif cor_detectada == Color.GREEN:
            resposta = "verde"
        elif cor_detectada == Color.YELLOW:
            resposta = "amarelo"
        elif cor_detectada == Color.BLACK:
            resposta = "preto"
        else:
            resposta = "desconhecida"

        robo.enviar_mensagem(resposta)

    # --- Comando "tem-cubo-na-frente" ---
    elif msg == "tem-cubo-na-frente":
        cen, _ = robo.infravermelhos()
        print(cen, _)
        if cen < 30:
            robo.enviar_mensagem("true")
        else:
            robo.enviar_mensagem("false")

    # --- Comando "tem-cubo-na-direita" ---
    elif msg == "tem-cubo-na-direita":
        _, dir = robo.infravermelhos()
        print(_, dir)
        if dir < 25: # Menor pois o sensor direito está muito proximo ao cubo
            robo.enviar_mensagem("true")
        else:
            robo.enviar_mensagem("false")

    # --- Comando "tem-cubo-na-frente-direita" ---
    elif msg == "tem-cubo-na-frente-direita":
        cen, dir = robo.infravermelhos()
        resposta = 'falseee'   # garante que sempre existe
        if cen < 30 or dir < 25:
            if cen < dir:
                resposta = "frente"
            else:
                resposta = "direita"
        robo.enviar_mensagem(resposta)

    # --- Comando "hitech-resgate" ---
    elif msg == 'hitech-resgate':
        cor_detectada = robo.hitech(area="resgate")
        print(cor_detectada)
        
        # Transforma o objeto Color em string legível
        if cor_detectada == Color.RED:
            resposta = "vermelho"
        elif cor_detectada == Color.BLUE:
            resposta = "azul"
        elif cor_detectada == Color.GREEN:
            resposta = "verde"
        elif cor_detectada == Color.YELLOW:
            resposta = "amarelo"
        elif cor_detectada == Color.WHITE:
            resposta = "branco"
        elif cor_detectada == Color.BLACK:
            resposta = "preto"
        else:
            resposta = "desconhecida"

        robo.enviar_mensagem(resposta)

    # --- Comando "hitech-lixao" ---
    elif msg == "hitech-lixao":
        cor_detectada = robo.hitech(area="lixao")

        print(cor_detectada)
        
        # Transforma o objeto Color em string legível
        if cor_detectada == Color.RED:
            resposta = "vermelho"
        elif cor_detectada == Color.BLUE:
            resposta = "azul"
        elif cor_detectada == Color.GREEN:
            resposta = "verde"
        elif cor_detectada == Color.YELLOW:
            resposta = "amarelo"
        elif cor_detectada == Color.WHITE:
            resposta = "branco"
        elif cor_detectada == Color.BLACK:
            resposta = "preto"
        else:
            resposta = "desconhecida"

        robo.enviar_mensagem(resposta)

    # --- Comando "Sensor" ---
    elif (msg == 'sensor'):
        cen, dir = robo.infravermelhos()
        resposta = ''   # garante que sempre existe
        if cen < 17:
            resposta = "tem-cubo"
        else:
            resposta = "nao-tem-cubo"
        robo.enviar_mensagem(resposta)
    
    elif (msg == 'sensor-direito'):
        cen, dir = robo.infravermelhos()
        resposta = ''   # garante que sempre existe
        if cen < 3:
            resposta = "tem-cubo"
        else:
            resposta = "nao-tem-cubo"
        robo.enviar_mensagem(resposta)
    
    # --- Comando "deixar" ---
    elif (msg == 'deixar'):
        cen, dir = robo.infravermelhos()
        resposta = ''   # garante que sempre existe
        if cen < 30:
            resposta = "parar"
        else:
            resposta = "continuar"
        robo.enviar_mensagem(resposta)

    elif (msg == 'verificar_se_cubo_deixou'):
        cima = robo.infravermelho_cima()
        resposta = ''   # garante que sempre existe
        if cima < 45:
            resposta = "tem_cubo_no_local"
        else:
            resposta = "N_tem_cubo_no_local"
        robo.enviar_mensagem(resposta)

    # --- Comando "cubos" ---
    elif (msg == 'cubos'):
        cen, dir = robo.infravermelhos()
        resposta = ''   # corrigido (antes estava "reposta")
        if cen < 40 or dir < 40:
            if cen < dir:
                resposta = "frente"
            else:
                resposta = "direita"
        else:
            resposta = "vazio"
        robo.enviar_mensagem(resposta)
    

    # --- Comando "pegar-cubo" ---
    elif (msg == "pegar-cubo"):
        robo.descer_braco()
        robo.fechar_garra()
        robo.levantar_braco()
        resposta = "pegar-cubo-concluido"
        robo.enviar_mensagem(resposta)

    # --- Comando "deixar-cubo" ---
    elif (msg == "deixar-cubo"):
        robo.descer_braco()
        
        robo.abrir_garra()
        robo.levantar_braco()
        resposta = "deixar-cubo-concluido"
        robo.enviar_mensagem(resposta)
    
    elif (msg == "mao_esq_descer"):
        robo.descer_mao_esq()
        resposta = "mao_esq_descer_concluido"
        robo.enviar_mensagem(resposta)
    
    elif (msg == "mao_dir_descer"):
        robo.descer_mao_dir()
        resposta = "mao_dir_descer_concluido"
        robo.enviar_mensagem(resposta)

    elif (msg == "mao_esq_levantar"):
        robo.levantar_mao_esq()
        resposta = "mao_esq_levantar_concluido"
        robo.enviar_mensagem(resposta)

    elif (msg == "mao_dir_levantar"):
        robo.levantar_mao_dir()
        resposta = "mao_dir_levantar_concluido"
        robo.enviar_mensagem(resposta)
    
