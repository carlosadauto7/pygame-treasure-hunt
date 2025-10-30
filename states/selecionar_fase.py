# Conteúdo para o arquivo: states/settings_modal.py

import pygame
from modulos import cores

def preparar_settings_modal(largura_tela):
    """Prepara os retângulos e textos para a tela de configuração da partida."""
    ui_elements = {}
    
    # --- MODIFICADO: Lógica para o seletor de tamanho ---
    largura_seletor_display = 280
    largura_seta = 60
    altura_seletor = 50
    espaco = 8
    largura_total = largura_seta * 2 + espaco * 2 + largura_seletor_display
    x_inicio_seletor = (largura_tela - largura_total) // 2
    y_seletor = 200

    ui_elements['seletor_tamanho'] = {
        'label': 'Tamanho do Tabuleiro:',
        'rect_esquerda': pygame.Rect(x_inicio_seletor, y_seletor, largura_seta, altura_seletor),
        'rect_display': pygame.Rect(x_inicio_seletor + largura_seta + espaco, y_seletor, largura_seletor_display, altura_seletor),
        'rect_direita': pygame.Rect(x_inicio_seletor + largura_seta + espaco + largura_seletor_display + espaco, y_seletor, largura_seta, altura_seletor)
    }

    # --- Campos de Input de Nome (sem alteração) ---
    largura_input_nome = 400
    x_centro_nome = (largura_tela - largura_input_nome) // 2
    ui_elements['input_nome1'] = {'rect': pygame.Rect(x_centro_nome, 300, largura_input_nome, 50), 'label': 'Nome do Jogador 1:'}
    ui_elements['input_nome2'] = {'rect': pygame.Rect(x_centro_nome, 400, largura_input_nome, 50), 'label': 'Nome do Jogador 2:'}

    # --- Botão de Iniciar (sem alteração) ---
    ui_elements['botao_iniciar'] = {'rect': pygame.Rect(x_centro_nome, 500, largura_input_nome, 60), 'texto': 'INICIAR JOGO'}

    return ui_elements


