import pygame
from modulos import cores # Assumindo 'cores.py' está em uma pasta 'modulos'
import logic.logica_jogo as lg # Importa o módulo de lógica do jogo
from states import menu
import main

# --- Funções de Carregamento de Recursos ---
def load_spritessheet_lines(sprite_states):
    # CORRIGIDO: Erros de digitação em .load() e .convert_alpha()
    sprite_sheet_img = pygame.image.load(sprite_states['caminho']).convert_alpha()

    sheet_largura, sheet_altura = sprite_sheet_img.get_size()
    frame_largura = sheet_largura // sprite_states['linhas']
    frame_altura = sheet_altura // sprite_states['linhas']

    linhas_frames = []
    for linha in range(sprite_states['linhas']):
        frames_da_linha = []
        for coluna in range(sprite_states['colunas']):
            x = coluna * frame_largura
            y = linha * frame_altura
            frame = sprite_sheet_img.subsurface((x, y, frame_largura, frame_altura))
            frames_da_linha.append(frame)
        linhas_frames.append(frames_da_linha)
    return linhas_frames, frame_largura, frame_altura

# --- Funções de Desenho ---

def draw_board(screen, ref_board, board_x, board_y, cell_size, font, screen_size, game_state, tesouro_img, buraco_img):
    largura, altura = screen_size
    board_size = len(ref_board)
    pygame.draw.rect(screen, (25, 43, 84), (0, 0, largura//2, altura))

    pygame.draw.rect(screen, (84, 25, 29), (largura//2, 0, largura//2, altura))

    if(game_state['turn'] % 2 == 0):
        pygame.draw.rect(screen, (43, 65, 173), (0, 0, largura//2, altura))
    else:
         pygame.draw.rect(screen, (173, 43, 52), (largura//2, 0, largura//2, altura))
    for i in range(board_size):
        for j in range(board_size):
            rect = pygame.Rect(board_x + j*cell_size, board_y + i * cell_size, cell_size, cell_size)
            
            cell_content = ref_board[i][j]
            color = None
            if cell_content == '#':
                color = None
                if rect.collidepoint(pygame.mouse.get_pos()):
                    color = (144, 144, 144)
                else:
                    color = (155, 155, 155)
                pygame.draw.rect(screen, color, rect)
            elif cell_content == 'T':
                # Desenha a imagem redimensionada
                screen.blit(tesouro_img, rect)
            elif cell_content == 'B':
                # Desenha a imagem redimensionada tbm
                screen.blit(buraco_img, rect) 
            else:
                val = int(cell_content)
                if val > 0:
                    color = (100 + val*30, 100 + val*30, 255 - val*30) 
                else:
                    color = (180, 180, 180) 

                pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (0, 0, 0), rect, 1)

            if cell_content not in ['#', 'T', 'B']:
                text_surface = font.render(str(cell_content), True, (0, 0, 0))
                text_rect = text_surface.get_rect(center=rect.center)
                screen.blit(text_surface, text_rect)
        
def draw_game_info(screen, game_state, font_destaque, largura_tela, players_sprites, frame_largura, frame_altura, spsh_gamerun, config):

    if game_state['turn'] % 2 == 0:
        linha_animacao_j1 = 0
        linha_animacao_j2 = 2 
        alturaj1 = 300
        alturaj2 = 348
    else:
        linha_animacao_j1 = 1 
        linha_animacao_j2 = 3 
        alturaj1 = 350
        alturaj2 = 325

    game_state['frame_index'] = (game_state.get('frame_index', 0) + game_state['frame_speed'])
    if game_state['frame_index'] >= spsh_gamerun['colunas']:
        game_state['frame_index'] = 0

    frame_atual_int = int(game_state['frame_index'])

    # Pega o frame correto da lista para cada jogador
    frame_j1 = players_sprites[linha_animacao_j1][frame_atual_int]
    frame_j2 = players_sprites[linha_animacao_j2][frame_atual_int]

    # Redimensiona os frames
    char_largura = int(frame_largura * 0.5)
    char_altura = int(frame_altura * 0.5)
    pirata1_render = pygame.transform.scale(frame_j1, (char_largura, char_altura))
    pirata2_render = pygame.transform.scale(frame_j2, (char_altura, char_altura))

    # --- Informações do Jogador 1 (esquerda) ---
    font_j1 = font_destaque 
    cor_j1 = cores.BRANCO 
    jogador_1 = config['nome_p1']
    texto_j1 = font_j1.render(jogador_1, True, cor_j1)
    texto_pontos1 = font_j1.render(f"Pontos: {game_state['score1']}", True, cor_j1)

    # Posição das infos acima do pirata 1
    area_j1_x_center = 153

    pygame.draw.rect(screen, cores.CINZA, (35, 410, 250, 60), 0)

    screen.blit(texto_j1, texto_j1.get_rect(center=(area_j1_x_center, 437)))
    screen.blit(texto_pontos1, texto_pontos1.get_rect(center=(area_j1_x_center, 629)))
    screen.blit(pirata1_render, pirata1_render.get_rect(center=(area_j1_x_center, alturaj1)))


    # --- Informações do Jogador 2 (direita) ---
    font_j2 = font_destaque 
    cor_j2 = cores.BRANCO 
    jogador_2 = config['nome_p2']
    texto_j2 = font_j2.render(jogador_2, True, cor_j2)
    texto_pontos2 = font_j2.render(f"Pontos: {game_state['score2']}", True, cor_j2)

    # Posição das infos acima do pirata 2
    area_j2_x_center = 1130

    pygame.draw.rect(screen, cores.CINZA, (1000, 410, 250, 60), 0)

    screen.blit(texto_j2, texto_j2.get_rect(center=(area_j2_x_center, 437)))
    screen.blit(texto_pontos2, texto_pontos2.get_rect(center=(area_j2_x_center, 629)))
    screen.blit(pirata2_render, pirata2_render.get_rect(center=(area_j2_x_center, alturaj2)))


    # --- Mensagem "Vez do Jogador X" centralizada no topo ---
    font_vez_destaque = font_destaque 
    cor_vez = cores.BRANCO 

    if game_state['turn'] % 2 == 0:
        turn_text_display = f"Vez de {config['nome_p1']}"
    else:
        turn_text_display = f"Vez de {config['nome_p2']}"
    
    vez_surface = font_vez_destaque.render(turn_text_display, True, cor_vez)
    vez_rect = vez_surface.get_rect(center=(largura_tela // 2, 25))
    screen.blit(vez_surface, vez_rect)


def draw_game_over_message(screen, game_state, j1, j2):
    """Desenha a mensagem de fim de jogo centralizada."""

    #========================== LÓGICA DO TEXTO INÍCIO ===========================================

    font_g = pygame.font.Font(None, 60)
    font_m = pygame.font.Font(None, 35)
    font_p = pygame.font.Font(None, 24)

    texto_vencedor = ""
    pygame.draw.rect(screen, (66, 66, 77, 0.164), (screen.get_width() // 2 - 300, screen.get_height() // 2 - 150, 600, 300), 0)
    empate = False
    if game_state['score1'] > game_state['score2']:
        texto_vencedor = f"{j1} Venceu!"
        pontuacao_ganhador = game_state['score1']

        pontuacao_perdedor = game_state['score2']
        texto_perdedor = f'Pontuação de {j2}: %d' % pontuacao_perdedor 
        
    elif game_state['score2'] > game_state['score1']:
        texto_vencedor = f"{j2} Venceu!"
        pontuacao_ganhador = game_state['score2']

        pontuacao_perdedor = game_state['score1']
        texto_perdedor = f'Pontuação de {j1}: %d' % pontuacao_perdedor 
    else:
        empate = True
        texto_vencedor = "Empate!"
        
    if not empate:
        text_surface = font_g.render(texto_vencedor, True, cores.AMARELO)
        text_rect = text_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2-67))

        screen.blit(text_surface, text_rect)

        text_surface = font_p.render(f'Pontuação: {pontuacao_ganhador}', True, cores.AMARELO)
        text_rect = text_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2-30))

        screen.blit(text_surface, text_rect)

        text_surface = font_m.render(texto_perdedor, True, cores.BRANCO)
        text_rect = text_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))

        screen.blit(text_surface, text_rect)
    else:
        text_surface = font_g.render(texto_vencedor, True, cores.AMARELO)
        text_rect = text_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2-67))

        screen.blit(text_surface, text_rect)

        text_surface = font_p.render('Pontuação do jogador 1: %d' % game_state['score1'], True, cores.BRANCO)
        text_rect = text_surface.get_rect(center=(screen.get_width() // 2 - 130, screen.get_height() // 2-15))

        screen.blit(text_surface, text_rect)

        text_surface = font_p.render('Pontuação do jogador 2: %d' % game_state['score2'], True, cores.BRANCO)
        text_rect = text_surface.get_rect(center=(screen.get_width() // 2 + 130, screen.get_height() // 2-15))

        screen.blit(text_surface, text_rect)
        

    

    #========================== LÓGICA DO TEXTO FIM ===========================================

    #========================== LÓGICA DOS BOTOES INÍCIO ===========================================

    rect1 = pygame.Rect(screen.get_width() // 2 - 280, screen.get_height() // 2  + 50, 270, 70)
    pygame.draw.rect(screen, cores.CINZA, rect1)
    rect2 = pygame.Rect(screen.get_width() // 2 + + 10, screen.get_height() // 2  + 50, 270, 70)
    pygame.draw.rect(screen, cores.CINZA, rect2)

    text_surface = font_m.render('Jogar novamente', True, cores.BRANCO)
    text_rect = text_surface.get_rect(center=(screen.get_width() // 2 - 145, screen.get_height() // 2  + 85))

    screen.blit(text_surface, text_rect)

    text_surface = font_m.render('Voltar ao menu', True, cores.BRANCO)
    text_rect = text_surface.get_rect(center=(screen.get_width() // 2 + 145, screen.get_height() // 2  + 85))

    screen.blit(text_surface, text_rect)
    return rect1, rect2
# --- Função Principal do Loop de Jogo ---
def run_game_loop(screen, screen_size, config):

    board_size = config['tamanho']
            
    spritessheet_states_gamerun = {
        "caminho": 'assets/sprites.png',
        "colunas": 4,
        "linhas": 4,
        'fps': 12
        
    }

    
    board_rect_size = 640
    board_rect_x = (screen_size[0] - board_rect_size) // 2
    board_rect_y = (screen_size[1] - board_rect_size) // 2
    
    cell_size = board_rect_size // board_size

    tesouro_imagem = pygame.image.load("assets/tesouro.png").convert_alpha()
    buraco_imagem = pygame.image.load("assets/buraco.png").convert_alpha()
    
    TESOURO_IMG = pygame.transform.scale(tesouro_imagem, (cell_size, cell_size))
    BURACO_IMG = pygame.transform.scale(buraco_imagem, (cell_size, cell_size))

    game_state = lg.initialize_game_state(board_size)
    
    # --- ADICIONADO: Chaves para controlar a animação ---
    game_state['frame_index'] = 0.0
    game_state['frame_speed'] = 0.2

    # --- ADICIONADO: Carrega os sprites UMA VEZ antes do loop ---
    players_sprites, frame_largura, frame_altura = \
        load_spritessheet_lines(spritessheet_states_gamerun)
    
    no_jogo = True

    # --- Fontes ---
    font_large = pygame.font.Font(None, 40)
    # CORREÇÃO AQUI: Crie a fonte normal e depois defina negrito
    font_destaque_info = pygame.font.Font(None, 35) 
    font_destaque_info.set_bold(True) # Define o estilo negrito

    clock = pygame.time.Clock()

    while no_jogo:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                no_jogo = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                
                j = (mouse_x - board_rect_x) // cell_size
                i = (mouse_y - board_rect_y) // cell_size

                if 0 <= i < board_size and 0 <= j < board_size:
                    # Passa o game_state e i, j para sua função handle_turn
                    # MODIFICADO: para garantir que o estado seja sempre atualizado
                    game_state = lg.handle_turn(game_state, i, j)
                    # Verifica se o jogo terminou após a jogada
                    if game_state['game_over']:
                        no_jogo = False 
                
        screen.fill((20, 20, 20)) 

        draw_board(screen, game_state['ref_board'], board_rect_x, board_rect_y, cell_size, font_large, screen_size, game_state, TESOURO_IMG, BURACO_IMG)

        # Atualizando a chamada para draw_game_info
        # Agora não precisamos passar as imagens, pois elas são carregadas dinamicamente dentro da função
        # MODIFICADO: passando os sprites carregados para a função de desenho
        draw_game_info(screen, game_state, font_destaque_info, screen_size[0], 
                       players_sprites, frame_largura, frame_altura, spritessheet_states_gamerun, config)
        rect1, rect2 = None, None
        if game_state['game_over']:
            rect1, rect2 = draw_game_over_message(screen, game_state, config['nome_p1'], config['nome_p2'])
                            
        pygame.display.flip()

        # --- ADICIONADO: Controla a velocidade do loop ---
        clock.tick(spritessheet_states_gamerun['fps'])

    # Loop para a tela de Game Over

    game_over_loop = game_state['game_over']
    while game_over_loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over_loop = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if rect2.collidepoint(event.pos):
                    game_over_loop = False
                    main.main()
                elif rect1.collidepoint(event.pos):
                    game_over_loop = False
                    run_game_loop(screen, screen_size, config)