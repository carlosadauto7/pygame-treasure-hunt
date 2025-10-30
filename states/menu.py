import pygame
from modulos import cores

def imagem_fundo(caminho_imagem, larguraT, alturaT):
    fundo_carregar = pygame.image.load(caminho_imagem).convert()
    fundo = pygame.transform.scale(fundo_carregar, (larguraT, alturaT))
    return fundo

def musica_fundo(nome_arquivo):
    pygame.mixer.music.set_volume(0.03)
    pygame.mixer.music.load(nome_arquivo)
    pygame.mixer.music.play(-1)

def preparar_menu(largura_tela, altura_tela, fontes):

    largura_botao = 300
    altura_botao = 60
    inicio_y = altura_tela // 2 
    x_centro = (largura_tela - largura_botao) // 2

    rect = pygame.Rect(x_centro, inicio_y, largura_botao, altura_botao)
    rect2 = pygame.Rect(x_centro, inicio_y+68, largura_botao, altura_botao)
    botoes = [{'texto': 'JOGAR', 'rect': rect}, {'texto': 'SAIR', 'rect': rect2}]

    texto_titulo = 'CAÇA AO TESOURO'
    titulo_renderizado = fontes['titulo'].render(texto_titulo, True, cores.BRANCO)

    x_titulo = (largura_tela - titulo_renderizado.get_width()) // 2
    y_titulo = inicio_y - titulo_renderizado.get_height() - 20

    titulo_info = {'texto': texto_titulo, 'cor': cores.DOURADO_PALIDO, 'pos': (x_titulo, y_titulo)}
    return botoes, titulo_info

def desenhar_menu(tela, fundo, botao, fontes, titulo_info):
    tela.blit(fundo, (0, 0))
    titulo_jogo = fontes['titulo'].render(titulo_info['texto'], True, titulo_info['cor'])
    tela.blit(titulo_jogo, titulo_info['pos'])

    retangulo1 = botao[0]['rect']
    retangulo2 = botao[1]['rect']
    texto1 = botao[0]['texto']
    texto2 = botao[1]['texto']

    cor_botao1 = ''
    pos_mouse = pygame.mouse.get_pos()
    if retangulo1.collidepoint(pos_mouse):
        cor_botao1 = cores.AZUL_ARDOUSO 
    else:
        cor_botao1 = cores.PRETO

    cor_botao2 = ''
    pos_mouse = pygame.mouse.get_pos()
    if retangulo2.collidepoint(pos_mouse):
        cor_botao2 = cores.AZUL_ARDOUSO 
    else:
        cor_botao2 = cores.PRETO

    pygame.draw.rect(tela, cor_botao1, retangulo1, border_radius=12)
    palavra = fontes['normal'].render(texto1, True, cores.BRANCO)

    pos_x_palavra = retangulo1.x + (retangulo1.width - palavra.get_width()) // 2
    pos_y_palavra = retangulo1.y + (retangulo1.height - palavra.get_height()) // 2
    tela.blit(palavra, (pos_x_palavra, pos_y_palavra))

    pygame.draw.rect(tela, cor_botao2, retangulo2, border_radius=12)
    palavra = fontes['normal'].render(texto2, True, cores.BRANCO)

    pos_x_palavra = retangulo2.x + (retangulo2.width - palavra.get_width()) // 2
    pos_y_palavra = retangulo2.y + (retangulo2.height - palavra.get_height()) // 2
    tela.blit(palavra, (pos_x_palavra, pos_y_palavra))

def menu_dificuldade(tela, fundo, botoes, fontes, titulo_info):
    while True:
        desenhar_menu(tela, fundo, botoes, fontes, titulo_info)
        pygame.display.flip()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return 'SAIR'
            if evento.type == pygame.MOUSEBUTTONDOWN:
                for botao in botoes:
                    if botao['texto'] == 'JOGAR':
                        if botao['rect'].collidepoint(evento.pos):
                            return 'JOGAR'
                    else:
                        if botao['rect'].collidepoint(evento.pos):
                            return 'SAIR'