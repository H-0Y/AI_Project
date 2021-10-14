# -*- coding: utf-8 -*-
import game
import time
import copy          
import DQN
import numpy as np
        
   
if __name__=="__main__":
    
    begin = time.time()
    winner_conut = 0
    #mcts 只能为第一个ｐｌａｙｅｒ
    game_ddz = game.Game(["mcts","little_smart"])
    #print("here")
    result = 0
    if 'DQN' in game_ddz.model:
        DQN_index_list = []
        for i in range(len(game_ddz.model)):           
            if game_ddz.model[i] == 'DQN':
                DQN_index_list.append(i)
    game_round = 100

    # 初始化存储list
    #input_list = []
    #reward_list = []

    #load
    if 'DQN' in game_ddz.model:
        input_list = np.load("input_data.npy").tolist()
        reward_list = np.load("reward_data.npy").tolist()

    for j in range(game_round):
        #game_ddz = copy.deepcopy(game_ddz)
        game_ddz.game_start()
        #print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        game_ddz1 = copy.deepcopy(game_ddz)

        # 保存ｄａｔａ
        in_loop_input = []
        in_loop_reward = []

        # 记录每一轮所剩余的手牌
        new_cards_left_record = []

        i = 0
        #print("here")
        while (game_ddz1.playrecords.winner == 0):
            if j == 0 or j == game_round-1:
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                game_ddz1.playrecords.show(str(i))
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            new_cards_left_record.append(game_ddz1.playrecords.get_cards_left())
            game_ddz1.next_move()
            
            i = i + 1

        print("round " , j+1)
        print("winner:", game_ddz1.playrecords.winner)
        if game_ddz1.playrecords.winner == 1:
            result+=1
        #print(new_cards_left_record)
        #print(len(new_cards_left_record))

        if 'DQN' in game_ddz1.model: 
            
            if len(DQN_index_list) == 1:
                index = DQN_index_list[0]
                if game_ddz1.playrecords.winner == index + 1:
                    winner_conut += 1
                    reward = 100
                else: reward = -100
            else:
                print('two DQN')
                #选择赢的一方来训练网络
                index = game_ddz1.playrecords.winner - 1
                reward = 100

            DQN_player = game_ddz1.players[index]

            #Training the NN
            record = game_ddz1.playrecords.records
            record.reverse()
            new_cards_left_record.reverse()
            #print(len(record) == len(new_cards_left_record))
            #print(record)
            DQN_index = index + 1 

            if index == 0: enemy_index = 1
            else: enemy_index = 0 

            # 改变ｒｅｗａｒｄ
            # 地主
            if DQN_index == 1:
                reward *= 1.2
            # 手牌
            #print(record)
            card_length = len(record[1][2])
            reward -= card_length*10

            for k in range(len(record)):
                if record[k][0] == DQN_index:
                    rec = record[k]

                    # 构建手牌table
                    #print([card.name+card.color for card 
                    # in new_cards_left_record[k][index]])
                    input = DQN.get_table_of_cards(new_cards_left_record[k][index])
                    # 构建出牌table
                    if rec[1] == 'buyao' or rec[1] == 'yaobuqi':
                        #reward -= 5
                        move_table = DQN.get_table_of_cards([])
                    else:
                        #reward += len(rec[1])*2
                        move_table = DQN.get_table_of_cards(rec[1])
                    #print([card.name+card.color for card in rec[1]])
                    # 构建已出牌组table
                    record_list = []
                    for history in record[k+1:]:
                        if history[1] != 'yaobuqi' and history[1] != 'buyao':
                            record_list.extend(history[1])
                    #print([card.name+card.color for card in record_list])
                    record_table = DQN.get_table_of_cards(record_list)

                    # 构建对手手牌长度
                    enemy_length = [int(len(new_cards_left_record[k][enemy_index]))]
                    #print(enemy_length)

                    input.extend(move_table)
                    input.extend(record_table)
                    input.extend(enemy_length)

                    in_loop_input.append(input)
                    in_loop_reward.append(reward)
                    #DQN_player.net.train(input,reward)
                    reward *= 0.97

            if (j+1) % 20 == 0:
                print("------training-------")
                DQN_player.net.train(in_loop_input,in_loop_reward)
                input_list.extend(in_loop_input)
                reward_list.extend(in_loop_reward)
                in_loop_input = []
                in_loop_reward = []

            if (j+1) % 50 == 0:
                print('DQN Win time: ' + str(winner_conut) +'/' + str(j+1-50) + "-" + str(j+1))
                winner_conut = 0
                
            if j == game_round - 1:
                DQN_player.net.save_model()
        game_ddz1.playrecords.winner = 0

    #save
    if 'DQN' in game_ddz.model:
        np.save("input_data.npy",input_list)
        np.save("reward_data.npy", reward_list)
        print("data saved")
    print("win rate:",result/100)

        

        


    #print(time.time()-begin)
    