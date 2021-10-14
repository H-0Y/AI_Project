# -*- coding: utf-8 -*-
import numpy as np
import DQN
import random

#展示扑克函数
def card_show(cards, info, n):
    
    #扑克牌记录类展示
    if n == 1:
        print(info)
        names = []
        for i in cards:
            names.append(i.name+i.color)
        print(names)    
    #Moves展示
    elif n == 2:
        if len(cards) == 0:
            return 0
        print(info)
        moves = []
        for i in cards:
            names = []
            for j in i:
                names.append(j.name+j.color)
            moves.append(names)
        print(moves)  
    #record展示
    elif n == 3:
        print(info)
        names = []
        for i in cards:
            tmp = []
            tmp.append(i[0])
            tmp_name = []
            #处理要不起
            try:
                for j in i[1]:
                    tmp_name.append(j.name+j.color)
                tmp.append(tmp_name)
            except:
                tmp.append(i[1])
            names.append(tmp)
        print(names)
       

#在Player的next_moves中选择出牌方法


#random
def choose_random(next_move_types, next_moves, last_move_type):
    #要不起
    if len(next_moves) == 0:
        return "yaobuqi", []
    else:
        #start不能不要
        if last_move_type == "start":
            r_max = len(next_moves)
        else:
            r_max = len(next_moves)+1
        r = np.random.randint(0,r_max)
        #添加不要
        if r == len(next_moves):
            return "buyao", []
    """print("chudepai:")
    for i in range(len(next_moves[r])):
        print(next_moves[r][i].name)"""
    #sort_all_rank(next_moves)
    return next_move_types[r], next_moves[r]
    
# little_smart
def choose_with_little_smart(next_move_types, next_moves, last_move_type):
    
        
    if len(next_moves) == 0:
        return "yaobuqi", []
    else:
        return sort_all_rank(next_moves,next_move_types,last_move_type)

#DQN
def choose_DQN(next_move_types, next_moves, last_move_type, cards, net, record, length_of_enemy):
    #要不起
    if len(next_moves) == 0:
        return "yaobuqi", [] 
    else:
        # 有一定的概率随机出牌，方便在训练中遍历更多情况(10%)
        '''
        prop = random.randint(1,100)
        if prop > 89:
            choose_random(next_move_types, next_moves, last_move_type)
        '''

        # 根据ＤＱＮ出牌
        # 初始化
        best_action = next_moves[0] 
        best_action_type = next_move_types[0]
        max_value = -999999999
        # 构建我自己手牌的table
        cards_table = DQN.get_table_of_cards(cards)

        #print([card.name+card.color for card in cards])
        #print(cards_table)


        #　构建已经出牌的table
        #print(record.records)
        record_list = []
        for rec in record.records:
            if rec[1] != 'yaobuqi' and rec[1] != 'buyao':
                record_list.extend(rec[1])
        record_table = DQN.get_table_of_cards(record_list)
        #print([card.name + card.color for card in record_list])
        #print(record_table)

        # 添加对手牌组长度
        enemy_length = [int(length_of_enemy)]
        #print(enemy_length)

        if last_move_type != "start":
            next_move_types.append("buyao")
            next_moves.append([])
    
        #print([[card.name + card.color for card in move] for move in next_moves])
        for i in range(len(next_moves)):
            # 构建action的table
            move_table = DQN.get_table_of_cards(next_moves[i])
            # 构建同一长度的input(54+54+54+1=163)
            input = cards_table.copy()
            input.extend(move_table)
            input.extend(record_table)
            input.extend(enemy_length)
            #print(input)
            value = net.get_value_only(input)
            #print([card.name + card.color for card in next_moves[i]],value)
            if value > max_value:
                max_value = value
                best_action = next_moves[i]
                best_action_type = next_move_types[i]
        return best_action_type, best_action


#manual
def choose_manual(next_move_types, next_moves, last_move_type, cards):
    #要不起
    if len(next_moves) == 0:
        return "yaobuqi", [] 
    else:
        # 展示手牌
        card_show(cards,"Your card: ", 1)
        card_show(next_moves,"Moves: ", 2)
        #print(cards)
        move_index_list = []
        for move in next_moves:
            move_index_list.append([cards.index(card) for card in move])
        print("Move index combination: ", move_index_list)
        
        # 要求输入
        print("Print the index of cards in the deck shown above, split with comma")
        input_list = input('>>>')
        #　最开始不能出不要
        while last_move_type == 'start' and input_list == 'buyao':
            print("Illegal combinations, try again!")
            input_list = input('>>>')
        if last_move_type != 'start' and input_list == 'buyao':
            return 'buyao', []
        # 处理输入
        move_ind_list = [int(ind) for ind in input_list.split(',')]
        move = [cards[i] for i in move_ind_list]
        while move not in next_moves:
            print("Illegal combinations, try again!")
            input_list = input('>>>')
            move_ind_list = [int(ind) for ind in input_list.split(',')]
            move = [cards[i] for i in move_ind_list]
        # 返回出牌类型和牌组
        index = next_moves.index(move)
        return next_move_types[index], next_moves[index]

#发牌
def game_init(players, playrecords, cards):
    
    #洗牌
    np.random.shuffle(cards.cards)
    #排序
    p1_cards = cards.cards[:23]  # 地主
    p1_cards.sort(key=lambda x: x.rank)
    p2_cards = cards.cards[23:43]
    p2_cards.sort(key=lambda x: x.rank)
    #Dizhupai = cards.cards[40:43]
    left = cards.cards[43:]
    players[0].cards_left = playrecords.cards_left1 = p1_cards
    players[1].cards_left = playrecords.cards_left2 = p2_cards
    #card_show(p1_cards, "1", 1)
    #card_show(p2_cards, "2", 1)
    #card_show(left, "left", 1)
    

class SortCards(object):
    def __init__(self, cards_combination,cards_type):
        self.cards_combination = cards_combination
        self.rank = 0
        self.cards = []
        self.cards_type =cards_type
        

def sort_all_rank(next_moves,next_move_types,last_move_type):
        rankList = {}
        i = 0
        for cards_combination in next_moves:
            #print(i)
            sorted_cards =SortCards(cards_combination,next_move_types[i])
            for cards in cards_combination:
                sorted_cards.cards.append(cards.name)
                sorted_cards.rank += cards.rank
            
            rankList[i] = sorted_cards
            i += 1
        min_pai = sorted(rankList.items(), key=lambda x: x[1].rank,reverse=False)
        max_pai = sorted(rankList.items(), key=lambda x: x[1].rank, reverse=True)
        """print("next moves leng", len(next_moves))
        print("next moves type leng",len(next_move_types))
        print("ranklist leng",len(rankList))
        print("min_pai leng:", len(min_pai))
        print("max_pai leng:",len(max_pai))"""
        """for i in range(len(max_pai)):
            print(max_pai[i][1].cards_type,max_pai[i][1].cards)"""
        if last_move_type != "start":
            return min_pai[0][1].cards_type,min_pai[0][1].cards_combination
        else:
            return max_pai[0][1].cards_type,max_pai[0][1].cards_combination
    
