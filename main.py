import pygame
import sys
from states import menu
from states import selecionar_fase as modal
from states import gameplay as gmp 

def main():
    pygame.init()
    pygame.mixer.init()

    # Definições da tela
    largura_tela = 1280
    altura_tela = 720
    tela = pygame.display.set_mode((largura_tela, altura_tela))
    pygame.display.set_caption("Caça ao Tesouro - UFPB")
    
    # Carregamento de recursos essenciais
    fontes = {
        'normal': pygame.font.SysFont('Arial', 30),
        'titulo': pygame.font.SysFont('Arial', 60, bold=True)
    }
    fundo = menu.imagem_fundo('assets/fundo.png', largura_tela, altura_tela)
    menu.musica_fundo('assets/som_fundo.mp3')

 
    # 1. Prepara e chama o loop do menu, aguardando uma escolha.
    botao, info_do_titulo = menu.preparar_menu(largura_tela, altura_tela, fontes)
    escolha_menu = menu.menu_dificuldade(tela, fundo, botao, fontes, info_do_titulo)
    
    # 2. Se a escolha for 'JOGAR', o programa prossegue para o modal.
    if escolha_menu == 'JOGAR':
        # Chama o loop do modal, aguardando as configurações.
        configuracoes = modal.settings_modal_loop(tela, fundo, fontes)
        
        # 3. Se o modal retornou configurações (não foi fechado), o jogo iniciaria.
        if configuracoes:
            print("Configurações recebidas, iniciando o jogo com:")
            print(configuracoes)
        gmp.run_game_loop(tela, (largura_tela, altura_tela), configuracoes)
    elif escolha_menu == 'SAIR':
        pygame.quit()

    sys.exit()

if __name__ == '__main__':
    main()