def desenhar_settings_modal(tela, fundo, ui_elements, fontes, valores_input, input_ativo, tamanho_atual):
    """Desenha todos os elementos da tela de configuração."""
    tela.blit(fundo, (0, 0))
    pos_mouse = pygame.mouse.get_pos()

    # =================ABAIXO ESTÁ AS CONDICOES PARA VERIFICAR E PREENCHER A TELA COM OS ELEMENTOS==================================

    for chave, valor in ui_elements.items():
        if chave == 'seletor_tamanho':
            # Desenha o rótulo
            label_render = fontes['normal'].render(valor['label'], True, cores.BRANCO)
            tela.blit(label_render, (valor['rect_esquerda'].x, valor['rect_esquerda'].y - 30))
            

            # --- MODIFICADO: Desenha a seta da esquerda como um triângulo ---
            rect_esq = valor['rect_esquerda']
            cor_esq = ''

            if rect_esq.collidepoint(pos_mouse):
                cor_esq = cores.AZUL_ARDOUSO
            else:
                cor_esq = cores.CINZA

            pygame.draw.rect(tela, cor_esq, rect_esq, border_radius=8)


            # Calcula os 3 pontos do triângulo baseados no centro do retângulo
            ponto1_esq = (rect_esq.centerx + 10, rect_esq.centery - 15)
            ponto2_esq = (rect_esq.centerx + 10, rect_esq.centery + 15)
            ponto3_esq = (rect_esq.centerx - 10, rect_esq.centery)

            pygame.draw.polygon(tela, cores.BRANCO, [ponto1_esq, ponto2_esq, ponto3_esq])

            # Desenha o display do valor (sem alteração)

            pygame.draw.rect(tela, cores.PRETO, valor['rect_display'], border_radius=8)
            valor_texto = f"{tamanho_atual}x{tamanho_atual}"
            valor_render = fontes['normal'].render(valor_texto, True, cores.BRANCO)
            tela.blit(valor_render, valor_render.get_rect(center=valor['rect_display'].center))

            rect_dir = valor['rect_direita']
            cor_dir = ''

            if rect_dir.collidepoint(pos_mouse):
                cor_dir = cores.AZUL_ARDOUSO
            else:
                cor_dir = cores.CINZA

            pygame.draw.rect(tela, cor_dir, rect_dir, border_radius=8)

            # Calcula os 3 pontos do triângulo baseados no centro do retângulo
            
            ponto1_dir = (rect_dir.centerx - 10, rect_dir.centery - 15)
            ponto2_dir = (rect_dir.centerx - 10, rect_dir.centery + 15)
            ponto3_dir = (rect_dir.centerx + 10, rect_dir.centery)
            pygame.draw.polygon(tela, cores.BRANCO, [ponto1_dir, ponto2_dir, ponto3_dir])

        elif chave.startswith('input'):
            #=============================INPUT VAI SE REFERIR AS CAIXAS DE TEXTO===============================================
            rect = valor['rect']
            label_render = fontes['normal'].render(valor['label'], True, cores.BRANCO)
            tela.blit(label_render, (rect.x, rect.y - 30))

            cor_borda = None

            if input_ativo == chave:
                cor_borda = cores.AMARELO
            else:
                cor_borda = cores.BRANCO

            pygame.draw.rect(tela, cores.PRETO, rect)
            pygame.draw.rect(tela, cor_borda, rect, 2, border_radius=8)

            texto_surface = fontes['normal'].render(valores_input[chave], True, cores.BRANCO)
            tela.blit(texto_surface, (rect.x + 10, rect.y + (rect.height - texto_surface.get_height()) // 2))

        elif chave.startswith('botao'):
            #============================BOTAO PARA IR AO JOGO======================================================================
            pos_mouse = pygame.mouse.get_pos()
            rect = valor['rect']
            cor_fundo = ''

            if rect.collidepoint(pos_mouse):
                cor_fundo = cores.AZUL_ARDOUSO
            else:
                cor_fundo = cores.CINZA

            pygame.draw.rect(tela, cor_fundo, rect, border_radius=12)
            texto_render = fontes['normal'].render(valor['texto'], True, cores.BRANCO)
            tela.blit(texto_render, texto_render.get_rect(center=rect.center))

def settings_modal_loop(tela, fundo, fontes):
    """Roda o loop de eventos para a tela de configuração."""
    ui_elements = preparar_settings_modal(tela.get_width())
    
    # MODIFICADO: O tamanho agora é um número, não um texto
    tamanho_atual = 4 # Valor inicial
    valores_input = {
        'input_nome1': 'Jogador 1',
        'input_nome2': 'Jogador 2'
    }
    input_ativo = None
    
    while True:
        # Passa o 'tamanho_atual' para a função de desenho
        desenhar_settings_modal(tela, fundo, ui_elements, fontes, valores_input, input_ativo, tamanho_atual)
        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return None

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:
                    input_ativo = None # Desativa inputs de texto ao clicar
                    
                    # --- MODIFICADO: Lógica de clique para o seletor e outros botões ---
                    if ui_elements['seletor_tamanho']['rect_esquerda'].collidepoint(evento.pos):
                        tamanho_atual = max(4, tamanho_atual - 1) # Limite mínimo de 3
                    
                    elif ui_elements['seletor_tamanho']['rect_direita'].collidepoint(evento.pos):
                        tamanho_atual = min(20, tamanho_atual + 1) # Limite máximo de 20

                    elif ui_elements['botao_iniciar']['rect'].collidepoint(evento.pos):
                        if valores_input['input_nome1'] and valores_input['input_nome2']:
                            return {
                                'tamanho': tamanho_atual, # Usa o valor numérico
                                'nome_p1': valores_input['input_nome1'],
                                'nome_p2': valores_input['input_nome2']
                            }
                    # Verifica cliques nos inputs de texto
                    elif ui_elements['input_nome1']['rect'].collidepoint(evento.pos):
                        input_ativo = 'input_nome1'
                    elif ui_elements['input_nome2']['rect'].collidepoint(evento.pos):
                        input_ativo = 'input_nome2'

            # MODIFICADO: A lógica de digitação agora só se aplica aos nomes
            if evento.type == pygame.KEYDOWN and input_ativo:
                texto_atual = valores_input[input_ativo]
                if evento.key == pygame.K_BACKSPACE:
                    valores_input[input_ativo] = texto_atual[:-1]
                elif len(texto_atual) < 15: # Limite de caracteres para nomes
                    valores_input[input_ativo] += evento.unicode