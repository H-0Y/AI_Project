import myutil
import random


def choose(next_move_types, next_moves, last_move_type, model, cards_left1, cards_left2, player_id, net, playerecord):
    from mcts import MCTSModel
    if player_id == 0:
        my_cards = cards_left1
        enemy_cards = cards_left2
    else:
        my_cards = cards_left2
        enemy_cards = cards_left1

    if model == "random":
        #print("?????????????????????")
        return myutil.choose_random(next_move_types, next_moves, last_move_type)
    if model == "little_smart":
        #print("!!!!!!!!!!!!!!!!!!!!!!!!")
        return myutil.choose_with_little_smart(next_move_types, next_moves, last_move_type)
    if model == "mcts":
        prop = random.randint(1,100)
        if prop > 79:
            myutil.choose_random(next_move_types, next_moves, last_move_type)
        if len(next_move_types) == 0:
            return "yaobuqi",[]
        mc = MCTSModel()
        return mc.choose_with_mcts(next_moves, next_move_types, last_move_type,my_cards,enemy_cards,player_id)
    if model == "DQN":
        return myutil.choose_DQN(next_move_types, next_moves, last_move_type, my_cards, net, playerecord, len(enemy_cards))
    if model == "manual":
        return myutil.choose_manual(next_move_types, next_moves, last_move_type, my_cards)