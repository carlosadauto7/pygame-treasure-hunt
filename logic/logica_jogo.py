from . import matrizes as mt

def initialize_game_state(n):
    board = mt.matriz_geral(n)
    ref_board = [['#']*n for i in range(n)]
    num_tes, num_bur = mt.count(mt.matriz(n))

    game_state = {
        'board': board,
        'ref_board': ref_board,
        'num_tes': num_tes,
        'num_bur': num_bur,
        'celulas_reveladas': 0,
        'tesouros_achados': 0,
        'score1': 0,
        'score2': 0,
        'turn': 0,
        'game_over': False
    }
    return game_state

def handle_turn(game_state, i, j):

    if(game_state['ref_board'][i][j] != '#' or game_state['game_over']):
        return game_state
    
    conteudo_celula = game_state['board'][i][j]
    game_state['ref_board'][i][j] = conteudo_celula


    if(conteudo_celula == "T"):
        game_state['tesouros_achados'] += 1
        if game_state['turn'] % 2 == 0:
            game_state['score1'] += 100
        else:
            game_state['score2'] += 100
        game_state['celulas_reveladas'] += 1
    elif(conteudo_celula == 'B'):
        if game_state['turn'] % 2 == 0:
            game_state['score1'] = max(0, game_state['score1'] - 50)
        else:
            game_state['score2'] = max(0, game_state['score2'] - 50)
        game_state['celulas_reveladas'] += 1
    
    game_state['turn'] += 1

    check_game_over(game_state)

    return game_state

def check_game_over(game_state):
    total_items = game_state['num_tes'] + game_state['num_bur']
    if((game_state['tesouros_achados'] >= game_state['num_tes']) or (game_state['celulas_reveladas'] >= total_items)):
        game_state['game_over'] = True